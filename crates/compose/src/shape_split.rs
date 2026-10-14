//! A stroked shape layer split into its fill and its vector stroke (rasterised over the canvas),
//! for shapes with clipped layers: Photoshop draws the stroke above the clipped layers. Cached
//! per shape state, so tiles (and the GPU's textures) reuse one rasterisation.

use std::collections::HashMap;
use std::hash::{Hash, Hasher};
use std::sync::{Mutex, OnceLock};

use photocraft_color::{PixelFormat, SampleType};
use photocraft_doc::vector::ShapeLayer;
use photocraft_geom::Rect;
use photocraft_raster::Surface;

struct Entry {
    parts: (Surface, Surface),
    tick: u64,
    bytes: usize,
    // Pin the pixels used to fit the stroke: their tile addresses are part of the key.
    _pixels: Option<Surface>,
}

#[derive(Default)]
struct Cache {
    entries: HashMap<u64, Entry>,
    tick: u64,
    bytes: usize,
    generation: u64,
}

impl Cache {
    fn get(&mut self, key: u64) -> Option<(Surface, Surface)> {
        self.tick = self.tick.saturating_add(1);
        let entry = self.entries.get_mut(&key)?;
        entry.tick = self.tick;
        Some(entry.parts.clone())
    }

    fn insert(&mut self, key: u64, parts: (Surface, Surface), pixels: Option<Surface>, budget: usize, generation: u64) {
        let bytes = surface_bytes(&parts.0).saturating_add(surface_bytes(&parts.1)).saturating_add(pixels.as_ref().map_or(0, surface_bytes));
        // Oversized results remain usable by the caller without global retention. A purge
        // also rejects admission by calculations that started before it.
        if bytes > budget || generation != self.generation {
            return;
        }
        if let Some(old) = self.entries.remove(&key) {
            self.bytes = self.bytes.saturating_sub(old.bytes);
        }
        while self.entries.len() >= CAPACITY || self.bytes > budget.saturating_sub(bytes) {
            let Some(old) = self.entries.iter().min_by_key(|(_, e)| e.tick).map(|(&key, _)| key) else { break };
            if let Some(entry) = self.entries.remove(&old) {
                self.bytes = self.bytes.saturating_sub(entry.bytes);
            }
        }
        self.tick = self.tick.saturating_add(1);
        self.bytes = self.bytes.saturating_add(bytes);
        self.entries.insert(key, Entry { parts, tick: self.tick, bytes, _pixels: pixels });
    }

    fn clear(&mut self) -> usize {
        let bytes = self.bytes;
        self.entries.clear();
        self.bytes = 0;
        self.tick = 0;
        self.generation = self.generation.wrapping_add(1);
        bytes
    }
}

type Store = Mutex<Cache>;

fn cache() -> &'static Store {
    static C: OnceLock<Store> = OnceLock::new();
    C.get_or_init(|| Mutex::new(Cache::default()))
}

// A 33-shape layout must not cycle through a 32-entry LRU on every plan. Limit both
// entry overhead and retained pixels; a larger shape is still rendered correctly on a miss.
const CAPACITY: usize = 128;
const CACHE_BUDGET: usize = 128 << 20;

fn surface_bytes(surface: &Surface) -> usize {
    surface.tiles().fold(surface.default_bytes().len(), |bytes, (_, tile)| bytes.saturating_add(tile.bytes().len()))
}

/// Accounted pixel storage, including pinned input pixels. Shared tiles can be counted more
/// than once; this is a conservative cache allowance, not process memory usage.
pub fn cache_bytes() -> usize {
    cache().lock().unwrap_or_else(|e| e.into_inner()).bytes
}

/// Drop cached split surfaces (Edit > Purge > All). Returned bytes are accounted retention;
/// callers and GPU residents may still hold shared tiles.
pub fn purge_cache() -> usize {
    cache().lock().unwrap_or_else(|e| e.into_inner()).clear()
}

/// (fill only, stroke only) of a stroked shape, rendered over `canvas` in RGBA at `depth`.
/// `None` without a stroke. Where the shape's pixels
/// (Photoshop's rendering, `sh.cache`) reach past our fill, the part the fill doesn't explain is
/// stroke: the stroke follows Photoshop's coverage (psd-tools double-stroke-effects).
pub fn split(sh: &ShapeLayer, canvas: Rect, depth: SampleType) -> Option<(Surface, Surface)> {
    split_cached(sh, canvas, depth, cache())
}

