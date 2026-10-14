# PhotoCraft: user-first product revamp

Planning draft, 13 October 2026. Updated after reading the owner's 17-page improvement plan. This is a product and experience plan, not an implementation or delivery commitment. Visual directions below are proposals, not approved mockups. No product code was changed.

## Updated direction after the owner's plan

The primary goal is now novice success with sophisticated results: a beginner, including a 14-year-old, should learn useful creative workflows within one or two days. Adopt the owner's eight systems as the reliability and guidance foundation, and add outcome-led entry, editable creative recipes, image-aware defaults, contextual teaching and professional finishing checks.

Read [the merged conclusion](beginner-first-conclusion-2026-10-13.md) for the reconciled evidence, revised delivery order and measurable learnability goals. It takes precedence over the earlier provisional audience order and release sequence below where they differ. The original broad professional capability program remains the destination; not every specialist capability is a first-day learning promise.

## Product ambition

Make PhotoCraft a professional creative studio where photographers, retouchers, designers and painters can finish work confidently and enjoy the process. Give it its own identity, with the depth professionals expect and approachable ways to discover that depth.

Success means an artist can open real work, understand the canvas, make precise edits without distracting delays, explore alternatives, recover from mistakes, and deliver the right files. A beautiful screen alone does not achieve this. Feature counts alone do not achieve this either.

The owner's direction supersedes the repository's older Photoshop-layout target for this proposed revamp. Preserve professional capabilities, file exchange, useful terminology and optional familiar shortcuts; replace the default visual identity and information architecture. This plan does not rewrite the existing parity documents or claim that fidelity problems are resolved.

Work is organized by what users need. Internal refactoring and code-quality milestones are outside this plan. Rendering correctness, responsiveness, dependable saving and recovery remain product requirements because users experience their failures directly.

Updated audience priority: first-time visual creators, including teenage learners, lead the entry experience. Photographers/retouchers, designers and painters define the depth and output-quality requirements; they keep direct access to manual and precise tools. Animation and advanced generative work extend the product later rather than defining the first release.

## What the recorded baseline actually established

[Recorded results](live-feature-test-results-2026-10-11.md) retain 908 checks, all 65 tool activations and representative interactions, and 622 attempted menu rows. These are different levels of evidence, not 908 complete workflows.

| Evidence | Planning consequence |
|---|---|
| U16 partial-mip assertion failed again in isolation | Correct high-depth canvas previews before qualifying professional color work |
| Three GPU targets crashed in the workspace run; serial reruns passed | Investigate and qualify stability on real supported hardware; serial passing is not a repair |
| Eight format save/reopen cases passed | Keep the working paths; expand to external acceptance and feature preservation |
| Menus needed prepared contexts and explicit inputs | Improve input acquisition, disabled-state explanations and on-canvas affordances |
| Panels accumulated over the canvas in the broad walkthrough | Design workspace persistence and predictable tray behavior |
| PNG transparency and TGA named alpha passed; TGA export matched every RGBA byte independently | Preserve this behavior; do not create a fictional alpha-loss fix ticket from the initial harness mistake |
| A bounded 150-layer nudge/visibility case passed | Expand to larger representative documents; do not claim the original field crash is cleared |
| Many commands were refused by automation policy | Manual qualification is needed; policy refusal is not proof a feature is missing |
| Basic action replay on a fresh document passed | Deepen replay and recipe semantics; do not describe all cross-document actions as absent |

Reported lag in the source evaluation still needs fresh release measurements. The recordings used small fixtures, a debug build and four-frame-per-second capture; they cannot measure brush latency or qualify large-document speed.

## The user promises

