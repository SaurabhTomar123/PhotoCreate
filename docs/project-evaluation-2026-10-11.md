# PhotoCraft project evaluation

Runtime follow-up: [recorded feature baseline and completed test results](live-feature-test-results-2026-10-11.md). The source review below preserves the assessment made before building; use the follow-up for measured execution results.

Reviewed 11 October 2026. Checkout: `d45b371`; workspace version: **0.7.0**.

## Verdict

**PhotoCraft is a substantial, ambitious alpha with the architecture of a real editor. It is not yet demonstrated to be a dependable replacement for Photoshop in paid production.** Its best foundations are an independent command engine, a capable document model, CPU/GPU rendering, native Rust desktop and browser clients, and unusually broad automation. Its greatest remaining risk is the distance between a feature being present and a complete workflow being predictable, responsive, editable, and exchangeable with other software.

The existing assessment reports approximately **76% feature breadth and 40–50% professional readiness**, with approximately 61% readiness for essentials users. These are the project's weighted estimates for an older 0.6.0 snapshot, not fresh measurements by this review. Recent code has advanced beyond several entries. I would retain **alpha** as the defensible stage, retire stale counts, and avoid publishing a new percentage until workflow acceptance and clean-machine benchmarks support it.

Recommended positioning now: **an offline, open-source layered editor for experimentation, personal projects, and controlled pilot workflows**. A professional can evaluate it on copies of work; the evidence does not yet establish it as the sole editor for client PSD exchange, demanding print production, or sustained tablet painting.

## Evidence and limits

This review inspected architecture and parity documentation, manifests, CI workflows, scorecard sources, representative engine/UI/format/security implementations, and test code. Three committed screenshots were visually inspected: the dark editing canvas, typography workspace, and light export dialog. Their layouts agree with the current Pro/Studio theme concepts, but their exact rendering freshness is not established; they are illustrations, not screenshots of this checkout running.

Evidence labels below:

- **Source:** directly inspected implementation or configuration.
- **Recorded:** committed results, floors, scorecard claims, or documented user reports; not reproduced here.
- **Visual:** observations from the committed screenshots.
- **Proposal:** recommended capability or acceptance criterion, not an existing defect.

**Runtime verification was blocked before compilation.** `cargo` and `rustc` were absent from PATH. Direct execution of `C:\Users\Saurabh\.cargo\bin\rustup.exe show` found no installed or active toolchain. Direct `cargo test -p photocraft-geom --lib --locked --offline` failed because rustup could not select a toolchain. There is no `target/` or `corpus/` in this checkout. No tests passed or failed at the application level in this session; no fresh GPU, startup, brush-feel, recovery, or Photoshop re-open result is claimed.

The Impeccable context launcher was attempted and could not load its engine because its cache was unavailable. UI evaluation therefore uses manual source and screenshot evidence. This is a general project audit, not a completed formal dual-assessor Impeccable critique. No running app or independent Adobe installation was available. The private sibling `craftrules` repository referenced by AGENTS.md is absent.

This is a broad, representative assessment, not proof that every defect in approximately a thousand source files has been discovered. Historical issue counts are not current live issue counts.

## What is already strong

