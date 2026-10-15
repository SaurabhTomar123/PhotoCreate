"""Interrupted-session acceptance test using an isolated profile and synthetic artwork.

Terminates only the child app launched here, after an observed completed autosave.
Records editing before interruption and restoration after relaunch. Autosave waits
and the second edit are retained in the timestamped command transcript, not video.
No product timer bypass, personal files, or shared user preferences.
"""
import argparse
import json
import os
from pathlib import Path
import re
import time

from live_feature_audit import Audit, release_app_visible, write_json


def stop_clip(audit, name):
    audit.record_stop.set()
    audit.record_thread.join(timeout=15)
    if audit.record_thread.is_alive():
        raise RuntimeError("Recorder did not stop; refusing interruption")
    audit.recorder.wait(timeout=20)
    metadata = {"frames": audit.record_frames, "fps": audit.record_fps,
                "error": audit.record_error, "encoder_exit": audit.recorder.returncode}
    write_json(audit.out / (name + "-recording.json"), metadata)
    if metadata["error"] or metadata["encoder_exit"] or not metadata["frames"]:
        raise RuntimeError("Recording failed: " + str(metadata))
    (audit.out / "live-walkthrough.mp4").rename(audit.out / (name + ".mp4"))
    audit.recorder = None


def wait_snapshot(audit, minimum_revision, timeout=100):
    deadline = time.monotonic() + timeout
    folder = audit.out / "private/config/Recovery"
    while time.monotonic() < deadline:
        # The authenticated control connection has a deliberate 30-second idle limit.
        # Keep it active while waiting for the real 60-second autosave timer.
        audit.state()
        for path in folder.glob("*.json"):
            try:
                info = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if info["revision"] >= minimum_revision and (folder / (info["key"] + ".pcraft")).is_dir():
                # Sidecar is published after the bundle; allow completion notification a frame.
                return info
        time.sleep(1)
    raise TimeoutError("No completed recovery snapshot within the real one-minute interval")


