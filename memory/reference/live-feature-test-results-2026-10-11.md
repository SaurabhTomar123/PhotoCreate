<!-- Generated reference snapshot; edit the canonical source, then run project_memory.py index. -->
Canonical source: [docs/live-feature-test-results-2026-10-11.md](../../docs/live-feature-test-results-2026-10-11.md)

Source content SHA-256: `c9d85d9799c1ac8307325d689319c0b17d5b92d495480964050c471d1fee0a87`

# PhotoCraft live feature test results — 11 October 2026

Subsequent local implementation: [GPU-preview mitigation, fresh checks, recordings and remaining lag](implementation-progress-2026-10-13.md). The audit below preserves the original baseline; its failure counts are not current-build claims.

The actual desktop application was built, launched, exercised and recorded. The audit retains **908 cases across ten sessions**, screenshots, inspected state, exact control requests, saved examples and video chapter times. This is a feature baseline for review before adding more functionality.

**Validation is complete and failed overall. One GPU mip assertion reproduced in isolation; three GPU integration targets crashed in the workspace run and passed when rerun serially.**

Open `dist/qa/feature-audit-2026-10-11/index.html`. Search for a tool, feature, status or evidence level, then use **Watch** to jump to its case in the appropriate video. Initial failures link to later successful prepared retests. `coverage.csv` preserves the full history, while `tool-coverage.csv` identifies the latest representative tool evidence.

## Coverage and its meaning

| Area | Result | What was established |
|---|---|---|
| Tool activation | 65/65 passed | Selected-tool state and options captured |
| Representative tool interactions | 65/65 have an observable result | Canvas/tool/view changes; seven advanced gestures and Slice Select/Remove needed follow-up setup |
| Behavioral assertions | 33 passed, 8 restricted, 2 historical assertion failures | Selection, strokes, text, exact undo/redo pixels, non-default adjustment/filter pixels, paths, masks, channels, layer properties, smart filters and actions |
| Save/reopen | 8 passed, 1 unsupported | Native, PSD, PSB, PNG, JPEG, TIFF, WebP and OpenRaster dimensions; native/PSD/PSB layer counts |
| Source menu rows, latest attempt | 535 passed smoke checks, 87 restricted | 622/631 rows attempted; a passed menu check verifies dispatch/dialog behavior, not complete output semantics |
| Remaining menu rows | 9 unexercised | Cut, Copy, Copy Merged, Paste, three Paste Special variants, Purge Clipboard and Purge All |
| Simulated GPU loss | Captured CPU recovery state | Application remained inspectable and screenshot-capable; real driver failure recovery was not induced |

The raw history contains 698 passed cases, 75 failed attempts, 126 restricted/unsupported attempts and 9 initial gestures needing dedicated fixtures. **These are execution counts, not counts of broken features.** All 73 failed menu attempts subsequently passed with required fixtures or explicit inputs. All nine initially unresolved tool gestures have successful follow-ups. Earlier outcomes remain available for reproduction. Two additional TGA assertions failed because the harness initially expected layer transparency; the corrected channel-based test passed.

The nine clipboard/purge rows were left out to preserve the user's existing OS clipboard. Restrictions are primarily the application's automation policy: ambient filesystem commands, linked/external assets, printing/export menus and desktop color-mode/profile operations. Capability-scoped `app.open` and `app.save` were tested separately. A policy refusal does not establish that the corresponding manual feature is absent or broken.

## Concrete behavior demonstrated

The recordings include selection drawing; pressure-ramp brush, pencil, eraser and retouch strokes; inline editable type; shape and path tools; native mouse panning/view rotation; zoom clicks; anchor insertion/deletion/direct selection; slicing; controlled mark removal with background-job completion; selection masks and feathering; alpha-channel selection restoration; duplicate/blend/opacity/group operations; Gaussian smart-filter parameter editing and visibility; action recording/replay; layer effects, shape combinations, rasterization, multi-layer operations, blank video-frame commands and warp-grid editing.

Undo/redo restored an inspected composite pixel exactly. Brightness and Gaussian parameter dialogs were edited to non-neutral settings and changed inspected pixels. A saved selection restored identical bounds. Action playback reproduced rotated canvas dimensions. These are stronger assertions than a successful command return.