| Foundation | Evidence | Why it matters |
|---|---|---|
| Engine separated from UI | `docs/architecture.md`, `crates/engine`, dependency layering configuration | Editing behavior can be tested and automated without rebuilding a second implementation for each frontend. |
| Rich document model | `crates/doc`; layers, masks, adjustments, effects, smart objects, text and vector data | The project starts with structures professional workflows need. |
| CPU reference and GPU renderer | `crates/compose`, `crates/gpu`; dedicated rendered-canvas tests | An independent reference makes renderer discrepancies diagnosable. |
| Copy-on-write tiled storage | Raster/document architecture | Useful foundation for history and background snapshots; does not itself prove low latency or low peak memory. |
| Non-destructive editing primitives | Smart-filter mapping, adjustment commands, layer styles | Strong basis for iterative creative work, though interoperability and interaction depth remain uneven. |
| Automation | CLI, JSON control and MCP share engine commands | A distinctive foundation for repeatable editing and future assistants. It does not prove every GUI gesture has equivalent headless semantics. |
| Save integrity | Atomic-save implementation and failure-injection tests | Reduces the risk of a partial overwrite destroying an existing file. |
| Test breadth | Static scan: 1,126 `.rs` files and 6,269 `#[test]` occurrences under crates/apps/xtask | Considerable testing effort; occurrences are not executable test totals, coverage, or pass rates. |
| Accessibility/theming groundwork | AccessKit enabled; 12 theme variants and contrast tests | The groundwork exists. Actual screen-reader usability and whole-interface contrast still need verification. |
| Real-file oracles | Pinned corpora, sha256 manifests and rendering comparisons | Stronger evidence than synthetic round trips alone. |

## Reporting problems that change the assessment

These should be corrected before using the roadmap to choose work or make public claims.

| Finding | Current evidence | Correction |
|---|---|---|
| Version drift | Workspace is 0.7.0; headline assessment describes 0.6.0 | Stamp all quantitative assessments with commit, version, date and measurement method. |
| Tool counts disagree | README says 15 missing; other docs say 53/56/58 present; `Tool::ALL` currently contains 65 variants, also represented in the toolbar groups | Regenerate a tool-by-tool behavior matrix. 65 definitions do not establish 65 finished Photoshop-equivalent tools. Color Sampler, Art History Brush and a dedicated Convert Point variant are absent from the enum; modifier behavior is a separate question. |
| Menu counts disagree | Older roadmap 628/628; current generated scorecard 630/630 | Treat this as catalog wiring coverage, never overall product completeness. The project's catalog is not independent proof of Photoshop's entire current command surface. |
| Preferences counts disagree | Roadmap 46/149 unread; current scorecard 32/154 | A static unread-field audit is a useful signal, not proof that every counted preference is visibly broken or every read preference works. Verify behavior individually. |
| Corpus denominator is stale | Scorecard reports round-trip floor 258/256; current manifest contains 258 PSD entries and pin description says 258 | The numerator is not evidence of an impossible test gate: the documented denominator is outdated. Derive counts from the manifest. Current oracle floor 133 against 258 files is approximately 51.6%, not a newly measured pass rate. |
| Completed work remains listed missing | Current code includes long-press flyouts, Color Replacement, anchor tools, four Pro brightness levels, Windows ARM64 release configuration, Warp Text preview tests and pre-transform locked-layer refusal | Move these from missing to implemented/needs validation. Manual and optical kerning are already marked done in the newer type scorecard. |
| RAW documentation lags code | `raw/src/sensor.rs` decodes baseline JPEG DNG compression 34892 for supported sample layouts | Limited lossy DNG support exists; camera/sample coverage still needs proof. Do not claim universal lossy DNG support. |
| Signing promises exceed configuration guarantees | README states Windows executables are signed; release workflow explicitly permits missing secrets and unsigned artifacts | Describe signing as artifact-specific and verify released signatures before claiming it. ARM64 configuration likewise does not establish that a particular release artifact passed. |

## Failure and gap register

Priority means impact on professional adoption: **P0** workflow/data-loss or crash release blocker; **P1** major working limitation; **P2** narrower workflow or usability issue; **P3** polish. Recorded P0 candidates need reproduction on this checkout before being called current confirmed failures.

