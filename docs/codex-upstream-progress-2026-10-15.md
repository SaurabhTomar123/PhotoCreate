# Codex upstream and reliability lane

15 October 2026. Work follows [the shared allocation](codex-claude-work-plan-2026-10-15.md). Claude owns the poster/readiness/guided-tray lane; this record does not claim its progress.

## C1: pinned upstream intake

Integration branch `integration/upstream-2026-10-15` starts from the published coordination checkpoint `388a0077` and merges pinned upstream `df055f3dcb0bb0312af97548ee6c6f9628f21dd7`. Merge checkpoint: `ab1c9d0c`. This is an unqualified development candidate until the results below are complete; main remains unchanged.

The only text conflict was the autosave retry test in `apps/photocraft/src/services.rs`. Upstream independently adopted our wait-for-requested-revision correction. Resolution keeps upstream's nonzero revision assertion and explanatory comments, the explicit requested-revision predicate, and final revision/recovered-pixel assertions. No production recovery logic changed in the resolution.

Semantic review confirms the local bounded shape cache, generation guard, one Purge All integration, histogram coalescing, small-mip full-redraw mitigation and expanded U8/U16/F32 readback test remain. Upstream's new DX12 scratch routing is kept pending explicit hardware qualification. New wasm boot application is registered as an exempt app in the layer table. No source changes were made in Claude's assigned modules.

Initial completed checks: dependency layers (30 crates), scorecard consistency and all pinned corpus fetch/verification passed. Full native/corpus, documentation, lint, wasm and app-build checks are running sequentially against the isolated worktree and existing compact build target. Logs: local `dist/qa/codex-upstream-2026-10-15/`. The owner-facing summary must distinguish finished checks from pending ones.

## C2: differential probe of the preserved app

Before changing input code, tested the preserved integrated 0.8 executable on the original synthetic 1791 × 1083 RGB16 fixture in four new isolated profiles. One batched brush gesture was followed by nine zoom changes and one undo/redo. Transcript and sampled pixels are retained; only the recording mode has continuous video.

| Mode | Result |
|---|---|
| No capture | Passed: no extra history; undo/redo restored expected samples |
| Capture with `focus:false` | Failed: a screenshot timed out waiting 60 seconds |
| Capture with focus | Passed: no extra history; undo/redo restored expected samples |
| Background recording connection | Passed: no extra history; undo/redo restored expected samples |

These runs do not reproduce the earlier extra Brush history entry and do not fix or invalidate the historical failures. The no-focus timeout is a separate observed capture failure; occlusion, device state or another cause is not established. Do not remove strict single-stroke/history checks, issue extra undos to force a pass, or attribute events to a user without evidence. Further diagnosis needs event-source/frame evidence if the extra edit recurs. No editor input code was changed based on these probes.

The old and new executables, profiles and evidence directories remain distinct. Private profiles and tokens are never added to Git or shared archives. The full integration and any new live recording must finish before promoting main; performance and professional-readiness claims remain unchanged.

## C4: first Claude branch review

Claude published `claude/editorial-poster` at `f5a0f0c7`, containing L1 specification, command map and three documented headless prototypes, with no product source changes. Fetched and reviewed its technical contract without merging it. [Required rollback/history/journal corrections and integration choices](codex-review-claude-poster-l1-2026-10-15.md) are recorded for L3. New document always and Portrait 4:5 at 150 ppi are accepted as reversible initial choices; installed-font fallbacks avoid blocking on bundled fonts. The recipe is not implemented or qualified by this review.

Candidate publication initially failed because the shared checkout had a remaining shallow-history boundary. A no-thin retry alone failed; completing upstream history with `fetch --unshallow` corrected publication. The candidate branch is on PhotoCreate; main is still unchanged. To avoid a disk-full build, reclaimed 8.01 GiB from individually verified old generated test EXE/PDB files predating the current native run. Baseline GPU unit/integration executables, frozen app/benchmark copies, source, corpus, private test profiles and recordings were preserved. Current compilation continued.

## Completed checks and evidence-reporting correction

Full pinned native suite passed **8,860 tests, zero failures/crashes, 73 ignored**, across 257 result groups. Corpus-enabled run passed **3,658, zero failures/crashes, 27 ignored**, across 160 groups. Documentation tests, formatting, strict workspace/all-target HEIF clippy, layers, scorecard, verified corpus, all 24 wasm library checks and the normal HEIF desktop build passed. Wasm retains three nonfatal dead-code warnings (`PAR_PIXELS`, `MAX_SUBFOLDER_DEPTH`, `MAX_SUBFOLDER_FILES`); native strict lint is clean. Explicit adversarial-input panic hunt passed. Actual AMD Radeon mip matrix passed separately on Vulkan and DX12. Test executions overlap; these are not unique-file or Photoshop-acceptance counts.

The recorded three-layer RGB8 compatibility workflow passed: new `layer.list` found the named shape, editable master saved/reopened with inspected layer data, pixel samples and clean state, PNG and PDF exported. PDF explicitly warns it is flattened and loses editable layers/masks/transparency. Independent PyMuPDF 1.27.2.3 rendered the single-page PDF at 512 × 384 and matched every RGB pixel of the PNG export. Screenshot inspection confirmed the three expected editable layers. The clip is 3.75 seconds; this is one bounded opaque RGB case, not calibrated print or independent Photoshop acceptance.

The RGB16 live capture reached 25% and 12.5% zoom, then timed out at 3.125%. Case failed; an 11-second playable partial clip and failed case ledger are retained. The clip does not cover the timeout interval. Earlier extra brush history remains unreproduced in the differential probes, and capture reliability remains open. No production input fix is claimed.

That failure exposed two auditor defects: CLI cases could fail but return exit 0 / summary `completed`, and an already-exited encoder skipped metadata publication. Added regression tests that fail before the correction, then changed the auditor to report failed case/capture/encoder outcomes, return a failing CLI status and retain encoder metadata even for a playable partial file. All **10 audit tests and 6 recovery-auditor tests pass**; memory tests pass 15 with one real-symlink permission skip. Historical failed artifacts keep their original summaries; use their case ledger and this correction rather than rewriting their provenance. No Rust source changed after the passing integration gates.

Owner then requested more space. Cleared **16.08 GiB additionally**: remaining verified old EXE/PDBs (8.39 GiB), plus inactive original debug incremental/library/metadata/object caches (7.69 GiB). Actual free space immediately afterwards was 16.93 GiB. Preserved executables/PDB/DLL in the original debug cache, baseline GPU tests, all source/corpus/recordings and active outputs. Release compilation can consume some reclaimed space. Cleanup logs are local. Logged build/test durations span activity gaps; they are not continuous CPU-work measurements.

Release baseline 0.8 is frozen with explicit Layer auto-selection; the pinned 0.9 release example is building for sequential 12 MP and 24 MP comparisons. No latency improvement is claimed before those measurements. Background redraw frame costs must not be mistaken for time to final pixels. Main is not yet promoted.