Displace initially required a map and a filesystem map was refused by automation. A later in-memory document-map invocation succeeded without bypassing the policy. Vanishing Point succeeded with explicit plane/clone data. Their default menu invocations had returned missing-input errors; that history remains useful for reviewing input acquisition and discoverability.

PDN saving is explicitly unsupported: it is import-only. Flat exports report layer flattening and format losses. OpenRaster warns that text is saved as pixels. JPEG warns about lossy compression; WebP warns about lost DPI. These are product limitations and correctly surfaced warnings, rather than silently successful full-fidelity round trips.

## Failure needing investigation

The workspace UI library failed:

`gpu_canvas::mip_tests::canvas_mips_preserve_opaque_pixels_and_partial_updates`

At `crates/ui-egui/src/gpu_canvas_mip_tests.rs:95`, a partial U16 mip at level 5 returned `[5.9604645e-8, 0.0, 0.0, 0.0]`, violating the expected opaque-alpha invariant. The reported adapter was **AMD Radeon(TM) Graphics**, **Vulkan**, driver **25.10.37.03**. The test compares partial mip updates with a full rebuild and checks U8/U16/F32 surfaces.

This is a real test failure, separate from fixture prerequisites. It raises a concern about reduced canvas previews after edits, particularly high-depth documents. It does not by itself identify a driver bug or prove that every document visibly fails. The exact test reproduced the same failure in isolation. Investigate rendering before adding features.

## Recording and environment

- Checkout: `d45b371`, PhotoCraft 0.7.0. Product source was left unchanged.
- Rust stable 1.99.0; Visual Studio 2022 C++ toolchain; Windows; desktop build with `--locked --features heif`.
- Original synthetic 512×384 artwork; isolated preferences and scoped sample/output roots.
- H.264 recordings generated from the application's GPU screenshots at 4 fps, with duplicated frames when capture is late; no audio.
- SRT/VTT captions, chapter times, per-case PNGs and inspected JSON accompany each session.
- GDI window capture was rejected after a frame inspection showed a white GPU surface. Its probe and interrupted early run are diagnostic outputs and are excluded from the viewing package.
- The initial workspace build hit Windows' running-executable lock. It was rerun after moving subsequent recording launches to a copied executable. That initial infrastructure failure is preserved separately.

The menu sweep sometimes retains floating panels opened by earlier cases. It is a recorded walkthrough rather than an isolated visual-regression suite. The deeper prepared checks use separate sessions. Recording and concurrent compilation timings are not performance benchmarks.

## Boundaries before claiming professional readiness

This audit does not certify every parameter combination, artistic output quality, calibrated print/color accuracy, large-document release performance, camera-specific RAW coverage, actual tablet hardware, IME/screen-reader behavior, plugin installation, or fidelity when reopened in an independently installed Photoshop/Affinity/GIMP. The corpus run passed 2,774 tests; those are repository test executions, not 2,774 certified Photoshop-compatible files. The corpus floor can pass despite known oracle mismatches. The large camera RAW corpus was not fetched.

Keep the recordings and sample files as the baseline. Prioritize investigating the GPU failure, reviewing default menu input flows, and adding scenario-specific semantic assertions. This evidence supports evaluating the current implementation; it is not a declaration of Photoshop parity or production readiness.


## Completed repository checks

Counts are test executions within each run; corpus checks and isolated reruns overlap workspace tests and must not be summed into a unique-test count.

| Check | Result |
|---|---|
| Desktop build, locked dependencies, HEIF enabled | Passed |
| Workspace library/integration tests | 6,577 passed, 1 failed assertion, 59 ignored; 3 integration targets crashed; exit 101 |
| Exact GPU mip test, isolated | Failed again with the same U16 partial-mip value |
| checker_canvas, isolated with one test thread | 7 passed |
| color_managed_canvas, isolated with one test thread | 2 passed; actual GPU/CPU sampled outputs logged |
| full_res_preview, isolated with one test thread | 3 passed |
| Corpus suite | 2,774 passed, 0 failed, 24 ignored |
| Command panic-hunt, explicitly including ignored test | 1 passed |
| Documentation tests | 1 passed |
| Dependency layers and generated scorecard consistency | Passed |
| Python audit harness tests | 5 passed |