fn split_cached(sh: &ShapeLayer, canvas: Rect, depth: SampleType, store: &Store) -> Option<(Surface, Surface)> {
    sh.stroke.as_ref()?;
    let mut h = std::collections::hash_map::DefaultHasher::new();
    (canvas.x0, canvas.y0, canvas.x1, canvas.y1).hash(&mut h);
    depth.hash(&mut h);
    format!("{:?}{:?}{:?}{:?}", sh.path, sh.fill, sh.stroke, sh.live).hash(&mut h);
    if let Some(c) = &sh.cache {
        format!("{:?}{:?}", c.format(), c.default_pixel()).hash(&mut h);
        for (k, t) in c.tiles() {
            (k.tx, k.ty, std::sync::Arc::as_ptr(t) as usize).hash(&mut h);
        }
    }
    let key = h.finish();
    let generation = {
        let mut c = store.lock().unwrap_or_else(|e| e.into_inner());
        if let Some(parts) = c.get(key) {
            return Some(parts);
        }
        c.generation
    };
    let fmt = PixelFormat::RGBA8.with_sample(depth);
    let fill_only = ShapeLayer { stroke: None, cache: None, ..sh.clone() };
    let stroke_only = ShapeLayer { fill: None, cache: None, ..sh.clone() };
    let mut parts = (photocraft_vector::render_shape(&fill_only, fmt, canvas), photocraft_vector::render_shape(&stroke_only, fmt, canvas));
    if let Some(cache) = &sh.cache {
        fit_stroke(&parts.0, &mut parts.1, cache, canvas);
    }
    let mut c = store.lock().unwrap_or_else(|e| e.into_inner());
    c.insert(key, parts.clone(), sh.cache.clone(), CACHE_BUDGET, generation);
    Some(parts)
}

/// Fits the stroke part to the shape's own pixels: where they reach past the fill, the stroke
/// covers what the fill doesn't (`(pixels - fill) / (1 - fill)`), in the pixels' colour where we
/// drew no stroke, and elsewhere in the colour that, drawn over the fill, gives back the pixels'
/// colour. Our stroke's own colour would be wrong where the file's fill covers more of the pixel
/// than ours (shapes snapped to whole pixels with a stroke thinner than a pixel): the fitted
/// stroke is then mostly the file's fill, and an edge drawn in the stroke's full colour is far
/// too dark.
fn fit_stroke(fill: &Surface, stroke: &mut Surface, cache: &Surface, canvas: Rect) {
    // Where either has pixels (the stroke may reach past the shape's pixels, and vice versa).
    let (cb, sb) = (crate::bounds::content_bounds(cache), crate::bounds::content_bounds(stroke));
    let r = if cb.is_empty() {
        sb
    } else if sb.is_empty() {
        cb
    } else {
        cb.union(&sb)
    }
    .intersect(&canvas);
    if r.is_empty() {
        return;
    }
    let n = r.width() as usize * r.height() as usize;
    let (mut f, mut s, mut c) = (vec![[0.0f32; 4]; n], vec![[0.0f32; 4]; n], vec![[0.0f32; 4]; n]);
    fill.read_rgba_into(r, &mut f);
    stroke.read_rgba_into(r, &mut s);
    cache.read_rgba_into(r, &mut c);
    let mut out = Vec::with_capacity(n * 4);
    let float = stroke.format().sample == SampleType::F32;
    for ((fp, sp), cp) in f.iter().zip(&s).zip(&c) {
        let mut p = *sp;
        if fp[3] < 1.0 - 1e-3 {
            let a = ((cp[3] - fp[3]) / (1.0 - fp[3])).clamp(0.0, 1.0);
            p = if sp[3] <= 0.0 {
                [cp[0], cp[1], cp[2], a]
            } else if a > 1e-3 {
                // Normal over the fill: a·p + f·(1 - a)·fill = pixels (premultiplied).
                let k = fp[3] * (1.0 - a);
                let un = |i: usize| {
                    let v = (cp[3] * cp[i] - k * fp[i]) / a;
                    // Float RGB retains HDR values; integer samples use the normalized range.
                    if float { v } else { v.clamp(0.0, 1.0) }
                };
                [un(0), un(1), un(2), a]
            } else {
                [sp[0], sp[1], sp[2], a]
            };
        }
        out.extend_from_slice(&p);
    }
    stroke.write_region(r, &out);
}

#[cfg(test)]
mod tests {
    use super::*;
    use photocraft_color::Color;
    use photocraft_doc::Fill;
    use photocraft_doc::vector::{Path, ShapeStroke, Subpath};
    use std::sync::Arc;

    fn shape(i: usize) -> ShapeLayer {
        let x = (i * 4 + 2) as f64;
        ShapeLayer {
            path: Path::new(vec![Subpath::polygon(&[(x, 8.0), (x + 3.0, 8.0), (x + 3.0, 12.0), (x, 12.0)])]),
            fill: Some(Fill::Solid(Color::WHITE)),
            stroke: Some(ShapeStroke { width: 1.0, ..Default::default() }),
            ..Default::default()
        }
    }

