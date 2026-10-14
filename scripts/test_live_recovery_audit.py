"""Ensure the recovery auditor accepts only a newer completed snapshot."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from live_recovery_audit import simulate_missing_sidecar, wait_snapshot


class SnapshotTests(unittest.TestCase):
    def test_missing_sidecar_simulation_preserves_metadata_and_leaves_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            folder = out / "private/config/Recovery"
            (folder / "test.pcraft").mkdir(parents=True)
            (folder / "test.pcraft/manifest.json").write_text("{}")
            (folder / "test.json").write_text('{"revision":6}')
            (out / "state").mkdir()
            backup = simulate_missing_sidecar(SimpleNamespace(out=out), {"key": "test"})
            self.assertEqual((out / backup).read_text(), '{"revision":6}')
            self.assertFalse((folder / "test.json").exists())
            self.assertTrue((folder / "test.pcraft/manifest.json").is_file())

    def test_missing_sidecar_simulation_refuses_keys_outside_owned_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            for key in ["../other", "", "test/name", "C:\\other", None]:
                with self.assertRaises(ValueError):
                    simulate_missing_sidecar(SimpleNamespace(out=Path(tmp)), {"key": key})

    def test_newer_sidecar_requires_its_bundle_and_observes_a_frame(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            folder = out / "private/config/Recovery"
            folder.mkdir(parents=True)
            (folder / "old.json").write_text(json.dumps({"key": "old", "revision": 4}))
            (folder / "old.pcraft").mkdir()
            (folder / "broken.json").write_text("unfinished")
            (folder / "incomplete.json").write_text(json.dumps({"key": "incomplete", "revision": 10}))
            wanted = {"key": "new", "revision": 5}
            (folder / "new.json").write_text(json.dumps(wanted))
            (folder / "new.pcraft").mkdir()
            audit = SimpleNamespace(out=out, state=Mock())
            self.assertEqual(wait_snapshot(audit, 5), wanted)
            audit.state.assert_called_once_with()

    def test_timeout_does_not_claim_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit = SimpleNamespace(out=Path(tmp), state=Mock())
            with self.assertRaises(TimeoutError):
                wait_snapshot(audit, 1, timeout=0)
            audit.state.assert_not_called()

    def test_wait_polls_status_each_interval_instead_of_expiring_control_socket(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit = SimpleNamespace(out=Path(tmp), state=Mock())
            with patch("live_recovery_audit.time.monotonic", side_effect=[0, 1, 2, 4]), \
                 patch("live_recovery_audit.time.sleep") as sleep:
                with self.assertRaises(TimeoutError):
                    wait_snapshot(audit, 1, timeout=3)
            self.assertEqual(audit.state.call_count, 2)
            self.assertEqual(sleep.call_count, 2)


if __name__ == "__main__":
    unittest.main()