| ID | Priority | Failure or gap | Evidence and practical effect | Recommended action |
|---|---|---|---|---|
| F01 | P0 candidate | PSD exchange not sufficiently established | Recorded export refusal/corruption reports in `docs/gaps.md`; FILE-216-4 still lacks a systematic external-editor re-open gate | Test PhotoCraft-created and edited PSD/PSB files in actual Photoshop, then edit and save back. Check appearance and editable structure. |
| F02 | P0 candidate | Complex-document GPU failure | Committed P12 baseline records an invalid compositor buffer during 150-layer nudge | Reproduce on current code and several adapters; test device loss and recoverable failure while retaining document state. |
| F03 | P1 | Historical interactive performance far above targets | See performance table below; baseline is old and heavily contaminated by machine load | Rebenchmark in release on a quiet machine; profile dirty-region updates, composition, effects, uploads and allocations. |
| F04 | P1 | Visual parity still incomplete | IO oracle floor 133/258 Photoshop fixtures; 236/309 psd-tools fixtures | Publish actual results by effects, type, mode/depth, smart filters and masks. Fix the largest common-workflow discrepancies. |
| F05 | P1 | Select and Mask lacks the full interactive workspace | Source: menu opens the `select.refineEdge` filter dialog (`menus.rs:465`) | Build an edge-refinement workspace with meaningful background views, brush refinement, before/after and explicit output choices. |
| F06 | P1 | Smart-object/filter workflow has partial fidelity and interaction | File scorecard: partial filter mapping, simple filter rows, missing directly paintable filter masks and non-affine smart-object perspective | Complete mask targeting, reorder/blend/context actions, transform model and verified PSD mapping. Clearly warn about unsupported export state. |
| F07 | P1 | Tablet painting quality is not established | Recorded pressure, latency, falloff and smoothing differences; OS-specific pen limitations | Use instrumented strokes plus real artists on Wacom/Huion/XP-Pen across Windows, macOS, X11 and Wayland. |
| F08 | P1 | Typography depth incomplete | Source: `TextShape` supports Point/Box only; scorecard has missing path text/direction UI and partial variable/OpenType UI | Add editable path text, predictable mixed-direction editing, exposed font axes and script-specific tests. Preserve font information across saves. |
| F09 | P1 | Performance/test gates miss important conditions | Ignored panic_hunt; GPU harness can silently return; large fixtures outside normal CI | Make gate execution explicit and distinguish pass, skip, unsupported and failure. |
| F10 | P1 | Allocation/resource exhaustion coverage incomplete | Reliability scorecard: codec internals and injected allocator failure remain partial | Test bounded decoding and failed allocation at import, effect, preview and save boundaries; keep original state intact. |
| F11 | P1 | Professional RAW workflow incomplete | Source: CR3 detected but rejected; recorded gaps in sidecars, lens profiles and camera-specific coverage | Prioritize cameras by user demand; build per-camera references and a reversible RAW-settings workflow. |
| F12 | P1 | Print and document interchange incomplete | File scorecard: Photoshop/vector/text PDF, multi-page output and spot-plate export missing; layered TIFF extra channels partial | Add explicit output preflight and focus on a small verified print workflow before promising broad prepress readiness. |
| F13 | P1 | Actions may not generalize between documents | Automation scorecard: document-independent recording and cross-document replay coverage missing | Normalize layer/selection targets; replay on documents with different IDs, dimensions and layer trees. |
| F14 | P1 | Important preferences may have no effect | Current static scorecard identifies 32/154 fields unread | Hide unavailable controls or explain limits; add restart-and-observe checks for supported settings. |
| F15 | P2 | Workspace flexibility incomplete | UI scorecard: floating dock groups and OS-window tear-off missing; persistent tool/export settings partial | Support focused presets, reliable restart persistence and multiple-monitor layouts. |
| F16 | P2 | Photoshop ecosystem incompatibility | No .8BF/UXP/CEP compatibility; custom WASM ABI remains filter-oriented | Invest in a documented native PhotoCraft plugin ecosystem first; scope proprietary compatibility separately. |
| F17 | P2 | Asset-library workflow absent | FILE-215-21: presets exist, reusable linked images/layers library missing | Add local project assets with linked/copy semantics, relink, missing-file reporting and portable packaging. |
| F18 | P2 | AI functionality is mostly classical substitutes | No ML runtime; Remove and subject/sky operations do not establish semantic generative capability | Keep classical tools honest; prototype optional licensed local inference and reversible output. |
| F19 | P2 | Missing/narrow format support | Documented PDF, AVIF decode, JXL/JP2 and specialist formats; defaults/features affect support | Show a build-specific capability list and explicit import/export-loss warnings. Validate each direction separately. |
| F20 | P2 | Localization and hardware edge cases | Recorded missing Hindi/Arabic/Vietnamese catalogs, English engine errors, partial RTL and pen/display coverage | Test actual text/IME/focus and monitor changes, rather than counting translated keys alone. |
| F21 | P2 | Release/support experience incomplete | No in-app update check or reviewable diagnostic bug-report workflow in scorecard | Add verified version checks and a local diagnostic preview with user-controlled sharing. |
| F22 | P2 | Automation/dependency security work remains | Security overview: no general capability scopes, aggregate memory/duration budgets, audit trail, confirmed audit/deny jobs or SBOM | Extend existing authentication/root restrictions and resource limits; add dependency policy and release inventory. This review confirms a documented gap, not an exploit. |

