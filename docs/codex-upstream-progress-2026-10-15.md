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