1. **My work is safe.** Save state is truthful, recovery is understandable, and exports disclose losses before delivery.
2. **My hand leads.** Painting, dragging, panning, selecting and scrubbing feel immediate and predictable.
3. **I know what happens next.** A tool has visible controls, clear targets, preview, confirm/cancel and useful explanations.
4. **I can change my mind.** Edits remain editable where practical; history, masks, variations and comparisons are easy to use.
5. **The studio fits my task.** Tools and trays are accessible without surrounding the canvas with every feature at once.
6. **I can finish professional work.** Color, type, file exchange, assets, batch operations and delivery are complete workflows.

## Professional capability program

Each area needs discoverability, direct manipulation where appropriate, precise numeric control, meaningful preview, reversibility, persistence, keyboard access and a recorded realistic acceptance task. Existing implementations should be assessed and deepened before being replaced.

| Area | User-facing scope | Proof of completion |
|---|---|---|
| Documents and recovery | Reliable open/save, autosave, visible save state, crash recovery, version history, linked-file status, large documents | Recover an interrupted multi-layer edit; save and reopen without unexplained losses |
| Layers and compositing | Multi-select, groups, masks, clipping, locks, blending, effects, smart objects, live filters, links and layer search | Build and revise a layered composite without flattening the editable master |
| Selection and masking | Marquee/lasso modifiers, snapping, autoscroll, quick/object selection, channels, hair/fur refinement, edge decontamination, reusable masks | Cut out hair and translucent edges, inspect on several backgrounds, revise and export |
| Transform and geometry | Visible confirm/cancel, multi-layer transform, skew/perspective, accurate blend preview, warp grids, puppet pins, perspective planes | Position a product in perspective; reopen and revise the deformation |
| Retouching | Clone/heal/patch/remove, sampling overlays, protected regions, frequency-separation workflow, dodge/burn, content-aware controls | Retouch a portrait or product on editable layers with a clean before/after |
| Painting and pen input | Reliable pressure, device-dependent tilt/rotation, smoothing, stabilizers, textured/custom tips, brush preview, symmetry, mixer behavior, brush organization | Complete a real tablet session with deliberate slow strokes, fast strokes and large brushes |
| Color and grading | RGB/Gray/CMYK/Lab and depth workflows, ICC profiles, gamut warnings, curves, scopes, LUTs, local adjustments, proofing | Produce a calibrated print variant and web variant from one editable master |
| RAW and photographic assembly | Camera support matrix, lens corrections, white balance, highlight recovery, local masks, HDR/panorama/focus-stack workflows | Develop a real supported camera file and continue editing without an unexplained conversion |
| Typography | Font discovery/preview, paragraph styles, variable axes, OpenType, text on paths/shapes, live warp, multilingual shaping and missing-font handling | Create editable multilingual poster typography and a dependable delivery file |
| Vector and layout | Bezier editing and Convert Point, shape operations, strokes, guides, grids, artboards, alignment, constraints and reusable components | Build a multi-size campaign with consistent layout and editable paths |
| Formats and handoff | PSD/PSB acceptance, native files, layered TIFF, ORA, PDF/SVG workflows, modern raster formats, explicit format limitations | Open supported exports in an independent target app and verify named feature preservation |
| Export and print | JPEG controls, preview, DPI/ICC/alpha options, batch naming, bleed/safe zones, artboard/slice export, delivery presets | Deliver a print job and a social kit with correct sizes, colors, names and documented losses |
| Assets and reuse | Brushes, palettes, textures, patterns, fonts, styles, reusable layers, favorites, tags, licences and missing-asset repair | Move a project to another machine and identify or package its dependencies |
| Actions and recipes | Editable recording, cross-document targeting, parameters, validation, batch runs, cancellation and progress | Apply a retouch recipe to different-sized documents, revise a step and cancel safely |
| Animation and motion | Timeline, onion skin, frame/layer animation, loops, cinemagraphs and dependable video/GIF export | Export a short loop and reopen its editable source |
| AI assistance | Subject/sky/depth masks, generative fill/expand, reference style, relight and editable command assistance | Review a proposed change, protect chosen layers, accept a separate result and undo it |
| Accessibility and languages | Keyboard navigation, readable contrast, UI scale, reduced motion, screen-reader qualification, IME, Hindi/Arabic/Vietnamese and RTL | Complete a representative task with keyboard-only input and appropriate language hardware/input |
| Workspaces and ecosystem | Task layouts, persistent docks, multi-monitor workspaces, shortcuts, command search, presets and plugin capability disclosure | Restore a personalized workspace and find an unfamiliar tool without consulting code |

