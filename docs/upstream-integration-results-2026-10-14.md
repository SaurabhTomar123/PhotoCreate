# Upstream integration qualification ? 14 October 2026

Status: integration candidate under validation; not yet promoted to main. The owner explicitly requested current-project publication to SaurabhTomar123/PhotoCreate, followed by upstream update and merge.

## Protected baseline and candidate

The existing revamp was published as commit `918d422fece281e30b9b6e61f726ce97d77c850c` to main and `baseline/revamp-2026-10-14`. Source, reports, curated memory and three privacy-filtered evidence archives are included. The original large audit archive, complete local QA data, executable copies and baseline corpus remain preserved locally.

The separate `photocraft-integration` worktree merges upstream `ed7df56a2455375240959bae6e5273a71d858d84`: 750 commits and 870 changed files from the old base. The candidate preserves our 128-entry / conservative 128 MiB shape cache, purge-generation guard, one Purge All call, U16 mip mitigation, expanded readback regression, histogram worker coalescing and benchmark diagnostics. Upstream assessments remain labelled with provenance alongside local evidence. README identifies this development fork without claiming the planned guided UI is shipped.

## Failures discovered and corrected

The first full native run had 8,385 passes, one assertion failure, 68 ignored cases and two crashed targets. Its logs remain retained; the run failed overall.

- The autosave retry test stopped at the first discoverable bundle. Upstream's new missing-sidecar discovery makes a committed bundle visible with revision zero before sidecar publication. This raced the test's assertion of the requested revision. The original test failed in three of ten isolated repetitions. It now waits for the requested revision and retains its exact revision and pixel checks. Twenty rebuilt repetitions passed. Production recovery logic was not weakened.
- The newer mid-tone checker test bypassed the GPU lock used by six other tests, and the new three-test marquee-autoscroll target had no guards. Both binaries crashed with STATUS_ACCESS_VIOLATION. Adding the existing per-process GPU guard for each test's full lifetime corrected those observed failures. Tests remain multithreaded; the device-owning regions serialize. This does not establish a universal production GPU crash fix.
- A fresh-checkout memory note depended on an ignored historical log. It now cites the committed baseline report so provenance validation works without local QA artifacts. The original log remains preserved.

## Verified so far

The corrected full native workspace run passed **8,396 tests, zero failures, zero native crashes, 68 ignored**, across 250 result groups. The prior crash targets checker_canvas (7), color_managed_canvas (2), full_res_preview (3), and the newly failing marquee_autoscroll (3) passed. Counts describe test executions, not unique real files or exhaustive professional readiness.

Formatting, dependency layers, scorecard consistency and pinned corpus verification passed. Explicit adversarial-input panic hunt passed. Python recovery auditor: five tests passed, including bounded missing-sidecar simulation and invalid-key refusal. Existing audit/memory checks passed with the known real-symlink permission skip.

The first full build took 4,680.3 seconds; the corrected cached native run took 1,043.13 seconds. These are logged elapsed durations. To maintain storage headroom, 16.28 GiB of verified generated executables/PDBs from the inactive old test cache were removed. Baseline UI test executables, root application copies, release benchmark copies, source, recordings, active integration targets and corpora were preserved. Compact debug settings reduced new build storage but Windows still produced symbols and many executable files.

## Remaining before promotion

Corpus-enabled tests, documentation tests, strict workspace lint, L0?L6 wasm checks, the desktop build, Vulkan/DX12 mip qualification, fresh release comparison and recorded live workflows are pending. The candidate will not be promoted based only on the passing native count. Baseline timings remain historical, and current ignored/hardware/Photoshop-acceptance limitations remain open.

Logs and source information are retained in the development checkout's dist/qa/upstream-integration-* directories. Completed qualification and shareable records will be appended here before the merge is promoted.
