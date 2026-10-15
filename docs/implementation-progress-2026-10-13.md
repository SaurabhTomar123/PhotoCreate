# PhotoCraft revamp implementation progress

13 October 2026. This is the current execution record, separate from the immutable original feature audit and planning proposals.

## Current batch

- **F01 / S1: local mitigation implemented and validated.** A fresh pre-change run of the retained GPU test binary reproduced the U16 partial-mip failure. Evidence: `dist/qa/revamp-gpu-before-2026-10-13/`.
- **GPU diagnosis: regression improved; root cause not established.** Added image size, mip path and pixel coordinates to the regression; both direct and scratch paths are attempted even when one fails. An unavailable adapter now fails this required test explicitly instead of silently passing.
- **Obsidian-compatible memory: vault-local snapshots implemented.** Canonical planning/audit sources and this execution record are mirrored into `memory/reference/`; the index links to vault-local readable copies. CSV backlog is rendered as Markdown. Originals remain authoritative and snapshot changes are detected by `check`.
- **F02: still unresolved.** The three original GPU target crashes are not claimed fixed by serial passing.
- **Other F01–F51 product work:** pending; no new shell, AI or beginner workflow is claimed implemented.

Updates below will include validated fixes, the exact checks and remaining limits. Open `memory/INDEX.md` from the memory vault for the same current information in Obsidian. Generated copies are refreshed with `python scripts/project_memory.py index`; do not edit them as an alternative source of truth.


## Diagnosis update

The enriched regression located the direct-path failure at U16 1791x1083, mip 5, pixel (16,16). In that same diagnostic device session the scratch path also failed at U8 mip 5, pixel (16,16); switching to scratch is not a validated workaround. Exact retained diagnostics: dist/qa/revamp-gpu-diagnostic-2026-10-13/.

Candidate change under test: redraw and clear complete mip levels when both dimensions are at most 64 pixels, while retaining bounded partial updates on larger levels. This specifically protects untouched texels in the small reduced previews, with at most a small number of additional texels per edit. It does not blame the driver or claim performance gains. Final results will determine whether it remains.


## Validated rendering change

The bounded small-mip redraw passed the focused GPU checks: eight tests passed, including the expanded readback matrix. It covers 8/16/32-bit inputs, opaque/semi-transparent/transparent backgrounds, center/top-left/bottom-right edits, thin images and both direct/scratch paths. Every reduced level is compared against a full rebuild. Strict UI linting passed.

This is a validated local correctness mitigation, not a confirmed driver root cause or a general GPU stability repair. F02 remains unresolved. Broader UI, WebAssembly, rebuilt live recording and the focused release layout benchmark are still finishing. No claim of faster overall editing or professional beta readiness is made.

Obsidian-compatible vault snapshots now include this execution record, all canonical planning/audit sources and a readable backlog table. `check` detects edited/stale snapshots; `index` refreshes them from canonical sources. Source notes and plans remain reference data, never execution authority.


## Validation infrastructure incident

The initial broad UI test build failed at link time (LNK1180: insufficient disk space), and the desktop, wasm and performance builds also encountered OS error 112. These are retained infrastructure failures, not passing checks or new product assertions. All affected jobs finished.

