# Editorial poster: command and API map (Claude L1/L2 input)

15 October 2026. Every command and API below was read from source or exercised; nothing is assumed. Companion to the [workflow specification](claude-editorial-poster-spec.md). Evidence: [records/2026-10-15/claude-editorial-poster](../records/2026-10-15/claude-editorial-poster/).

## 1. Versions checked

| Source | Commit | Use |
|---|---|---|
| PhotoCreate `main` (this branch's base) | `388a0077` (upstream `ed7df56` + preserved fixes) | Source reading |
| Official `photocraft-cli` 0.9.0, signed Windows x64 | `c699e3cda` (2 commits after `ed7df56`; ancestor of `df055f3`) | Registry dump (`commands --json`, 909 commands) and headless runs |
| Upstream candidate | `df055f3d` (174 commits after 0.9.0) | Diffed for the commands below |

Between 0.9.0 and `df055f3` no parameter documentation of the commands below changed. Two behaviour changes matter: `3ee78a36`/`45f8921a` make Free Transform's frame the **selection's bounds** when a selection exists, and `47cf5af9`/`dbfe8ba4` change history memory accounting. `History::purge_last`, `set_current_label`, `past_len` and `record` are unchanged in `df055f3`. Re-check this map against the qualified base Codex pins before L3 code depends on it.

## 2. Commands the recipe uses

Precondition = the registry's `disabledReason` with no document, plus what was observed. All rows were exercised in the prototypes except where marked.

| Recipe step | Command | Parameters used | Returns | Precondition / observed behaviour |
|---|---|---|---|---|
| New poster document | `file.new` | `width`, `height`, `background` (`#rrggbb`), `resolution`, `name` | — | Always enabled. |
| Frame / colour block / rule | `shape.create` | `kind` (`rect`, `line`), `rect` or `from`/`to`/`weight`, `fill`, `name` | `layer` id, `bounds`, live geometry | Needs a document. |
| Place photo | `file.placeEmbedded` | `path`, `smartObject: true`, `fit: true` | `layer` id, `bounds`, `scale` (%) | Needs a document. **Reads the file system**: must run before any rollback scope and is refused by the automation policy; the UI calls it with a user-chosen path. |
| Cover-scale and position photo | `edit.transform` | `scaleX`, `scaleY`, `dx`, `dy` (relative); `rect` recommended | `rect` | "no active layer" without one. In `df055f3` an active selection becomes the frame: pass `rect` or deselect first. |
| Clip / rename / opacity / blend | `layer.setProps` | `clipped`, `name`, `opacity` (0..1), `blend` | `null` | **Silent no-op found:** `clipped: true` on the bottom layer returns `null` with no error. Readiness must check there is a layer below. |
| Duotone | `layer.newAdjustmentLayer.gradientMap` | `stops` `[[t,"#hex"],…]` | — | Needs a document. |
| Black and white | `layer.newAdjustmentLayer.blackWhite` | `{}` | — | Needs a document. |
| Shade for text | `layer.newFillLayer.gradient` | `from`, `to`, `angle`, `style` | — | Needs a document; no alpha stops, so legibility shade uses Multiply over white→black. |
| Title, subtitle, credit | `type.create` | `x`, `y` (baseline), `text`, `font`, `size` (pt), `color`, `align`, `name` | `layer` id, `bounds` | Needs a document. **Missing font:** succeeds, renders a fallback face, keeps the requested name, and returns `warnings: ["font '…' is not installed; …"]`. |
| Fit title to width | `type.info` → `type.setStyle` | `layer`, `size` | `lines[].x0/x1`, `bounds` | Not yet exercised for fitting; `type.info` line extents confirmed. |
| Resolve fonts | `type.fonts` | `{}` | `families` (214 on the test machine) | Includes installed system fonts; only Inter/JetBrains Mono are bundled. |
| Contrast check (finishing) | `document.sampleColor` | `x`, `y`, `size`, `sampleLayer` | `[r,g,b,a]` | Not yet exercised. |
| Select result layer | `layer.select` | `layer`, `mode` | — | Not yet exercised. |
| Undo whole poster | `history.undo` / `edit.undo` | — | — | Needs the fold in §5 to be one step. |

Commands considered and left out of the first recipe: `select.subject` (classical, slower, not needed for these layouts), `layer.smartObjects.warp`, `layer.layerStyle.*` effects, `layer.new.groupFromLayers` (grouping may be added once layer targeting in the tray is designed).

## 3. Observed facts the design depends on

1. **One history step per command.** `file.new` + 3 commands gave history `["Open","New Layer","New Layer","Layer Properties"]`. A 9–14 command poster therefore needs folding (§5).
2. **Missing fonts warn, don't fail** (above). The recipe resolves the fallback chain first so the warning never appears unexplained.
3. **Silent no-op** for clipping the bottom layer (above).
4. **Placement returns its own scale and bounds**, so cover-scaling can be computed exactly: for a frame `F` and placed bounds `P`, scale% = `100 × max(F.w/P.w, F.h/P.h)`, then translate the centre to the focus point inside `F`.
5. **The registry documents every parameter** but as free text (`params` string). L2 metadata must be checked against this text and behaviour, not invented.

## 4. Readiness predicates for this recipe only (L2 scope)

Bounded to the commands in §2. Each predicate is evaluated with `Session::disabled_reason_with(id, params)` (the engine's real precondition, with the actual parameters) immediately before each step, plus the recipe-specific checks below that the engine does not make. Commands outside this list are reported as "not supported by guidance", never guessed.

| Predicate | Checked how | Message if unmet | Preparation offered |
|---|---|---|---|
| Photo available | File decodes (open/peek) or the open document has pixels | "Add a photo to see your poster" | Use open photo / Choose a photo |
| Title present | Non-empty after trimming | "Add a title" | Focus field |
| Font installed | Name in `type.fonts` | "Title font: X (Y isn't installed)" | Choose installed font |
| Layer below exists (for clipping) | Target layer is not the bottom layer | (internal error, never user-facing) | Recipe order guarantees it; checked anyway |
| No selection before transform | Explicit `rect` on every `edit.transform` (or `select.deselect` first) | (internal) | Always pass `rect` |
| Engine precondition | `disabled_reason_with(id, params)` is `None` | The engine's reason, in plain words | Abort before any change |

## 5. One-step apply and rollback: reuse the existing compound-command pattern

No new engine transaction API is needed for this recipe. `frame_cmds.rs::frame_from_layers` already runs sub-commands through `Session::execute`, folds them into one history step with `History::purge_last()`, and on error undoes, truncates the journal and clears redo. The recipe follows that pattern as an ordinary engine command in a **new module**:

- `recipe.editorialPoster.apply` (name to agree): validates all inputs and predicates first; creates the new document with `file.new`; places the photo; runs the remaining steps through `s.execute`; on success calls `purge_last()` until one step remains and `set_current_label("Editorial poster (Gallery)")`.
- **On any error:** close the new, unsaved document (`Session::close`), so nothing is left behind. Because the poster is always a new document, rollback never touches the user's existing work.
- **Journal:** `after_command` truncates nested entries when the outer command is replayable, so the recipe records as one Actions step once it is listed in `actions_cmds::replayable`.
- **Risks to test:** history trimming by `max_states` (default 50) and the memory budget (`47cf5af9`) must not drop the pre-recipe state mid-run; background jobs started by a step (none in this recipe as mapped) would need waiting or refusal.

## 6. Shared-file patches Codex would apply (none applied here)

Per the work plan, Claude does not edit these files. Expected small patches when L3 lands:

| File | Change |
|---|---|
| `crates/engine/src/commands.rs` | One line in the `v.extend(...)` list: `crate::recipe_cmds::specs()` |
| `crates/engine/src/lib.rs` | `mod recipe_cmds;` |
| `crates/engine/src/actions_cmds.rs` | Add the recipe id to `replayable` (if Actions recording is wanted) |
| `crates/ui-egui/src/lib.rs`, `state.rs`, `menus.rs` | Tray module declaration, tray open/closed state, a menu/palette entry |
| `docs/parity-checklist.md` / scorecard | Regenerated by `cargo xtask parity` / `scorecard` if the new command appears in menus |