## Performance: what the committed results actually say

The baseline is **5 October 2026, commit f5d2bcb54a, Apple M4 Pro, 48 GB RAM**. Its recorded starting load average is **224.90 / 226.31 / 196.03 on 14 cores**. These timings are not trustworthy estimates of current speed on an idle machine and cannot support a numerical speed comparison with Photoshop. They nevertheless identify scenarios that urgently need clean measurement.

| Scenario | Recorded p95 | Project target | Interpretation |
|---|---:|---:|---|
| Styled-layer drag update | 535 ms | 25 ms | Would visibly trail the pointer if representative. |
| Opacity change | 443 ms | 20 ms | Continuous slider adjustment would feel delayed. |
| Paste 12 MP, first | 3,136 ms | 100 ms | Large pause for a common action. |
| Move layer, 150 MP/16-bit | 4,318 ms | 80 ms | Major large-document interaction concern. |
| Content-Aware Scale, 24 MP | 954,192 ms | 3,000 ms | Approximately 15.9 minutes in this baseline; needs algorithm/work-budget investigation. |
| Select Subject, 24 MP | 693 ms | 100 ms | Responsiveness shortfall; selection quality must be measured separately. |
| Content-Aware Fill, 10 MP | 256 ms | 1,500 ms | Meets recorded target; timing does not establish fill quality. |
| Spot Healing, 10 MP | 247 ms | 500 ms | Meets recorded target. |

Current generated scorecard: **56 scenarios: 3 within budget, 22 over budget/failing, 9 tracked only, 17 not run, 5 not measurable**. “22 of 25” describes the historically exercised budget subset, not 25 exhaustive tests of the product. Frame timing, preview memory, cancellation and several expensive style cases still need observation.

## Testing assessment

**The quantity and variety of tests are strong for an alpha. The acceptance evidence is weaker than the feature count.**

Existing strengths: Linux/Windows workspace tests and Clippy; feature-on/off HEIF checks; font-enabled builds; dependency layering; actual browser build/size checks; pinned corpus fetching in CI; malformed and property tests; CPU/GPU comparisons; real egui pointer-driven pixel tests; atomic-save failure injection; memory-failure transaction tests; and a scheduled performance workflow. Engine Photoshop-oracle tests deliberately discard cached type/smart-object images and rerender them, which avoids one important false sense of correctness.

Concrete test gaps:

