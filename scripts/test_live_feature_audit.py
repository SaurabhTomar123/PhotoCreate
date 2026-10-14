"""Local validation of audit evidence/reporting; does not launch PhotoCraft."""

import argparse
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import zlib

from live_feature_audit import Audit, RPC, fixture, inventory, release_app_visible


class AuditTests(unittest.TestCase):
    def test_inventory_has_real_tools_and_menu_paths_without_separators(self):
        menus, tools = inventory()
        self.assertGreater(len(menus), 600)
        self.assertEqual(len(tools), len(set(tools)))
        self.assertIn("Brush", tools)
        self.assertIn("Type", tools)
        self.assertTrue(all(item["id"] != "---" and item["menu"] for item in menus))
        self.assertIn("filter.blur.gaussianBlur", {item["id"] for item in menus})

    def test_fixture_is_valid_rgb_png_with_correct_crc_and_dimensions(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.png"
            fixture(path, 48, 32)
            image = path.read_bytes()
        self.assertEqual(image[:8], b"\x89PNG\r\n\x1a\n")
        offset, payload = 8, bytearray()
        while offset < len(image):
            length = struct.unpack(">I", image[offset:offset+4])[0]
            kind = image[offset+4:offset+8]
            data = image[offset+8:offset+8+length]
            crc = struct.unpack(">I", image[offset+8+length:offset+12+length])[0]
            self.assertEqual(crc, zlib.crc32(kind + data))
            if kind == b"IHDR":
                self.assertEqual(struct.unpack(">IIBBBBB", data), (48, 32, 8, 2, 0, 0, 0))
            if kind == b"IDAT":
                payload.extend(data)
            offset += length + 12
        self.assertEqual(len(zlib.decompress(payload)), 32 * (48 * 3 + 1))

    def test_prepared_report_never_claims_live_passes_or_a_recording(self):
        with tempfile.TemporaryDirectory() as directory:
            audit = Audit(argparse.Namespace(output=Path(directory), dwell=0))
            audit.finish()
            summary = json.loads((Path(directory) / "summary.json").read_text())
            page = (Path(directory) / "index.html").read_text()
            self.assertEqual(summary["cases"], 0)
            self.assertEqual(summary["run_status"], "prepared_not_run")
            self.assertIsNone(summary["recording"])
            self.assertEqual(len(summary["uncovered_tools"]), len(audit.tools))
            self.assertNotIn("<video", page)

    def test_failed_assertion_is_retained_in_coverage(self):
        with tempfile.TemporaryDirectory() as directory:
            audit = Audit(argparse.Namespace(output=Path(directory), dwell=0))
            def fail(_):
                raise AssertionError("Undo changed the wrong pixel")
            with patch.object(audit, "screenshot", side_effect=RuntimeError("no app")):
                row = audit.case("workflow.undo", "Undo", "behavior", fail)
            audit.finish()
            self.assertEqual(row["status"], "failed")
            self.assertIn("wrong pixel", row["note"])
            rows = json.loads((Path(directory) / "results.json").read_text())
            self.assertEqual(rows[0]["status"], "failed")

    def test_rpc_auth_token_is_not_written_to_protocol_log(self):
        token = "a" * 64
        class Stream:
            def __init__(self):
                self.replies = iter([b'{"id":1,"ok":true,"result":{}}\n',
                                     b'{"id":2,"ok":false,"error":"unknown tool"}\n'])
            def write(self, _): pass
            def flush(self): pass
            def readline(self, _): return next(self.replies)
            def close(self): pass
        class Socket:
            def makefile(self, _): return Stream()
            def close(self): pass
        log = io.StringIO()
        with patch("live_feature_audit.socket.create_connection", return_value=Socket()):
            rpc = RPC(17878, token, log)
            with self.assertRaisesRegex(RuntimeError, "unknown tool"):
                rpc.call("ui.set", {"tool": "invalid"})
            rpc.close()
        self.assertNotIn(token, log.getvalue())
        self.assertIn("unknown tool", log.getvalue())


class CaptureVisibilityTests(unittest.TestCase):
    @staticmethod
    def lease(alive=True, owner=42, was_topmost=False):
        class Api:
            calls = []

            def IsWindow(self, window):
                return alive

            def GetWindowThreadProcessId(self, window, pointer):
                pointer._obj.value = owner

            def SetWindowPos(self, *args):
                self.calls.append(args)
                return True

        return {"api": Api(), "window": 7, "process_id": 42, "was_topmost": was_topmost}

    def test_destroyed_window_needs_no_restore(self):
        lease = self.lease(alive=False)
        self.assertEqual(release_app_visible(lease), {"restored": True, "window_closed": True})
        self.assertEqual(lease["api"].calls, [])

    def test_reused_handle_never_modifies_another_process(self):
        lease = self.lease(owner=99)
        result = release_app_visible(lease)
        self.assertTrue(result["handle_reused"])
        self.assertEqual(lease["api"].calls, [])

    def test_original_topmost_state_is_restored_without_focus_changes(self):
        for original, expected in [(False, -2), (True, -1)]:
            lease = self.lease(was_topmost=original)
            self.assertTrue(release_app_visible(lease)["restored"])
            call = lease["api"].calls[0]
            self.assertEqual(call[1], expected)
            self.assertEqual(call[-1], 0x13, "size, position and keyboard focus are preserved")


if __name__ == "__main__":
    unittest.main()
