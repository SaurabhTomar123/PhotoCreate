//! Cache reuse must preserve the vector renderer's pixels after live geometry/stroke edits.

use photocraft_color::{Color, PixelFormat, SampleType};
use photocraft_doc::Fill;
use photocraft_doc::vector::{Path, ShapeLayer, ShapeStroke, Subpath};
use photocraft_geom::Rect;
use std::sync::Arc;

fn path(x: f64) -> Path {
    Path::new(vec![Subpath::polygon(&[(x, 4.0), (x + 6.0, 4.0), (x + 6.0, 10.0), (x, 10.0)])])
}

#[test]
fn split_cache_tracks_geometry_stroke_and_canvas_at_all_depths() {
    for depth in [SampleType::U8, SampleType::U16, SampleType::F32] {
        let canvas = Rect::new(0, 0, 32, 16);
        let mut sh = ShapeLayer {
            path: path(2.0),
            fill: Some(Fill::Solid(Color::WHITE)),
            stroke: Some(ShapeStroke { width: 1.0, ..Default::default() }),
            ..Default::default()
        };
        let first = photocraft_compose::shape_split::split(&sh, canvas, depth).unwrap();
        let again = photocraft_compose::shape_split::split(&sh, canvas, depth).unwrap();
        assert!(Arc::ptr_eq(first.0.tiles().next().unwrap().1, again.0.tiles().next().unwrap().1));
        sh.path = path(18.0);
        let moved = photocraft_compose::shape_split::split(&sh, canvas, depth).unwrap();
        assert_eq!(moved.0.rgba(3, 6)[3], 0.0, "old geometry must disappear");
        assert_eq!(moved.0.rgba(20, 6), [1.0; 4], "new geometry must appear");
        sh.stroke.as_mut().unwrap().width = 3.0;
        let thicker = photocraft_compose::shape_split::split(&sh, canvas, depth).unwrap();
        assert_ne!(moved.1, thicker.1, "stroke settings invalidate the split");
        let fmt = PixelFormat::RGBA8.with_sample(depth);
        let fill_only = ShapeLayer { stroke: None, ..sh.clone() };
        let stroke_only = ShapeLayer { fill: None, ..sh.clone() };
        assert_eq!(thicker.0, photocraft_vector::render_shape(&fill_only, fmt, canvas));
        assert_eq!(thicker.1, photocraft_vector::render_shape(&stroke_only, fmt, canvas));
        let cropped = photocraft_compose::shape_split::split(&sh, Rect::new(0, 0, 10, 16), depth).unwrap();
        assert_eq!((cropped.0.tile_count(), cropped.1.tile_count()), (0, 0));
    }
}