1. **Ignored safety test is not an explicit CI gate.** `panic_hunt.rs` uses `#[ignore]`. No `panic_hunt` or `--ignored` invocation was found in `.github/workflows` or `xtask/src`. The contributor instructions require it manually; ordinary workspace testing will skip it. The scorecard checks that the file exists, not that it ran.
2. **The safety test is a smoke test, not exhaustive fuzzing.** It sends four fixed parameter objects into fresh tiny sessions. It catches panics/hangs, but does not assert correct rejection or unchanged state for every command. A timed-out thread is not forcibly stopped. Extend with schema-aware generated cases, long sessions and process-level isolation for hangs.
3. **GPU failures can be counted as success-by-return.** For example `checker_canvas.rs` catches any panic constructing the harness, labels it “no GPU adapter,” and returns `None`; callers may return without assertions. Distinguish unavailable adapter from broken initialization and require actual rendering on at least one CI lane.
4. **Self-round-trip is insufficient interoperability proof.** Our writer and reader can agree on the same nonstandard representation. FILE-216-4 identifies the external-editor gate as missing. Add Photoshop acceptance and an independent parser, including editability checks.
5. **Corpus floors are thresholds, not latest results.** 133/258 is a minimum, not a freshly observed success total. Include skips/errors/thumbnail comparisons and actual denominators in CI artifacts. Aggregate floors should not hide a regression in a critical subgroup.
6. **macOS correctness is tested at release, not ordinary PR/main CI.** Nightly performance helps but is not a substitute for platform correctness tests. Add a periodic correctness lane and selected pre-merge coverage for platform-sensitive changes.
7. **Fuzzing is manually triggered.** CI's fuzz job runs only on `workflow_dispatch` with the fuzz input. Add scheduled campaigns and retain/minimize regressions.
8. **Large documents and long sessions lack regular acceptance coverage.** Large PSB tools/tests exist, but scorecard says relevant fixtures are opt-in/outside CI. Add bounded 150-layer tests per merge and larger nightly/release stress runs.
9. **Workflow suite remains small.** Recorded MCP acceptance suite is ten tasks; target is 30–50. Include real UI gestures, save/reopen, cancellation, recovery and independent export inspection.
10. **Accessibility and artistic quality need distinct tests.** AccessKit and contrast assertions do not establish a usable screen-reader session; image equality does not establish pleasant brush response, believable healing or hair-edge quality.

Recommended validation sequence once a supported toolchain and dependencies are available:

```powershell
cargo test --workspace --locked --features heif
cargo clippy --workspace --all-targets --locked --features heif -- -D warnings
cargo xtask layers
cargo xtask wasm
cargo xtask scorecard --check
cargo test -p photocraft-engine --test panic_hunt -- --ignored
cargo xtask test-corpus
cargo xtask perf --quick
```

Then run full release benchmarks on quiet representative hardware, Photoshop re-open validation, and tablet/IME/screen-reader sessions. These commands are a plan, not completed checks in this review.

## UI and overall feel

**Visual judgment: the interface already communicates “serious image editor.” Its weaker area is demonstrating trustworthy interaction depth.** The dark screenshot places artwork first, with familiar toolbar/options/properties/layers organization. The typography capture shows editable type integrated with layer effects. The light export dialog has a readable grouping and a clear primary action. Those are useful strengths.

The product should keep the canvas dominant and communicate through precision, stable feedback and good defaults. Decorative effects and more themes would have less value than reliable actions and explicit states.

| Area | Observation or concern | Improvement |
|---|---|---|
| Hierarchy | Visual: canvas dominates; right dock is dense | Retain density for experts, offer task presets with only relevant panels initially. |
| Recognition | Visual: many similar small monochrome icons and compact footer actions | Verify tooltips, accessible names, shortcut hints and novice recognition; allow an optional labeled mode. |
| Legibility | Visual: muted secondary text is easy to overlook | Audit essential metadata at actual display sizes and all themes; essential small labels need stronger contrast. |
| Contrast gate | Source: some theme checks accept 3:1 dim text and 2:1 faint text | A passing test does not certify body-text accessibility. Determine which tokens render meaningful small text and use an appropriate threshold. |
| Interaction confidence | Recorded gaps around transforms, targeting and preview consistency | Clearly identify pixel/mask/channel/filter target; expose Apply/Cancel and preserve preview/commit agreement. Reverify older transform issues because some are already fixed. |
| Workspaces | Source/scorecard: docking exists, arbitrary floating groups remain incomplete | Reliable layouts, reset, restart persistence and multi-monitor behavior before adding panel decoration. |
| Export confidence | Visual: dialog shows format/quality/size preview; full output capability varies | Add a compact preflight for layers, profiles, alpha, text/fonts and unsupported features. Preview the exact selected encoding where feasible. |
| Learnability | Photoshop vocabulary suits migrants but assumes experience | Task examples and progressive explanations: “paint the mask to hide,” “this operation will rasterize,” and short tool recipes. |
| Recovery | Atomic saves and panic guards are valuable foundations | Make autosave/recovery provenance, pending work and safe retries understandable in the UI. Verify the full crash/relaunch journey. |
| Emotional feel | Artwork-led and restrained; confidence can fall when a familiar control differs silently | Explain capability limits at the point of action and make every experiment reversible. |

