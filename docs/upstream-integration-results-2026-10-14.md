# Upstream integration qualification ? 14?15 October 2026

Status (15 October): upstream integration qualified with the bounded results below. The owner explicitly requested current-project publication to SaurabhTomar123/PhotoCreate, followed by upstream update and merge. The protected baseline remains available separately; this is development integration, not a professional-readiness certification.

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

## Completed integration checks (15 October)

Corpus-enabled tests passed: **3,532 passed, zero failures, 27 ignored** across 156 result groups. Documentation tests, strict workspace/all-target clippy with HEIF, all 24 wasm checks and the HEIF desktop build passed. The wasm checks retain an upstream nonfatal `PAR_PIXELS` dead-code warning; native strict clippy was clean. Explicit panic hunt passed. After the benchmark-only adjustment, formatting and strict example clippy also passed again. Recovery auditor unit tests now total six, including a regression proving selection-only changes are ignored while changed document bounds still fail.

The mip readback matrix passed separately on actual AMD Radeon integrated graphics through both Vulkan and DX12. It covers U8/U16/F32, three sizes, three alpha cases, direct/scratch paths, 54 base cases and 162 partial updates, compared with full mip regeneration. This is one adapter, not qualification of every GPU or device-loss recovery.

The integrated release example compiled. The first auto-select comparison was invalid for like-for-like layer timing: upstream changed the product default from Layer to Group. Its logs remain retained and explicitly labelled. The benchmark now explicitly requests Layer and asserts the headline is selected. This changes the benchmark only; the product default remains Group.

The corrected quiet pair uses the same AMD Vulkan adapter, 12 MP / 174 layers / 60 text layers, GPU synchronization, PSD roundtrip and nine repetitions. Selected median / p90 milliseconds:

| Interaction | Preserved baseline | Integrated |
|---|---:|---:|
| Text visibility | 22.26 / 27.62 | 24.63 / 28.40 |
| Group visibility | 28.07 / 32.75 | 31.77 / 32.37 |
| Opacity | 22.57 / 25.23 | 29.49 / 38.66 |
| Pixel move commit | 26.99 / 29.86 | 31.85 / 33.60 |
| Shape move commit | 3.13 / 26.84 | 3.76 / 33.51 |
| Group move commit | 112.71 / 139.92 | 96.82 / 106.77 |
| Smart-object move commit | 48.12 / 57.03 | 33.62 / 49.89 |
| Canvas layer selection | 93.77 / 164.72 | 119.35 / 125.40 |
| Auto-selected type drag | 3.26 / 50.35 | 3.43 / 73.29 |
| Auto-selected type commit | 96.34 / 118.63 | 90.30 / 98.36 |

Results are mixed and several operations still exceed smooth-interaction budgets. These are instrumented frame/command timings, not physical input-to-display p95, and nine samples do not establish a universal regression or improvement. The preserved baseline already contains our cache fix; the historical 398-to-25 ms improvement compares a different earlier baseline.

## Live recordings and open failures

The integrated 12 MP layout case passed its sampled opacity/restore, shape bounds, undo/redo, native save/reopen, PNG export and Purge All assertions. A 15.75-second recording and screenshots are retained. Visual inspection found a displaced tile beyond the planned grid, so the case is not claimed as an independent whole-image match to the historical layout. Unplanned edits also appeared in an interrupted-recovery attempt; their origin is unproven.

Two high-depth live brush attempts failed the single-undo pixel restoration assertion; an additional Brush Tool history entry appeared during zoom/capture. A third attempt using Move during navigation timed out before editing. All three failed records remain retained. The passing hardware mip tests do not close this live input/capture issue. Do not label it a proven core undo defect or blame user input without evidence. A navigation-history assertion was added to the auditor, but has not yet passed a complete live run.

The first missing-sidecar recovery attempt restored matching inspected document fields, but failed because it compared the transient selected-layer UI flag as document content. The auditor now excludes only that flag, with a unit regression; layer order, IDs, bounds, opacity and pixels remain checked. Missing-sidecar simulation renames metadata only inside the owned synthetic profile after a completed autosave and owned-child termination. It is not an actual power-loss or mid-write test.

The final missing-sidecar retry **passed** after completed autosave revisions 5 and 6. Same-profile relaunch restored all three editable layers and exact sampled pixels, marked the document dirty and did not invent an original save path. The recovered native master saved and reopened with matching inspected document fields and samples. An independent Pillow oracle matched **every pixel of the 512 × 384 RGBA export**. Screenshot inspection confirmed the two expected rectangles and three-layer master. PNG flattening was explicitly warned, as expected. Short first-edit and recovery/save/reopen clips are supplied; the second edit, autosave waits and interruption are in the timestamped transcript, not continuous footage.

Logged elapsed build/test durations span long host/activity gaps; they are not continuous CPU measurements. The first release build result was preserved separately after its detailed log was reused for the benchmark-only rebuild. Initial failures, warnings and mismatched workloads remain part of the evidence.

## Conclusion and scope

The integrated development branch preserves the local revamp fixes and imports the pinned upstream work. It does not deliver the planned Atelier, guided recipes, command planner, AI/ML or universal Photoshop parity. The remaining priorities are the live input/capture issue, latency, wider GPU/recovery qualification, external PSD acceptance and one complete beginner-first recipe. Main promotion is a fast-forward of this reviewed merge, with the baseline branch retained and no force push.

Logs and source information are retained in the development checkout's dist/qa/upstream-integration-* directories. Completed qualification and shareable records will be appended here before the merge is promoted.