def simulate_missing_sidecar(audit, info):
    """Preserve, then remove only our synthetic snapshot's metadata after interruption."""
    key = info.get("key", "")
    if not isinstance(key, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", key):
        raise ValueError("Invalid synthetic recovery key")
    folder = audit.out / "private/config/Recovery"
    source = folder / (key + ".json")
    backup = audit.out / "state/interrupted-sidecar.json"
    for path in [source, backup, folder / (key + ".pcraft/manifest.json")]:
        path.resolve().relative_to(audit.out.resolve())
        if path.is_symlink() or path.is_junction():
            raise ValueError("Refusing a reparse test path")
    if backup.exists() or not (folder / (key + ".pcraft/manifest.json")).is_file():
        raise ValueError("Need a committed snapshot and a new backup path")
    source.rename(backup)
    return "state/interrupted-sidecar.json"


def document_layers(state):
    """Compare inspected document data, excluding the shell's active-layer selection."""
    return [{key: value for key, value in layer.items() if key != "selected"}
            for layer in state["document"]["layers"]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", type=Path, required=True)
    parser.add_argument("--ffmpeg", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--simulate-missing-sidecar", action="store_true",
                        help="After termination, preserve/remove synthetic metadata to simulate interrupted sidecar publication")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Use a new output directory so earlier evidence remains intact")
    args.port, args.dwell, args.keep_visible = 17843, .8, True
    audit = Audit(args)
    awake_prior = None
    if os.name == "nt":
        import ctypes
        execution_state = ctypes.windll.kernel32.SetThreadExecutionState
        execution_state.argtypes = [ctypes.c_uint32]
        execution_state.restype = ctypes.c_uint32
        awake_prior = execution_state(0x80000003)
        if not awake_prior:
            raise RuntimeError("Could not hold the display awake for the recording")
    result = {"status": "failed", "scope": "completed autosaves, forced child-process termination, same-profile relaunch; not power loss or interruption mid-write"}
    try:
        audit.run_status = "running"
        audit.launch()
        audit.engine("prefs.set", {"values": {"fileHandling.autosave": True,
                     "fileHandling.autosaveMinutes": 1, "fileHandling.recoverOnLaunch": True}})
        audit.fresh()
        audit.engine("select.deselect")
        audit.call("app.save", {"path": "samples/original-master.pcraft"})
        audit.engine("shape.create", {"kind": "rect", "rect": [70, 70, 230, 210], "fill": "#ee7733"})
        audit.screenshot("first-unsaved-edit")
        stop_clip(audit, "first-edit")
        first = wait_snapshot(audit, 1)
        print("First autosave completed; creating a newer edit", flush=True)
        audit.engine("shape.create", {"kind": "rect", "rect": [290, 90, 450, 260], "fill": "#3377ee"})
        second = wait_snapshot(audit, first["revision"] + 1)
        before = audit.state()
        assert before["session"]["documents"][0]["dirty"], "Edits must still be unsaved before interruption"
        expected = [audit.engine("document.pixel", {"x": x, "y": 150}) for x in [110, 350, 490]]
        write_json(audit.out / "state/before-interruption.json", before)
        pid = audit.process.pid
        audit.process.kill()
        code = audit.process.wait(timeout=20)
        audit.rpc.close()
        audit.rpc = None
        release_app_visible(audit.visibility_lease)
        (audit.out / "private/control.token").unlink(missing_ok=True)
        result.update({"terminated_child_pid": pid, "termination_exit": code,
                       "snapshots": [first, second], "expected_pixels": expected})
        if args.simulate_missing_sidecar:
            result["simulated_missing_sidecar"] = True
            result["preserved_sidecar"] = simulate_missing_sidecar(audit, second)
        write_json(audit.out / "recovery-result.json", result)
        print("Child interrupted; relaunching the same isolated profile", flush=True)
        audit.launch()
        deadline = time.monotonic() + 60
        while not audit.state().get("document"):
            if time.monotonic() > deadline:
                raise TimeoutError("Relaunch did not recover a document")
            time.sleep(.5)
        restored = audit.state()
        if args.simulate_missing_sidecar:
            assert restored["session"]["documents"][0]["path"] is None, "Missing metadata must not invent the original save path"
        assert restored["session"]["documents"][0]["dirty"], "Recovery must not claim edits were saved to the original master"
        assert document_layers(restored) == document_layers(before), "Recovered layer data differs"
        actual = [audit.engine("document.pixel", {"x": x, "y": 150}) for x in [110, 350, 490]]
        assert actual == expected, "Recovered composite samples differ"
        audit.screenshot("recovered-editable-master")
        write_json(audit.out / "state/recovered.json", restored)
        audit.call("app.save", {"path": "samples/recovered-master.pcraft"})
        audit.call("app.save", {"path": "samples/recovered.png"})
        audit.engine("file.closeAll")
        audit.call("app.open", {"path": "samples/recovered-master.pcraft"})
        assert document_layers(audit.state()) == document_layers(before), "Saved recovered master lost layer data"
        assert [audit.engine("document.pixel", {"x": x, "y": 150}) for x in [110, 350, 490]] == expected
        audit.screenshot("recovered-master-reopened")
        time.sleep(2)
        stop_clip(audit, "after-recovery")
        result.update({"status": "passed", "actual_pixels": actual,
                       "editable_layers": len(restored["document"]["layers"])})
        audit.run_status = "completed"
    except Exception as error:
        result["error"] = f"{type(error).__name__}: {error}"
        result["app_exit_at_failure"] = audit.process.poll() if audit.process else None
        audit.run_status = "failed"
        audit.run_error = result["error"]
        raise
    finally:
        write_json(audit.out / "recovery-result.json", result)
        try:
            audit.finish()
        finally:
            if getattr(audit, "visibility_lease", None):
                release_app_visible(audit.visibility_lease)
            if awake_prior:
                write_json(audit.out / "display-awake.json", {"temporary": True,
                           "restore_succeeded": bool(execution_state(awake_prior))})


if __name__ == "__main__":
    main()