    #[test]
    fn thirty_three_unchanged_shapes_reuse_their_raster_tiles_at_each_depth() {
        for depth in [SampleType::U8, SampleType::U16, SampleType::F32] {
            let store = Mutex::new(Cache::default());
            let canvas = Rect::new(0, 0, 192, 32);
            let shapes: Vec<_> = (0..33).map(shape).collect();
            let first: Vec<_> = shapes.iter().map(|sh| split_cached(sh, canvas, depth, &store).unwrap()).collect();
            for (i, (sh, (fill, stroke))) in shapes.iter().zip(&first).enumerate() {
                let again = split_cached(sh, canvas, depth, &store).unwrap();
                assert!(
                    Arc::ptr_eq(fill.tiles().next().unwrap().1, again.0.tiles().next().unwrap().1),
                    "unchanged shape {i} at {depth:?} rebuilt its fill and would re-upload it"
                );
                assert!(
                    Arc::ptr_eq(stroke.tiles().next().unwrap().1, again.1.tiles().next().unwrap().1),
                    "unchanged shape {i} at {depth:?} rebuilt its stroke and would re-upload it"
                );
            }
        }
    }

    #[test]
    fn edited_shape_and_source_pixels_invalidate_cached_parts() {
        for depth in [SampleType::U8, SampleType::U16, SampleType::F32] {
            let store = Mutex::new(Cache::default());
            let canvas = Rect::new(0, 0, 32, 32);
            let mut sh = shape(0);
            sh.cache = Some(photocraft_vector::render_shape(&sh, PixelFormat::RGBA8.with_sample(depth), canvas));
            let old = split_cached(&sh, canvas, depth, &store).unwrap();
            sh.fill = Some(Fill::Solid(Color::BLACK));
            let changed = split_cached(&sh, canvas, depth, &store).unwrap();
            assert_ne!(old.0.rgba(3, 9), changed.0.rgba(3, 9));
            sh.cache.as_mut().unwrap().fill_rect(Rect::new(2, 8, 5, 12), &[1.0, 0.0, 0.0, 0.5]);
            let changed_pixels = split_cached(&sh, canvas, depth, &store).unwrap();
            assert!(!Arc::ptr_eq(changed.1.tiles().next().unwrap().1, changed_pixels.1.tiles().next().unwrap().1));
            let fresh = split_cached(&sh, canvas, depth, &Mutex::new(Cache::default())).unwrap();
            assert_eq!(changed_pixels.0, fresh.0);
            assert_eq!(changed_pixels.1, fresh.1);
            let outside = split_cached(&sh, Rect::new(16, 0, 32, 32), depth, &store).unwrap();
            assert_eq!(outside.0.tile_count(), 0, "canvas bounds are part of the cache key");
        }
    }

    #[test]
    fn cache_bounds_pixel_storage_pins_inputs_and_rejects_oversized_entries() {
        let mut source = Surface::new(PixelFormat::RGBA8);
        source.fill_rect(Rect::new(0, 0, 1, 1), &[1.0, 1.0, 1.0, 1.0]);
        let parts = (source.clone(), source.clone());
        let tile = source.tiles().next().unwrap().1.clone();
        let bytes = surface_bytes(&source) * 3;
        let mut cache = Cache::default();
        cache.insert(1, parts.clone(), Some(source.clone()), bytes * 2, 0);
        assert_eq!(cache.bytes, bytes);
        cache.insert(1, parts.clone(), Some(source.clone()), bytes * 2, 0);
        assert_eq!(cache.bytes, bytes, "replacing a raced insertion does not double count");
        cache.insert(2, parts.clone(), Some(source.clone()), bytes * 2, 0);
        assert!(cache.get(1).is_some());
        cache.insert(3, parts.clone(), Some(source.clone()), bytes * 2, 0);
        assert!(cache.get(2).is_none(), "byte pressure evicts the least recently used entry");
        assert_eq!(cache.bytes, bytes * 2);
        let refs = Arc::strong_count(&tile);
        cache.insert(4, parts.clone(), Some(source.clone()), bytes - 1, 0);
        assert!(cache.get(4).is_none(), "an oversized result is never retained");
        assert_eq!(Arc::strong_count(&tile), refs);
        let generation = cache.generation;
        assert_eq!(cache.clear(), bytes * 2);
        assert_eq!(cache.bytes, 0);
        assert!(cache.entries.is_empty());
        assert!(Arc::strong_count(&tile) < refs, "purge releases pinned tiles");
        cache.insert(5, parts, Some(source), bytes, generation);
        assert!(cache.entries.is_empty(), "pre-purge calculations cannot refill the cache");
    }

    #[test]
    fn cache_also_bounds_entry_count_and_survives_tick_saturation() {
        let parts = (Surface::new(PixelFormat::RGBA8), Surface::new(PixelFormat::RGBA8));
        let mut cache = Cache::default();
        for key in 0..CAPACITY as u64 {
            cache.insert(key, parts.clone(), None, CACHE_BUDGET, 0);
        }
        assert!(cache.get(0).is_some());
        cache.insert(CAPACITY as u64, parts.clone(), None, CACHE_BUDGET, 0);
        assert_eq!(cache.entries.len(), CAPACITY);
        assert!(cache.get(1).is_none());
        assert!(cache.get(0).is_some());
        cache.tick = u64::MAX;
        assert!(cache.get(0).is_some());
        cache.insert(999, parts, None, CACHE_BUDGET, 0);
        assert_eq!(cache.entries.len(), CAPACITY);
    }
}