Specialist features such as HDR monitor output, spot-color separations, advanced RAW profiles, natural-media simulation and proprietary plugin compatibility have their own qualification requirements. They remain in the ambition; none is promised simply because a similarly named command exists.

External behavioral references help define task depth: Adobe documents hair refinement inside a [Select and Mask workspace](https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/make-improved-hair-selections.html); Affinity documents re-editable [live filters](https://s3-eu-west-1.amazonaws.com/affinity-docs/help/photo/en-US.lproj/pages/Layers/livefilters.html); Krita documents a [dynamic brush tool](https://docs.krita.org/en/reference_manual/tools/dyna.html?highlight=brush+smoothing). These are reference capabilities, not directions to copy their interfaces or evidence of PhotoCraft parity.

## Remove the friction users feel

Start with brush lag, preview errors, layer opacity/blend/visibility, move and transform, zoom/pan, large selections, type editing and opening/saving. Measure input-to-visible feedback on an idle release build; report median and slow-tail results, hardware, document content, depth, dimensions and cold/warm behavior. Do not substitute command dispatch time for perceived latency.

Initial acceptance targets below are proposed product budgets, not measured results or universal hardware guarantees. Validate them on a published supported-machine profile before adopting them.

| Interaction | Proposed target | User experience when work takes longer |
|---|---|---|
| Press, selection feedback and common controls | Visible acknowledgment within 50 ms at the 95th percentile | State changes immediately; no repeated-click ambiguity |
| Pan, zoom and transform while dragging | Sustain 60 fps on the reference workload, with no recurring stalls over 100 ms | Predictable preview quality and a clearly indicated refinement |
| Brush strokes | Proposed pen-to-visible target at or below 30 ms; qualify with physical input measurement | Preserve the stroke and keep cursor/ink feedback coherent |
| Opacity, blend and adjustment scrubbing | Preview within 100 ms at the 95th percentile | Show preview state; full-quality result settles after release |
| Selection edge controls and mask refinement | Preview within 150 ms on the reference workload | A clear updating indicator; retain the last valid preview |
| Long filters, imports and exports | Immediate acknowledgment and trustworthy progress | Cancel where safe, keep source intact, explain completion and errors |

Workload ladder: small onboarding image; 12–24 MP photograph with masks and adjustments; 150 populated layers with mixed effects; large 16/32-bit image; oversized PSB under a published memory limit. Layer count alone is insufficient. Exact documents, hardware and thresholds are fixed before qualification, not adjusted after a failing run.

Preview speed cannot trade away color, alpha, brush placement or final export quality. A refining preview is acceptable when disclosed; silently showing a wrong image is not. Avoid claiming to remove every lag before the measurements exist.

## A distinct visual identity

Recommended direction: **Atelier**, a precise contemporary artist's studio. The artwork dominates; the interface feels composed, tactile and deliberate. Use warm graphite for outer chrome, neutral image-viewing surrounds, a restrained copper accent for primary interactions, clear typography and refined tool silhouettes. A light studio variant should feel like clean archival paper. Keep simulated paper grain and decorative color out of image inspection and color judgments.

This is a replacement visual world. Change the silhouette, hierarchy, panel grammar, tool discovery and working rhythm together. Recoloring the existing dock stack would not deliver the requested revamp.

Two alternatives remain available before visual prototyping: **Gallery**, a very quiet editorial canvas with a separate asset shelf; **Instrument**, a compact precision desk for dense expert controls. Atelier is the proposed lead because it accommodates painting, photo work and design without turning the whole product into a gallery or a technical console. All three need a usable task demonstration, not just a mood board.

Design principles:

- Give the canvas a single strong focal position and generous working room.
- Use flat, calm surfaces, carefully placed separators and consistent control shapes. Avoid ornamental glow, glass, excessive rounding and decorative dashboard cards around artwork.
- Keep dense numeric controls legible and aligned; use exact values alongside visual controls.
- Keep brand expression in the project home, asset presentation, selection details and restrained motion. Neutralize it near color-critical inspection.
- Offer comfortable and compact density, scalable text and controls, high contrast and reduced motion.
- Label unfamiliar tools and make their state visible. A beautiful icon is insufficient instruction.

## Proposed editor structure

The editor is an **Operate** surface: a person is completing creative work. The project gallery is an **Experience** surface; it can be more expressive without slowing editing.

```text
 PROJECT / DOCUMENTS      Search commands      Workspace      Save / Deliver
 --------------------------------------------------------------------------
 TOOLS       Active tool controls + target + preview + confirm/cancel
             --------------------------------------------------------------
             |                                            | INSPECTOR     |
             |                                            | Layers        |
             |             WORKING CANVAS                 | Properties    |
             |                                            | pinned tray   |
             |                                            |               |
             --------------------------------------------------------------
             TRAY SHELF: References · Assets · Looks · Materials · Variations
             HISTORY / COMPARISON / BACKGROUND TASK STATUS
```

This is a spatial proposal, not a rendered final design. At narrow laptop widths the lower tray becomes an overlay drawer with a reserved canvas area; at wide widths it can sit beside the canvas. Panels can be resized, collapsed, pinned or moved to another monitor. Opening a drawer must not hide the selected handle or text caret. Workspace changes retain document state.

Use one stable tool rail, one contextual control band, one main inspector, and optional trays. Keep Layers persistently reachable during editing. The default workspace opens at most two expanded inspector sections and one lower tray; users can override this. Added tray categories do not all become permanent visible panels.

Task presets: **Photo**, **Retouch**, **Paint**, **Design**, **Print**, and eventually **Motion**. Presets alter layout and useful defaults, not the availability of the document's tools. Search and shortcuts work across presets. Offer a visible workspace reset and remember per-user choices.

## Feature trays

| Tray | What the user finds | Direct action |
|---|---|---|
| References | Pinned images, moodboards, notes, palettes | Sample a color or pin a crop beside the canvas without exporting it |
| Assets | Cutouts, shapes, linked files, reusable components | Drag into the document; inspect licence and dependency status |
| Brushes | Preset groups, tip previews, pressure curve, stabilization | Test a brush in a scratch area before painting |
| Materials | Paper, canvas, pigment, grain, texture interaction | Apply a material as an editable layer or brush interaction |
| Color | Harmony wheel, image palette, numeric sliders, scopes | Choose a color precisely or establish a coordinated palette |
| Looks | Film grades, LUTs, recipes, before/after previews | Preview on the current artwork and apply as editable adjustments |
| Masks | Saved selections, masks, edge views, protected regions | Refine or reuse a mask with explicit output choice |
| Retouch | Clone/heal sampling, remove, frequency tools, dodge/burn | Work on separate layers with sampling and protected-region overlays |
| Type and layout | Font previews, paragraph styles, path type, grids, artboards | Preview the actual selected text, then apply a style or layout rule |
| Variations | Named alternatives, snapshots, side-by-side comparison | Compare, keep a branch or restore a milestone |
| Recipes | Editable actions, step parameters, batch targets | Preview affected layers and run a validated recipe |
| Delivery | Output presets, artboards, color/alpha checks, format warnings | Inspect a proof and export a named deliverable set |

Every tray needs empty, loading, selected, incompatible, missing-asset, failed and completed states. Show meaningful thumbnails, names, searchable tags and favorites. Do not make hover the only way to understand a control. Drag actions also need keyboard/menu alternatives.

Context may suggest the next tray, but never silently replace a pinned inspector or steal the user's tool. Users can close suggestions, keep their workspace fixed and use compact expert controls.

## Redesign the difficult workflows

**Selection Studio:** enter with the current selection or an explicit target. Preview edges on white, black, overlay and transparency. Provide a refine brush, edge controls, protected areas and named-mask output. Show exactly whether Apply modifies a mask, creates a masked layer or replaces a selection.

**Retouch Studio:** keep source and retouch layers visible, show the sampling region and exclusions on canvas, let users brush corrections and compare results. A slow operation has progress and cancellation; it must not leave uncertainty about what changed.

**Transform Studio:** keep handles, pivot, snap state and original footprint visible. Show position, size, angle and skew beside on-canvas controls. Apply/Cancel stay reachable. Warp and puppet pin editing occur over the artwork with reversible, named changes.

**Type Studio:** select text on canvas and preview fonts on that actual content. Separate common typography from advanced settings without hiding the latter. Surface missing fonts and unsupported glyphs before export. Include Devanagari and Arabic tasks in qualification.

**Delivery Studio:** choose the job first: editable master, web image, print, social kit or motion. Show dimensions, color profile, transparency, text treatment and lost editable features before confirming. Keep the source master separate from delivery variants and make saved/exported status unambiguous.

First-run flow: create or open work, select an optional task preset, complete one useful edit, compare it, and save. Contextual tips explain the current task and disappear when dismissed. Experienced users can skip onboarding completely.

## Artistic capabilities that create a reason to choose PhotoCraft

Start with a coherent set rather than unrelated novelty filters:

| Feature | Artist benefit | First useful version |
|---|---|---|
| Reference Desk | Keep inspiration next to the work | Pinned references, sampling, notes and linked attribution |
| Palette from Anything | Establish the color story quickly | Extract a palette, edit its harmony and apply it to adjustments |
| Print Lab | Make distinctive graphic artwork | Risograph, halftone, engraving and ink-separation recipes with proof views |
| Material Library | Give work physical character | Editable paper/canvas grain and brush-material presets |
| Idea Branches | Explore without losing a good version | Named branches, comparisons and deliberate keep/restore actions |
| Paint Replay | Share the making process | Export a replay with milestones, pause and output controls |
| Creative Recipes | Repeat a look while keeping control | Named editable steps with reusable parameters and target validation |
| Texture Workshop | Turn artwork into usable patterns | Seam preview, wrap-around painting and repeat variations |
| Typography Art | Make lettering part of the image | Type on paths/shapes and editable text compositions |
| Light Painting | Shape mood without destructive retouch | Brush controlled exposure, rim light and haze on masked adjustments |

Larger explorations: living watercolor, impasto, pigment mixing, flow-field brushes, procedural layers, relighting, sketch-to-image and semantic masks. Keep a research lane for these; do not let their novelty delay dependable professional delivery.

AI belongs behind explicit user intent. Show proposed changes and target layers, preserve originals, label generated results, offer variations, and disclose remote processing/cost where applicable. An AI assistant must not silently flatten, upload or overwrite the artist's work. Offline manual editing remains a complete path.

## Release sequence and acceptance gates

Design exploration and workflow prototypes can start while reliability work proceeds. Shipping the new shell must preserve working capabilities; professional release claims wait for the relevant acceptance gates.

| Stage | Outcome visible to users | Exit gate |
|---|---|---|
| 0. Establish the truth | A ranked list of reproduced defects and uncovered tasks | Retain current recordings; distinguish policy limits, harness errors, historical reports and product defects |
| 1. Trust and responsiveness | Correct previews, safe files, predictable everyday interactions | Reproduced GPU failures addressed and recorded; recovery/save tests; measured reference-workload budgets |
| 2. Daily editing depth | Better masks, brush feel, transforms, layers and type | Realistic editing tasks completed with revisable outputs; physical tablet qualification |
| 3. New studio shell | A distinct, aesthetic editor with coherent tray behavior | Compare candidate designs on the same tasks; keyboard, scale and narrow-window usability; no lost working workflows |
| 4. Professional delivery | Dependable exchange, color, RAW, print and batch | Independent file acceptance; supported-camera tasks; calibrated output and batch cancellation checks |
| 5. Artistic identity | Reference, palette, material, print and variation tools form a connected workflow | Complete a finished piece and its deliverables using the new creative features |
| 6. Advanced studio | Deeper natural media, AI, motion, collaboration and ecosystem | Separate quality, hardware, service and interoperability qualification for each capability |

Prioritize each ticket by frequency of use, cost of failure, number of workflows unlocked, friction removed and distinct creative value. Save/render failures outrank cosmetic details; daily friction outranks rarely used breadth. This is a product priority order, not an engineering effort estimate. Dates follow measured scope and the merged beginner-first conclusion.

First candidate implementation batch after task-level planning: investigate the U16 preview failure and native GPU crashes; make save/recovery state dependable; measure common editing latency; add visible transform Apply/Cancel and input guidance; prototype the new shell on selection, retouch and design tasks. Track these as independent deliverables so design discovery can progress without pretending the failures are already fixed.

## The tasks that qualify the product

Record a professional task suite with realistic licensed or synthetic assets, not only isolated menu clicks:

1. Develop a supported RAW portrait and produce a reusable grade.
2. Retouch a portrait on separate layers, preserving skin detail.
3. Cut out hair, fur and translucent material and inspect the result on multiple backgrounds.
4. Composite a product into a scene with perspective, masks and matching light.
5. Edit a layered PSD received from an independent app and return an accepted editable file.
6. Create a multilingual poster with paths, images and editable typography.
7. Paint with a real tablet, including pressure ramps and stabilization comparisons.
8. Build a consistent multi-artboard social campaign and export its delivery set.
9. Proof a print image, inspect gamut and export with the intended ICC profile.
10. Replay a parameterized recipe across several documents; cancel a batch safely.
11. Recover interrupted work and resolve a missing linked asset or font.
12. Continue editing a large high-depth document through common layer and canvas operations.
13. Use References, Palette, Material and Print Lab to create a finished artistic piece.
14. Complete a core task with keyboard-only navigation and enlarged UI text.
15. Compare branches, restore a milestone and export a process edition.

Split these into 30–50 acceptance scenarios with destructive/non-destructive variants, empty/error states, supported formats and representative hardware. Review the actual artwork and saved outputs as well as machine assertions. The recorded suite must expose incomplete cases rather than calling them passed because a dialog opened.

## Recordkeeping and merging the owner's plan

The companion [feature backlog](revamp-feature-backlog-2026-10-13.csv) is the initial product ledger. Rows are proposals, not a claim of absent capabilities or completed implementation. The owner's eight systems are mapped onto existing rows, with beginner-success deliverables added. Retain intent and flag conflicts in priority or behavior as requirements develop. Give each accepted item a user outcome, current evidence, acceptance task and delivery stage.

For subsequent work retain: issue and reason, before recording, changed behavior, after recording on the same task, sample outputs, measured responsiveness where relevant, remaining boundaries and any migration notes. Keep the original baseline archive intact; each new run gets a fresh evidence directory. Record UI-affecting work in video and screenshots; record planning and background checks in documents/logs. Never claim that a planning session itself produced new UI footage.

Open decisions for the owner's plan: audience order; chosen visual direction; minimum supported hardware; must-have camera/format matrix; offline/local versus optional cloud AI; priority artistic features; and the professional beta acceptance set. The audience direction is settled by the latest owner request; the remaining implementation choices do not prevent delivering this planning draft. No implementation estimate or finished redesign is implied.