Recovered about 40 GiB by removing only target/debug/incremental and generated target/debug/deps/*.pdb files after validating their absolute targets. Sources, notes, corpora, recordings and saved outputs were retained. Retried checks use lower native build parallelism; results remain pending until completion. Original failure directories and new retry directories are separate.


## Platform/build progress

The desktop rebuild passed after storage cleanup. It was copied to dist/qa/photocraft-revamp.exe for recording, with a saved SHA-256 fingerprint. All 24 required wasm package/feature checks passed, including photocraft-ui-egui and codecs/HEIF. Dependency-layer validation passed. The UI library passed 2,035 tests with ten ignored; integrations and the release layout benchmark remain in progress.


## Completed batch results

- UI library/integration suite: 2,129 passed, zero failed, ten ignored across 24 test groups, run serially. This does not qualify the old parallel/native crash condition.
- Expanded GPU checks: eight passed on AMD Vulkan; the expanded mip regression passed separately on AMD DX12 (driver 32.0.21037.3009). The matrix includes 54 base cases and 162 center/edge updates, all reduced levels compared with full rebuilds.
- Strict UI lint, targeted formatting, dependency layers, all 24 wasm package/feature checks and the HEIF desktop build passed. Storage-failed initial builds remain separately recorded.
- Valid before/after live recordings: 19.25 and 14.5 seconds, H.264 1920x1200 at four fps. Both check 16-bit import, sampled composite editing/undo/redo and native save; the GPU readback test establishes the preview invariant.
- The first after-recording timed out waiting for screenshots while a benchmark was active. The isolated retry temporarily held the display awake and passed. The timeout cause is not established; no nonexistent/empty video is presented as success.
- Release layout benchmark ran twice after compilation; the final run had no concurrent app recording or GPU test. Its command exited zero, but this is not a latency-budget pass or proof of a speedup.

### Fresh responsiveness evidence

Workload: 4000x3000 (12 MP), 174 layers, 60 text layers, release offscreen GPU frame harness. Final isolated medians / p90: idle 1.22 / 1.44 ms; text visibility 424.76 / 490.99 ms; opacity 408.07 / 464.14 ms; pixel-move commit 428.67 / 447.82 ms; the translate operation itself 1.67 / 2.70 ms. These are frame/operation measurements, not physical pen-to-display latency. No comparable before-fix release benchmark was taken, so no performance improvement is claimed.

The expensive frame after layer changes is now a measured investigation target for F06. Profile rendering/compositing, invalidation and uploads before choosing the next optimization. F02 native-crash investigation, recovery qualification, other adapter/image coverage and the broader UI/novice work remain open.

### Records

[Review the scoped before/after viewer](../dist/qa/revamp-records-2026-10-13/index.html). Logs, source patch/fingerprints, failed/retry results, synthetic outputs and video health are retained under dist/qa/revamp-*. Original baseline recordings/archive are unchanged. Private control files stay outside shared records and memory. Obsidian snapshots, notes and backlog carry the same current status.


## Second batch: histogram work scheduling

Investigation found that the Histogram panel replaced its pending receiver whenever the document revision changed. Dropping a receiver does not stop its worker: repeated edits could leave multiple CPU thumbnail renders running alongside the GPU canvas. The existing histogram duration is background work, not evidence that the UI blocked for that entire duration.

The candidate change preserves one pending job across edits/document switches, consumes its result with the original revision tag, and requests another frame after completion/disconnection. The latest revision is scheduled next; stale data retains its existing warning. A synthetic test holds a worker pending across three edits, delivers an older result, and checks eventual latest-revision delivery. WebAssembly retains its inline fallback.

An optional PHOTOCRAFT_LAYOUT_TRACE diagnostic in the release layout harness prints slow-frame command, canvas, upload and retained-span counters. Counters explicitly remain last-sample values; they are not all costs incurred in that frame. Profiling and validation are in progress in dist/qa/revamp-layer-profile-2026-10-13 and dist/qa/revamp-histogram-*. No overall latency improvement or closure of F06 is claimed yet.


### Second batch completed checks and limits

The bounded Histogram worker scheduling change passed its corrected five-test tone suite and the entire serial UI library: 2,036 passed, zero failed, ten ignored. Final strict UI clippy, formatting, dependency layers, all 24 wasm package/feature checks, and the HEIF desktop build passed. Python recording checks passed five tests; local-memory checks passed 15 with one host-restricted real-symlink test skipped. Mocked refusal checks still run. No claim of fixing earlier parallel native crashes is made.

The first new Rust regression attempt failed because the minimal egui test pass discarded pending texture deltas. Clearing those test-only deltas corrected the harness; the failed log remains alongside the passing retry. A first Histogram-visible QA attempt used an invalid panels.histogram field; the app correctly rejected it. The retry uses panels.navigator plus dockTabs.navigator = 1 and asserts the tab state. These setup failures are not product regressions. A combined Python unittest invocation had an import-path error; script-entry-point reruns passed, and verified subprocess return codes are saved. PowerShell also reported stderr from passing Python tests as shell errors; direct subprocess results confirm exit zero.

### Paired release responsiveness evidence

Both preserved release executables ran sequentially with nine repetitions on the same PSD-round-tripped 4000x3000 / 174-layer / 60-text-layer workload. GPU synchronization and slow-frame tracing were enabled; Vulkan was requested. No build, UI recording or other GPU test ran during these measurements. This is one before/after sequence on one machine, not a controlled multi-run causal experiment or physical input latency measurement. The initial trace run overlapped compilation and remains diagnostic evidence only.

| Scenario | Before median / p90 (ms) | After median / p90 (ms) |
|---|---:|---:|
| idle frame | 0.79 / 2.27 | 1.19 / 2.00 |
| toggle visibility (text layer) | 351.48 / 399.48 | 335.03 / 349.23 |
| toggle visibility (group) | 37.87 / 423.71 | 29.73 / 340.84 |
| opacity change (Layers / Properties) | 337.92 / 349.78 | 345.11 / 377.98 |
| Move pixel: release (commit) | 323.73 / 342.15 | 326.46 / 362.82 |
| of which layer.translate (pixel) | 1.31 / 2.13 | 1.46 / 2.22 |

The scheduling fix does not deliver a consistent overall speedup. Opacity and pixel-move commit remain hundreds of milliseconds. Representative traces place almost all slow-frame time inside gpu-rect refresh while translate takes around 1-2 ms; that refresh includes CPU planning, staging and synchronized GPU execution. Repeated uploads are visible, but eviction/cache churn or a specific shader cause is not established. Next: measure those internal stages, effect work and cache residency separately. F06 remains open.

### New recordings and saved outputs

Two valid live captures show the rebuilt app: 14.5 seconds for 150-layer nudge/visibility/native save, and 13 seconds with Histogram explicitly visible during the same workflow. Both are H.264, 1920x1200, four fps, checked with ffprobe; screenshots were visually inspected. The Histogram is visible and populated after edits. Video establishes UI workflow behavior; the Rust test establishes pending-worker preservation and eventual latest-revision delivery. These use a 512x384 synthetic sample, not the 12 MP benchmark or original crash fixture. Native 150-layer .pcraft outputs are retained in each capture's samples directory. Temporary display-awake holds were restored successfully.

The [review page](../dist/qa/revamp-records-2026-10-13/index.html) links these clips, outputs and comparison. Source changes, final source/app hashes, release executables, JSON measurements and all failed/passing logs remain under dist/qa/revamp-histogram-* and revamp-layer-profile-2026-10-13. Private control configuration stays outside the viewer and vault.

## Third batch: canvas refresh stages and shape-cache working set

Added opt-in `PHOTOCRAFT_COMPOSE_TRACE` diagnostics for render/submission, mip submission and synchronized wait, alongside uploads, effect rebuilds, cache eviction and retained bytes. Submission can itself block in the driver; these are stage timings, not pure CPU/GPU hardware timestamps. Diagnostic write errors are ignored safely. The release harness also reports adapter identity on traced slow frames.

A source-level lead: the full layout fixture contains 33 stroked shapes (16 card backgrounds, 16 badges and one button), while `compose::shape_split` retains only 32 entries. Cyclic traversal can exceed that working-set limit and regenerate derived surfaces/uploads. This is a hypothesis pending traced runtime evidence and a regression; no speedup or cache fix is claimed yet. The instrumented release build is in progress under `dist/qa/revamp-compose-profile-2026-10-13`.


### Confirmed reuse defect and bounded fix under qualification

A traced AMD Vulkan sample spent 457 ms in render/submission, 0.88 ms in mip submission and 3.60 ms waiting. It rebuilt no effect shapes/programs and evicted no GPU cache pages, but reuploaded 78 tiles / about 20.4 MB. Submission is not pure CPU time, yet this sample rules out a long final GPU wait or GPU eviction as its dominant recorded stage.

A new isolated regression failed on the old 32-entry policy: unchanged shape zero of 33 rebuilt its fill on the next traversal. The proposed policy retains up to 128 entries and 128 MiB of conservatively accounted pixel storage, including input pixels pinned to protect address-based identity. Oversized results remain usable without retention; byte and entry pressure evict least-recently-used entries. A generation guard prevents a calculation started before purge from repopulating the cache. Edit > Purge > All now includes the shape cache, including eligibility when only cached data remains. Returned bytes describe cache retention, not guaranteed freed process memory.

The four focused regressions passed after the policy change, covering 33-shape reuse at U8/U16/F32, appearance/source/canvas invalidation, retained-byte/entry caps, pin release, old-generation admission and tick saturation. The full compositor suite passed 204 tests with one ignored. Additional live geometry/stroke pixel-oracle checks, native UI/engine/corpus checks, lint, wasm and rebuilt release timings remain in progress. The reuse defect is established; its performance contribution is not claimed until the comparison finishes.

A new recorded live workflow passed on the previous app: 4000x3000, 33 stroked/shadowed shapes plus three editable text layers and background. It checks sampled opacity change/restore, move bounds, undo/redo, native save/reopen and PNG export. The saved colour-study layout is a synthetic QA sample, not a new product UI design. Before records are in dist/qa/revamp-shape-layout-before-2026-10-13; the fixed-app capture is pending.


### 2026-10-14 continuation and storage recovery

The public geometry/stroke/canvas pixel-oracle integration passed at U8/U16/F32, and strict clippy across compose, engine and UI targets passed. The combined serial native/corpus/UI matrix is still executing. Initial desktop and wasm jobs failed with exit 101 after the disk filled (desktop log explicitly reports OS error 112). Their logs and results remain retained. Command wall times span a long interval across October 13/14; they are not continuous compiler CPU-time measurements. Host/activity continuity is not established.

Recovered 27.19 GiB by removing only the verified absolute target/debug/incremental cache and 191 generated target/debug/deps/*.pdb symbols. Reparse points were refused and source, corpus, recordings and outputs were retained. Free disk after recovery: 26.53 GiB. Desktop and wasm retries use new 2026-10-14 directories. No passing status is assigned to the failed attempts. Quiet final release comparison and fixed-app recording remain pending.


### Third batch qualified results ? 2026-10-14

The combined serial native engine/UI/file-corpus matrix completed 150 groups: **4,904 passed, zero failed, 34 ignored**. Separately: the compositor suite passed 204 with one ignored; four focused cache tests passed; the geometry/stroke/canvas pixel-oracle integration passed at U8/U16/F32; the ignored adversarial command panic-hunt passed. Strict all-target clippy across compose, engine and UI, formatting and dependency layers passed. All 24 wasm package/feature checks and the normal HEIF desktop rebuild passed on storage-recovered retries. Ignored cases and the earlier parallel/native crash condition remain unqualified. Python QA checks passed eight tests, including restoration without changing another process's reused window handle; memory checks passed 15 with one host-restricted real-symlink case skipped.

### Quiet release comparison

Nine repetitions per build, sequential runs with no concurrent external compile, recording or GPU test: same 4000x3000 PSD-round-tripped layout, 174 layers and 60 text layers. Both logs identify AMD Radeon(TM) Graphics, integrated GPU, Vulkan, AMD proprietary driver 25.10.37.03. GPU synchronization is enabled; stage tracing is off, and slow-frame diagnostics run after each measured frame. These are one paired run on one machine, not physical pen-to-display latency or a broad device guarantee.

| Scenario | Before median / p90 (ms) | After median / p90 (ms) |
|---|---:|---:|
| idle frame | 1.86 / 3.01 | 2.20 / 3.08 |
| toggle visibility (text layer) | 421.71 / 528.10 | 25.63 / 28.64 |
| toggle visibility (group) | 49.32 / 473.79 | 29.84 / 32.55 |
| opacity change (Layers / Properties) | 398.06 / 447.02 | 25.48 / 29.04 |
| Move pixel: release (commit) | 401.95 / 524.06 | 31.35 / 34.91 |
| Move text: release (commit) | 404.25 / 484.76 | 29.05 / 33.15 |
| Move shape: release (commit) | 5.78 / 495.44 | 3.57 / 30.52 |
| Move smart object: release (commit) | 427.47 / 541.02 | 33.73 / 53.26 |
| Move auto-select type: release (commit) | 462.69 / 604.02 | 93.46 / 104.65 |

Opacity median fell from 398.06 to 25.48 ms (about 15.6x), pixel-move commit from 401.95 to 31.35 ms (about 12.8x), and text visibility from 421.71 to 25.63 ms. The 32-entry cache cliff is a confirmed contributor to the earlier stalls: 33 unchanged stroked shapes exceeded the old working set, while hiding a card reduced it below that boundary. The bounded policy avoids that repeated rasterization/upload work on this fixture. Idle performance is essentially unchanged; shape-move medians were already small but their p90 spikes improved. The 16 ms target, more demanding text moves, larger working sets and the general GPU stability investigation remain open. Do not extrapolate the speedup to every tool, document or device.

### Verified recordings, output and capture limitation

The previous-app clip is 32 seconds; the fixed-app retry is 17.75 seconds. Both are H.264, 1920x1200 at four fps, verified with ffprobe. Clip duration is not a controlled workflow-speed measurement. The after case additionally tests Purge All: it reports shape-cache retention and preserves the sampled composite. Both cases save/reopen 37 editable native layers and export PNG. Independent Pillow decoding compared all 4000x3000 RGBA pixels: **before and after exports are identical**. Screenshots were visually inspected. The expected PNG warning reports flattening of 37 layers; the native master preserves editability.

The initial after capture timed out waiting for a screenshot and remains a failed attempt. The retry temporarily kept only the audit app above occluding windows without changing keyboard focus or other windows; its process/window ownership is checked before restoration. The window closed at finish and the temporary setting was cleared. Display-awake holds were restored. This is a QA mitigation, not an established screenshot-timeout root cause or a product fix for background/occluded capture. Only successful videos are displayed in the review page.

[Review all implementation recordings and outputs](../dist/qa/revamp-records-2026-10-13/index.html). The fresh comparison, validation ledger, source/executable hashes and independent output verification are in dist/qa/revamp-shape-perf-2026-10-14. Expected regression failures, build/storage failures and screenshot timeouts are retained separately. Private control files are excluded from the viewer, share archive and Obsidian memory.


## Live interruption and recovery qualification ? 14 October 2026

Passed a real forced child-process termination after observing successive completed autosaves at revisions 5 and 6. Same-profile relaunch restored the newer three-layer editable document, with matching inspected layer data and pixel samples. It correctly remained dirty; its saved native master reopened cleanly. Independent Pillow rendering matched every recovered 512?384 RGBA export pixel. No Rust editor code changed. F03 is partially qualified locally, not closed.

Added `scripts/live_recovery_audit.py` and three passing regression tests. Existing live harness: eight passed. Memory: fifteen passed, one permission-dependent real-symlink skip. Prior Rust/corpus/wasm checks remain unchanged; no product rebuild was required. Source/executable hashes, logs, output oracle and ffprobe verification are retained.

Five earlier attempts remain failed: two hit the 30-second authenticated control idle limit during a one-minute autosave wait; the corrected polling run and two short-clip variants hit 60-second screenshot timeouts after idle or export. Some failed recording encoders did not finish. These attempts do not establish failed recovery; the final run passed with no intermediate capture restart. Capture reliability remains a separate unresolved issue. Display-awake and visibility holds do not establish a cause or fix.

Final footage is a 1-second first-edit clip and a 3.5-second recovery/save/reopen clip, H.264 at four fps. The second edit, autosave waits and process interruption have timestamped command evidence, not continuous video. All clips and screenshots show synthetic art only. Temporary display-awake/visibility settings were released. The tab marked unsaved edits correctly, but a historical Saved action status remained visible: make current save/protection state clearer in the revamp.

[Detailed findings and limits](live-recovery-qualification-2026-10-14.md), [recordings and outputs](../dist/qa/revamp-live-recovery-final-2026-10-14/review.html). Updated the system contract, F03 backlog and Obsidian-compatible session record. Interrupted writes, disk failures, power loss, multi-document/high-depth/large-workload recovery and broader hardware remain pending, along with native GPU crash investigation and Atelier creation workflows.


## Upstream compatibility and next-generation strategy review ? 14 October 2026

Fetched upstream `ed7df56` without merging or changing editor code. Verified 750 commits and 870 changed files since our `d45b371` base. Per-file three-way previews are retained in `dist/qa/upstream-review-2026-10-14/compatibility.json`. Six of ten locally modified tracked files also changed upstream; text conflicts occur in the shape cache and two assessment docs. A clean text merge in Purge would call the shape cache twice, illustrating why clean Git merges still need semantic review. No integration build or tests have run.

Reviewed the owner-pasted PhotoCraft Next-Gen Technical Strategy after the Claude artifact URL returned only a public shell and its content endpoint required authentication. Support upstream editing depth plus our guided experience, with corrections to automatic shipping-branch rebases, cache budget reconciliation, typed metadata migration, capability enforcement, transaction scope, Actions export limits, L6 crate seams, AI data handling and audit/latency claims. Current catalogue: 871 commands; selected 25?31 ms cache figures are medians, not p95. Historical audit and completed-autosave recovery evidence remain bounded.

[Detailed review and proposed integration sequence](upstream-and-nextgen-strategy-review-2026-10-14.md). Prioritize upstream GPU test serialization, uniform-limit/error containment and missing-sidecar autosaves; retain our 128-entry/128 MiB policy, purge-generation guard, mip mitigation and histogram worker bounds. Recommend a protected current checkout plus a pinned integration candidate, then fresh validation and one finished beginner recipe. The feature backlog is unchanged because no upstream feature has been integrated or qualified locally. The recommendation is recorded as proposed in Obsidian memory; no external publication/account/CI actions occurred.


## Owner-authorized publication and integration started ? 14 October 2026

The owner requested publication of the current project to `SaurabhTomar123/PhotoCreate`, followed by upstream update and merge. The target repository was empty. Preparing a named baseline checkpoint before a separate pinned upstream integration; publication now has explicit authorization. Recent privacy-filtered evidence archives are versioned under `records/`, while the original large audit archive and complete ignored QA data remain preserved locally. Current local fixes, sources, plans and Obsidian memory are included. Integration qualification is still pending.


## Upstream candidate native gates passed ? 15 October 2026

The owner-authorized current snapshot is published to PhotoCreate at `918d422f`, on main and baseline/revamp-2026-10-14. The separate integration branch merges pinned upstream `ed7df56` and preserves the local cache, mip, histogram and QA work. The corrected full native suite passed 8,396 tests, zero failures, zero native crashes and 68 ignored. Initial failures remain retained: an autosave test publication race and missing GPU guards in two targets. The autosave correction passed twenty isolated repetitions. All three historical crash targets and the new marquee target passed under normal multithreaded tests.

Formatting, layers, scorecard consistency, corpus pin verification and explicit panic hunt passed. On 15 October, actual AMD Vulkan/DX12 mip readbacks passed for U8/U16/F32 across direct/scratch paths and partial updates. The first attempted GPU launch was not executed because automatic permission review timed out; the permitted retry launched and passed. The elapsed build interval crossed midnight with a long activity gap; continuous compiler work or its cause is not established.

Saving the candidate to integration/upstream-2026-10-14 now preserves reviewable progress while corpus-enabled tests, documentation/lint/wasm, normal app build, release timing and recorded live workflows finish. Main remains at the protected baseline. The GPU lock changes qualify test-device concurrency locally, not universal production stability. [Candidate findings and pending gates](upstream-integration-results-2026-10-14.md).

## Upstream integration completed ? 15 October 2026

Published the protected revamp checkpoint `918d422f` to PhotoCreate before merging pinned upstream `ed7df56` (750 upstream commits). Integration merge `ee75a490` preserves our shape-cache policy/generation guard, single purge, U16 mip mitigation, histogram coalescing, documentation, audit scripts and beginner-first direction. The final qualification commit adds benchmark/QA corrections, records and memory. Main is promoted by fast-forward; baseline/revamp-2026-10-14 remains restorable. No upstream push or force push is used.

Final gates: 8,396 native tests passed (68 ignored), 3,532 corpus-enabled tests passed (27 ignored), documentation tests, strict workspace clippy, 24 wasm checks, formatting, layers, scorecard, corpus pins, HEIF desktop build and explicit panic hunt passed. Wasm retains a nonfatal upstream dead-code warning. Actual AMD Vulkan and DX12 mip matrices passed. Corrected release comparison is mixed: opacity median 22.57 ? 29.49 ms, group move commit 112.71 ? 96.82 ms and smart-object commit 48.12 ? 33.62 ms. These are fixture frame/command timings, not physical p95. Upstream's changed Group default is preserved; the benchmark explicitly selects Layer and asserts the target.

Recorded layout assertions passed, with an unplanned tile displacement visible. Two high-depth brush captures failed single-undo pixel restoration after extra history entries, and a third capture timed out before editing; their cause remains unresolved and all failed records are retained. The integrated missing-sidecar recovery retry passed: completed revisions 5/6, owned-child interruption, metadata preserved/removed in the synthetic profile, three editable layers restored dirty with no invented path, native save/reopen and independent whole-image PNG oracle. Recovery footage is 1 second before and 3.5 seconds after; waits/second edit/interruption are transcript evidence. This is not power-loss or interrupted-write qualification.

[Full integration findings and limitations](upstream-integration-results-2026-10-14.md), [downloadable recordings and outputs](../records/README.md). Backlog and Obsidian-compatible local memory updated. Atelier/recipes, input-capture isolation, interaction latency, wider GPU/recovery coverage and independent Photoshop acceptance remain open. No cloud memory, AI service, upstream maintainer issue or nightly rebase was configured.
