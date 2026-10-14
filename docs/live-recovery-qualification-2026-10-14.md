# Live recovery qualification — 14 October 2026

**Passed locally:** a forced termination of the isolated PhotoCraft test process restored the latest completed autosave, retained three editable layers, and produced the expected pixels. No editor Rust code changed in this batch. Recovery already existed; this supplies live acceptance evidence and a repeatable QA harness.

[Watch the clips and open the outputs](../dist/qa/revamp-live-recovery-final-2026-10-14/review.html). [Download the evidence package](../dist/qa/photocraft-recovery-batch-2026-10-14.zip).

## Task and findings

The test used the existing shape-cache executable, an isolated test profile, and the original 512×384 RGB8 synthetic gradient/checker fixture. It saved an original native master, added an orange vector rectangle, and observed autosave revision **5**. It added a blue vector rectangle, then observed autosave revision **6** sixty seconds later. Status polls keep the authenticated connection alive during the real one-minute autosave interval; no product timer bypass was used.

After observing the newer sidecar and recovery bundle, the harness terminated **only its own child process**, without a graceful app quit. It relaunched the same isolated profile. Layer identities, names, bounds, visibility, blend/fill/opacity and types in the inspected layer data matched the pre-interruption state, and three composite samples matched exactly. Both unsaved shapes were present. The recovered document remained **dirty**, correctly avoiding a claim that the original master contained those edits.

The recovered master was saved as `samples/recovered-master.pcraft`, exported to PNG, closed and reopened. The inspected layers and pixels still matched; the reopened native document was clean. Independent Pillow rendering of the two integer-bound solid rectangles over the source PNG matched **every RGBA pixel** of the recovered 512×384 export. This is a separate pixel oracle for this fixture, not an independent native-format parser.

## Recording and failures

Successful clips: **1.0-second first edit** and **3.5-second recovery/save/reopen**, H.264 at four fps, verified with ffprobe. Screenshots were inspected visually. The second edit, actual autosave waits and process termination are recorded in the timestamped command transcript and JSON results, **not continuously filmed**. Clip duration does not measure tool latency. Temporary display-awake and app-visibility settings were released at completion.

Five earlier attempts remain retained:

- `revamp-live-recovery-2026-10-14`: an idle control connection expired before its next call; the recording encoder did not finish successfully.
- `revamp-live-recovery-awake-2026-10-14`: the same harness idle error persisted despite holding the display awake.
- `revamp-live-recovery-poll-2026-10-14`: polling fixed the control idle error, but a screenshot after the second edit timed out after 60 seconds. Quit still responded.
- `revamp-live-recovery-clips-2026-10-14` and `revamp-live-recovery-master-2026-10-14`: short initial clips succeeded, but restarting capture after idle/export or idle/autosave timed out. These are two additional retained capture attempts, bringing the total to **five failed attempts** before the successful run.

The control server deliberately limits idle sockets to 30 seconds (`crates/automation/src/security.rs`). The harness now polls once per second while waiting. Capture timeouts are a separate, unresolved finding; display sleep, occlusion, GPU/driver behavior or frame scheduling have **not** been established as their cause. Successful short capture after a fresh launch is a narrower qualification, not a product screenshot fix.

Before interruption the tab correctly displayed the modified marker, but the bottom status still displayed the previous “Saved” action message. Treat this as a save-status clarity issue for the revamp: distinguish the last action from current protection/save state. The recovered tab and status explicitly showed recovery.

## Validation and remaining work

The new recovery harness has **three passing tests**, including a regression that requires status polling during waits. The existing live-audit harness has eight passing tests. Local memory tests: fifteen passed, one real-symlink permission case skipped; the mocked refusal checks passed. Native/corpus/wasm results from the preceding cache batch remain unchanged and were not rerun for this Python-only QA addition.

F03 is **partially qualified locally**, not closed. Still required: interrupted writes, full disk/write failures, multiple dirty documents, corrupt snapshots, large/high-depth recovery, repeated kills, power loss and broader devices. F02 native GPU crashes and idle capture reliability remain open. The Atelier UI, guided creation studios and beginner usability trials remain planned.

Evidence: `dist/qa/revamp-live-recovery-final-2026-10-14/{recovery-result.json,protocol.jsonl,state/,video-verification.json,output-verification.json,source-state.json,python-validation.json}`. `private/` profiles and authentication files are excluded from the share package and memory vault. Run again with a **new** output directory:

```powershell
python scripts/live_recovery_audit.py --app dist/qa/photocraft-shape-cache.exe --ffmpeg <ffmpeg.exe> --output dist/qa/<new-recovery-run>
```