Minor but worthwhile improvements: keyboard focus that remains visible; consistent numeric precision/units; distinguishing disabled from unsupported commands; useful empty-library states; feedback when a click targets a locked/hidden layer; remembering recent export/tool settings; zoom-aware cursor readability; reliable long-name ellipsis; and consistent panel action placement. These are design checks/proposals unless tied to a specific source finding above.

Do not infer latency, pressure quality, screen-reader behavior or absence of clipping from a static screenshot. No fresh whole-UI accessibility rating is justified here.

## Comparison with Photoshop and other editors

This is a capability and workflow comparison using official product documentation, not a timed hands-on shootout. Competitor documentation describes supported features, not flawless behavior on all files.

| Editor | Benchmark worth learning from | Where PhotoCraft stands |
|---|---|---|
| Adobe Photoshop | Integrated selection/refinement, retouching, editable smart workflows, RAW and generative editing | Much conventional feature surface exists; depth, file acceptance, speed, hardware behavior and ecosystem remain material gaps. Adobe documents an interactive Content-Aware Fill workspace and non-destructive Generative Fill; a parameter dialog or classical inpaint is not equivalent. [Content-Aware Fill](https://helpx.adobe.com/uk/photoshop/desktop/repair-retouch/remove-objects-fill-space/remove-objects-with-content-aware-fill.html), [Generative Fill](https://helpx.adobe.com/ca/photoshop/desktop/create-open-import-images/create-images/edit-images-with-generative-fill.html). |
| Affinity | Dedicated RAW development plus adjustment/live-filter workflows, retouching, batch/macros and layered composition | An important everyday-photo-workflow benchmark. PhotoCraft has relevant primitives, but must establish that they form a reliable complete workflow. Current Affinity branding/product differs from older “Affinity Photo 2” comparisons. [Official photo toolkit](https://www.affinity.studio/photo-editing-software), [RAW development](https://www.affinity.studio/help/raw-raw/). |
| Krita | Painting-centered brush engines, stabilization, wrap-around and animation | The better benchmark for an illustrator's feel. PhotoCraft's broad brush options are promising; pressure/latency and an artist-tested painting loop should be proved before competing on painting quality. [Official features](https://krita.org/en/features/). |
| GIMP | Open-source editing, non-destructive GEGL filters and color-management workflows | PhotoCraft's Photoshop-like model and automation are differentiators; open source and non-destructive editing alone no longer distinguish it. GIMP 3.0 already documents re-editable filters persisted in XCF. [GIMP 3.0 release notes](https://www.gimp.org/release-notes/gimp-3.0.html). |
| Photopea | PSD-style smart-object editing inside a browser | A useful acceptance benchmark for PSD tasks and browser workflows. Photopea documents shared smart-object sources, nested editing and smart filters. PhotoCraft's native engine/CLI offers a different foundation, but Rust/WebAssembly alone does not prove a better browser experience. [Smart objects](https://www.photopea.com/learn/smart-objects). |

PhotoCraft's strongest potential differentiator is **a coherent offline editor whose human actions and automation use the same inspectable commands**. That advantage becomes meaningful when a user can replay an edit, understand its target, cancel it safely and exchange the result.

## Missing features: what to build first

### Professional essentials

1. Verified PSD/PSB exchange in both directions, including editable text, smart filters/objects, masks, effects and profiles.
2. Consistently responsive layer, opacity, brush, transform and large-document interactions.
3. Complete interactive Select and Mask and controllable content-aware workspaces.
4. Editable text on a path, mixed-direction text, visible variable-font axes and dependable IME behavior.
5. Smart-filter mask painting, blend/reorder controls and non-affine smart-object transforms.
6. Camera-specific RAW references, CR3 support, sidecars and lens/color workflows.
7. Correct vector/text PDF workflows, print preflight and honest spot-color limits.
8. Document-independent actions, robust batch naming/cancellation and cross-document replay.
9. Local reusable asset libraries with packaging/relinking.
10. Fully effective preferences, persistent workspaces and trustworthy recovery.

### Photoshop migration and specialist work

Dedicated Color Sampler/Art History Brush/Convert Point surfaces; broader preset interchange (`.atn`, `.asl`, `.csh` with source/format verification); deeper plugin ABI; reviewed Photoshop-plugin compatibility scope; full tool context menus; multi-monitor floating groups; HDR/display-profile behavior; video-layer interchange; additional modern and specialist codecs; and content provenance where demanded by users. Revalidate `.shc` claims: a contour editor/import/export already exists, while library management and external verification remain partial.

### AI capabilities

Optional semantic subject selection and matting first, then removal/upscaling and generative edits if model quality/licensing/runtime cost fit the product. Preserve classical offline tools. Each generated result should arrive as a separate editable layer with mask, recorded settings and clear provenance. Keep inference optional and distinguish local processing from remote processing before a job starts.

## Creative and artistic opportunities

These are proposals, not claims of uniqueness. Several have analogues in other editors. Their value would come from integrating them into an understandable, editable workflow.

| Idea | Artist's experience | Practical first version |
|---|---|---|
| **Creative branches** | Explore “quiet dawn,” “neon rain” and “ink poster” without losing the chosen version | Named branches of history with thumbnail comparison and copy-to-main; build on existing history/comps while defining actual branch semantics. |
| **Palette instrument** | Pull a palette from a reference, lock skin tones, then tune color harmony | Local reference sampling plus an editable masked color-map adjustment and palette lock controls. |
| **Material studio** | Build believable paper, grain, ink bleed and foil without flattening the artwork | Deterministic procedural textures and effect stacks with scale/lighting parameters and export-loss warnings. |
| **Printmaker workspace** | Create duotone, risograph and screen-print looks with intentional registration and ink overlap | Separation preview, halftone controls and editable simulated plates; certified physical separations come only after print validation. |
| **Light painting layers** | Paint warm bounce, rim light and atmospheric haze while preserving the original | Masked color/exposure layers and recorded strokes; semantic relighting can be a later optional ML extension. |
| **Composition lens** | Check focal balance, grayscale contrast, safe areas and thumbnail readability | Overlay modes and export-size previews that explain what they measure without judging the artist's taste. |
| **Reference desk** | Pin moodboards and material/color references beside the canvas | A non-exporting reference panel with local assets, notes and sampled colors. |
| **Collage cabinet** | Cut, arrange and reuse paper, photographs and shapes quickly | Cutout asset library, edge presets, linked sources and simple contact shadows. |
| **Living typography** | Bend text around organic curves and explore variable fonts directly on the canvas | Path text plus visible font-axis controls, with a dependable caret and save format. |
| **Texture workshop** | Turn artwork into seamless textile, game or product patterns | Wrap-around preview, offset/seam inspection and deterministic pattern export. |
| **Retouch recipes** | Repeat a careful workflow while adjusting its decisions for each image | Editable command recipes with masks, relative targets and staged before/after checks. |
| **Color score** | Play with several color treatments as a coordinated family | Compare editable grades across artboards/documents using shared palette references. |
| **Constraint-based assistant** | “Change the sky, preserve the face and jacket, show me three versions” | First expose a previewed command plan with locked layers/masks; execute after review, recording every edit. Natural-language ML is a separate extension. |
| **Process edition** | Export a final piece with a contact sheet of key creative decisions | Named milestone snapshots and a locally generated process sheet; publishing remains user-controlled. |
| **Craft packs** | Load a complete visual recipe rather than a disconnected preset list | Versioned bundles of brushes, palettes, textures and actions, including asset licenses and compatibility metadata. |

Start with **Reference desk + Palette instrument + Material studio** after reliability improvements. They fit the existing layers, adjustments, presets and command architecture, offer immediate artistic value, and have a manageable first version. Creative branches and Living typography are larger changes. Semantic relighting and generative assistants carry substantially more model, quality and resource work.

## Route to a professional product

| Stage | Scope | Proposed exit evidence |
|---|---|---|
| 1. Establish truth | Refresh metrics, get reproducible builds, make safety/GPU gates explicit, rerun baseline | Counts tied to one commit; executed/skipped checks visible; quiet-machine benchmark artifacts; no fabricated readiness percentage. |
| 2. Earn trust | PSD exchange, save/recovery, GPU/allocator failure handling, common-workflow visual fidelity | All agreed must-pass fixtures open in Photoshop and preserve required editability; failed operations retain original state; crash/relaunch recovery is demonstrated. |
| 3. Improve daily feel | Brushes, selections, transforms, masks, type, actual preferences | At least 30–50 acceptance workflows across supported desktop classes; latency targets met on defined hardware; artist/tablet and accessibility sessions documented. |
| 4. Support paid workflows | RAW, print/export, reusable assets, actions/batch, diagnostic support | Successful photography, retouch, design and painting pilot projects with independent output checks and no blocker defects in those supported scopes. |
| 5. Build artistic identity | Palette/material/reference workflows, then branches and optional AI | Artist evaluation shows useful control and understandable results; effects remain editable and portable or explicitly warn on conversion. |

The repository estimates 1,100–1,800 sequential agent-hours to beta and 2,300–4,100 to full parity. Those are historical planning assumptions, not a delivery promise or a fresh estimate from this audit. They include overlapping work and depend on hardware access, external oracles, scope and product decisions. Plan by demonstrated workflow gates instead of extrapolating a percentage from PR volume.

**Product decision:** prioritize dependable professional workflows, then add artistic depth. The current project has enough breadth to justify consolidation. Its professional milestone should be a user completing a real job, revising it, recovering it and handing it off successfully.

## Evidence index

- [Workspace and version](../Cargo.toml)
- [Existing readiness assessment](target-app-parity.md), [roadmap](../ROADMAP.md), [ranked historical gaps](gaps.md)
- [Generated scorecard](scorecard.md), [scorecard source checklists](../scorecard/)
- [Toolbar definitions](../crates/ui-egui/src/state.rs), [toolbar and long-press behavior](../crates/ui-egui/src/panels.rs)
- [Themes and contrast tests](../crates/ui-egui/src/theme.rs)
- [Text shape model](../crates/doc/src/text.rs), [Warp Text tests](../crates/ui-egui/src/warp_text_dialog_tests.rs)
- [PSD corpus floors](../crates/io/tests/corpus.rs), [manifest](../xtask/photoshop-corpus.sha256), [pins](../xtask/src/corpus_pins.rs)
- [Cache-free Photoshop re-render oracles](../crates/engine/tests/photoshop_oracles.rs)
- [Adversarial command test](../crates/engine/tests/panic_hunt.rs), [GPU harness example](../crates/ui-egui/tests/checker_canvas.rs)
- [CI](../.github/workflows/ci.yml), [nightly performance](../.github/workflows/perf-nightly.yml), [release configuration](../.github/workflows/release.yml)
- [Performance baseline](../perf/baseline.json), [budgets](../perf/budgets.toml)
- [RAW dispatch](../crates/raw/src/lib.rs), [DNG tile decode](../crates/raw/src/sensor.rs)
- [Security status](../book/src/security/overview.md), [security policy](../SECURITY.md)
- [Screenshot sources](images/SOURCES.md)