`checker_canvas` and `full_res_preview` crashed with Windows STATUS_ACCESS_VIOLATION; `color_managed_canvas` crashed with STATUS_HEAP_CORRUPTION. Their twelve serial tests passed, but that does not repair or explain the original crashes. GPU outputs and adapter logs demonstrate that the serial runs did more than merely skip an unavailable adapter. Native crashes remain a stability concern; neither GPU-driver blame nor a concurrency root cause is established.

The ignored-test ledger identifies excluded performance, huge-document, external-asset and manual evidence cases. A 12 GB PSB allocation test was not forced on this development machine. The initial workspace compilation failed because Windows locked the running application executable; the subsequent completed workspace run used a separate copied app for recordings. Both logs are retained.

## Follow-up from your evaluation document

The supplied Word document reviews commit d45b371 and explicitly says the app had not been built or run. Its recommendations were treated as test hypotheses, rather than implementation instructions. `evaluation-checklist.csv` maps its major gaps, failure reports, testing concerns and papercuts to evidence or an explicit remaining boundary. Source estimates, old issue reports, issue counts and CI statistics have not been revalidated as current external facts.

Three new bounded behavioral scenarios were recorded:

- Transparent PNG: zero, half and full composite alpha values survived import.
- TGA: the initial composite-alpha test failed twice. Source inspection showed deliberate import into an opaque Background plus a separate Alpha 1 channel. The corrected live test passed. Independent decoding with Pillow 12.2.0 then found **every RGBA byte identical** between the source TGA and the PhotoCraft-exported TGA. The specific claim that this synthetic TGA loses alpha is therefore unsupported; named-channel handling differs from PNG transparency. The original failed assertions remain visible.
- A 150-populated-layer, 512?384 document: ArrowRight moved the selected layer, ten visibility toggles completed, screenshots succeeded and the native document was saved. The reported GPU crash did not reproduce in this bounded fixture. This does not clear the original large-document problem or qualify release performance.

The document also says cross-document action replay is missing. The recorded rotate action successfully replayed on a fresh document; this establishes one basic cross-document scenario, not reliable replay of every recorded operation. Ten follow-up menu checks resolved additional context prerequisites, leaving 86 policy refusals and one CMYK-dependent Trap prerequisite among the 87 restricted menu rows.

## My assessment after seeing it run

PhotoCraft has substantial working breadth. Editable layers, masks, selections, text, smart filters, action playback and a recognizable Photoshop-style shell form a useful foundation. The clean session screenshots have a readable hierarchy and familiar dock order. The menu sweep shows how floating panels can accumulate and cover the canvas; a user walkthrough should handle panel cleanup and task context more deliberately. Default invocations of complex tools often need more guidance to acquire inputs. A successful prepared invocation proves the operation is reachable, but says little about whether an artist would discover it.

I would keep it at **alpha readiness for professional evaluation**. The reproducible high-depth preview failure and native test crashes deserve attention before feature expansion. Independent Photoshop export acceptance, real tablet feel, reliable recovery and large-document latency remain gates for paid work. I would not assign a new readiness percentage from this audit or promote the document's historical estimates into measured scores.

The artistic ideas in your evaluation remain attractive. After rendering and save/recovery confidence improves, I would start with a reference desk, palette extraction, material textures and print-style recipes. They build on demonstrated layers, filters, swatches and actions. Paint Replay and editable creative recipes are stronger identity bets once history/replay semantics are dependable. Natural-media simulation and generative layers are larger research projects; this audit provides no evidence that those missing capabilities already exist.

## Review package

The searchable viewer, ten MP4s, soft captions, chapters, screenshots, sample outputs, logs, coverage ledgers, evaluation matrix and reports are collected in `dist/qa/photocraft-feature-baseline-2026-10-11.zip`. Extract the whole archive and open `feature-audit-2026-10-11/index.html`; keep the sibling session folders beside it. For reliable browser caption loading, serve the extracted parent folder locally with `python -m http.server 8765` and open the viewer through localhost. The MP4s can also be opened directly in a video player with their SRT sidecars.

All ten videos were verified with FFprobe: H.264, 1920?1200, four frames per second, **25 minutes 21.25 seconds** total. Recording metadata reports no capture errors and successful encoders. A source-scoped SHA-256 artifact manifest accompanies the archive. Private control credentials/configuration, diagnostic white-screen runs, executable builds and third-party corpus assets are excluded. Product source remains unchanged.
