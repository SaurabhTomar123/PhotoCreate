"""Ensure the recovery auditor accepts only a newer completed snapshot."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from live_recovery_audit import wait_snapshot


class SnapshotTests(unittest.TestCase):
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
