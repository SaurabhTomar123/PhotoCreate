# Recorded live feature audit

## Current status — 11 October 2026

Rust stable 1.99.0, Visual Studio 2022 C++ tools and FFmpeg are available. **PhotoCraft built and launched successfully. The recorded audit and repository validation are complete; validation failed on a reproducible GPU assertion and three crashed GPU targets.** The verified recording session is `dist/qa/live-verified-2026-10-11`; startup frames were extracted and visually inspected.

The inventory lists **631 menu catalog entries and 65 tools**; the running build exposes **871 engine commands**. These are inventory counts, not pass counts. Read each session's `summary.json` for its completion status and evidence levels.

## Build and run

From the repository root in PowerShell, with network access and permission to use the Rust package caches:

```powershell
& "$env:USERPROFILE\.cargo\bin\cargo.exe" build -p photocraft --locked --features heif
```

If linking reports that `link.exe` or Windows SDK libraries are missing, use Visual Studio's **Developer PowerShell for VS 2022** and run the build there. The project requires Rust 1.95 or newer. Build/test failures should be recorded before modifying product code.

After a successful build:

```powershell
python scripts/live_feature_audit.py --menu-sweep --dwell 0.6 --ffmpeg "C:\Users\Saurabh\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0-full_build\bin\ffmpeg.exe"
```

This launches a visible PhotoCraft window and drives its authenticated loopback control server. A second authenticated connection captures GPU screenshots continuously and streams them to FFmpeg at four frames per second. Frames duplicate when capture falls behind to preserve the recording timeline. This records the actual application UI, excludes other windows and has no audio. GDI window capture was rejected after an extracted frame showed a white GPU surface; the original probe and interrupted first run are diagnostic evidence only.

Use a new `--output dist/qa/run-NAME` directory for each run to preserve previous evidence. The script regenerates its report after every completed case. If startup or transport fails it records an interrupted run instead of claiming completion. Stop with Ctrl+C; cleanup attempts to finalize the video and quit only the app instance it launched.

## Deliverables

| Output | Purpose |
|---|---|
| `index.html` | Browse screenshots, cases, status and video locally |
| `live-walkthrough.mp4` | Live GPU screenshot stream at 4 fps, only if recording starts successfully |
| `recording-metadata.json`, `walkthrough.srt` | Capture health and optional caption sidecar |
| `chapters.txt` | Case start times for navigating the recording |
| `coverage.csv` | Passed/failed/restricted and unexercised entries, with coverage level |
| `results.json`, `summary.json` | Machine-readable results and run status |
| `screenshots/`, `state/` | Per-case UI screenshots and inspected state |
| `samples/` | Original synthetic fixture and attempted saved/reopened examples |
| `protocol.jsonl`, `app.log`, `recording.log` | Reproduction evidence and diagnostics |
| `catalog.json`, `live-menus.json`, `engine-commands.json` | Source inventory and live registry where available |

Outputs are local and gitignored under `dist/`. Preferences are isolated in the output directory. **Do not share the `private/` directory**, which contains the control credential and runtime configuration. Authentication tokens are excluded from the protocol transcript. The sample is generated procedurally by the script; no personal photos or bundled third-party assets are used.

## What the first pass covers

- Every tool: activation, selected-tool assertion and options screenshot.
- Pointer gestures: marquee, ten painting/retouch strokes, editable text and pixel-checked undo/redo.
- Save/reopen examples: `.pcraft`, PSD, PSB, PNG, JPEG, TIFF, WebP and OpenRaster passed; Paint.NET save was explicitly unsupported (import-only). Dimensions are checked; native/PSD/PSB layer counts are checked. A successful round trip is not independent-editor fidelity proof.
- Menu sweep: safe filter, adjustment, selection, layer, type, view, panel and theme paths. Menu-created dialogs are captured; ordinary command dialogs are applied with defaults. Specialized dialogs are opening/cancel checks until dedicated scenarios are added.
- Recovery: simulated GPU-loss UI, recorded as a smoke check.

## What “full feature testing” still requires

The harness is a broad baseline, **not exhaustive semantic acceptance of every feature**. Activation is not a gesture test; opening a dialog is not output-quality verification; an error can indicate a harness fixture mismatch rather than a product defect. Restricted and unexercised items must remain visible in the coverage ledger.

Add dedicated cases for every uncovered path: linked objects, preset imports, plugin loading, actions/batch replay, nested masks, advanced blending, paths, channels, RAW camera samples, artboards/slices, video, print, all color depths/modes, persistent preferences and actual recovery after process termination. Ambient filesystem commands and preference operations are constrained by the existing automation policy; do not bypass that policy to inflate coverage.

The final professional baseline also needs actual Photoshop re-open checks, physical tablet sessions, IME/screen-reader use, representative large-document release benchmarks and an independent review of screenshots/results. The 512×384 synthetic fixture is suitable for feature demonstrations, not performance qualification or retouching quality assessment.

Before adding features, retain the recording and saved samples from a successful run, review failures, and expand coverage until every feature relevant to your intended workflow has a meaningful assertion. A complete command inventory alone does not provide that assurance.

## Local harness validation

```powershell
python -m unittest discover -s scripts -p test_live_feature_audit.py -v
python scripts/live_feature_audit.py --inventory-only
```

These checks validate inventory extraction, PNG generation, honest unexecuted reporting, failure retention and credential redaction. They do not exercise PhotoCraft itself.


## Completed baseline and follow-up modes

See [the results report](live-feature-test-results-2026-10-11.md) for the completed 908-case, ten-session baseline and its limitations. The aggregate viewer is `dist/qa/feature-audit-2026-10-11/index.html`.

Use `--app dist/qa/photocraft-audit.exe` after copying the built executable there if compiling tests concurrently, to avoid Windows locking the Cargo output executable. The follow-up phases are `extended`, `residual`, `remaining`, `prepared` and `evaluation`; `all` runs the original broad pass, not every follow-up. Prepared cases take `--retry-results`; remaining menus take `--remaining-menus`. Preserve each run in a distinct output directory. `--animate-input` delivers successive points over UI frames.

The evaluation phase generates original transparent PNG/TGA fixtures and a bounded 150-layer document. TGA imports deliberately put alpha in a separate named channel. Its saved TGA was checked independently with Pillow during this baseline; the standard-library harness checks channel presence and successful export, rather than using Pillow itself.

`run_feature_validation.py` preserves repository command logs and continues after failures. `package_feature_audit.py` combines explicit session and validation directories; `--archive` generates a ZIP and SHA-256 manifest and excludes each session's `private/` directory. The final package includes historical failures as well as successful retests.
