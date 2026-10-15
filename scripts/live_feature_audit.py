"""Record and audit a real PhotoCraft desktop session over its authenticated control API.

Uses only Python's standard library. Reports coverage levels rather than equating
successful command dispatch with full feature correctness. Outputs stay in dist/qa.
Run with --help. --inventory-only does not launch an app or access the network.
"""

import argparse
import collections
import csv
import html
import json
import math
import os
from pathlib import Path
import re
import socket
import struct
import subprocess
import time
import threading
import zlib


ROOT = Path(__file__).resolve().parents[1]


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def inventory():
    source = (ROOT / "crates/ui-egui/src/menu_catalog.rs").read_text(encoding="utf-8")
    menus = []
    for line in source.splitlines():
        match = re.search(r'\(&\[([^]]*)\],\s*"([^"]*)",.*?"([^"\s]+)"\),\s*$', line)
        if match and match[3] != "---":
            menus.append({"id": match[3], "label": match[2],
                          "menu": re.findall(r'"([^"]+)"', match[1])})
    source = (ROOT / "crates/ui-egui/src/state.rs").read_text(encoding="utf-8")
    block = source.split("pub const ALL: [Tool;", 1)[1].split("];", 1)[0]
    tools = re.findall(r"Tool::(\w+)", block)
    return menus, tools


def fixture(path, width=512, height=384):
    """Original synthetic gradient, checker, disks and lines; no personal assets."""
    rows = bytearray()
    for y in range(height):
        rows.append(0)
        for x in range(width):
            rgb = [int(35 + 150 * x / width), int(35 + 160 * y / height),
                   65 + 70 * ((x // 32 + y // 32) % 2)]
            if (x - 160) ** 2 + (y - 145) ** 2 < 70 ** 2:
                rgb = [235, 95, 45]
            if 310 < x < 440 and 70 < y < 230:
                rgb = [35, 180, 210]
            if abs(y - (x * 0.35 + 210)) < 3:
                rgb = [240, 240, 225]
            rows.extend(rgb)
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))


class RPC:
    def __init__(self, port, token, log):
        self.sock = socket.create_connection(("127.0.0.1", port), timeout=70)
        self.stream = self.sock.makefile("rwb")
        self.log = log
        self.index = 0
        self.call("auth", {"token": token}, record=False)

    def call(self, method, params=None, record=True):
        self.index += 1
        request = {"id": self.index, "method": method, "params": params or {}}
        started = time.perf_counter()
        self.stream.write((json.dumps(request) + "\n").encode())
        self.stream.flush()
        line = self.stream.readline(9 * 1024 * 1024)
        if not line:
            raise ConnectionError("PhotoCraft closed the control connection")
        response = json.loads(line)
        if record:
            self.log.write(json.dumps({"time": time.time(), "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
                                       "request": request, "response": response}, ensure_ascii=False) + "\n")
            self.log.flush()
        if not response.get("ok"):
            raise RuntimeError(response.get("error", str(response)))
        return response.get("result")

    def close(self):
        try:
            self.stream.close()
        except OSError:
            pass
        finally:
            self.sock.close()


class Audit:
    def __init__(self, args):
        self.args = args
        self.out = args.output.resolve()
        for directory in ["screenshots", "samples", "state", "private"]:
            (self.out / directory).mkdir(parents=True, exist_ok=True)
        self.menus, self.tools = inventory()
        self.rows = []
        self.command_calls = collections.Counter()
        self.engine_catalog = []
        self.process = self.recorder = self.rpc = None
        self.started = time.time()
        self.recording_started = None
        self.run_status = "prepared_not_run"
        self.run_error = None
        self.log = (self.out / "protocol.jsonl").open("w", encoding="utf-8")
        self.app_log = (self.out / "app.log").open("w", encoding="utf-8")
        self.record_log = (self.out / "recording.log").open("w", encoding="utf-8")
        fixture(self.out / "samples/fixture.png")
        write_json(self.out / "catalog.json", {"menus": self.menus, "tools": self.tools})

    def call(self, method, params=None):
        if method in ["engine.execute", "ui.menu.invoke"]:
            identifier = (params or {}).get("command" if method == "engine.execute" else "id")
            if identifier:
                self.command_calls[identifier] += 1
        return self.rpc.call(method, params)

    def engine(self, command, params=None):
        return self.call("engine.execute", {"command": command, "params": params or {}})

    def state(self):
        return self.call("ui.inspect")

    def screenshot(self, name):
        relative = "screenshots/" + re.sub(r"[^a-zA-Z0-9_-]", "-", name)[:140] + ".png"
        self.call("ui.screenshot", {"path": relative})
        if not (self.out / relative).is_file():
            raise AssertionError("Screenshot reply did not produce a file")
        return relative

    def cleanup_ui(self):
        state = self.state()
        for dialog in reversed(state.get("dialogs", [])):
            self.call("ui.dialog.cancel", {"dialog": dialog["id"]})
        self.call("ui.key", {"key": "Escape"})
        if state.get("cameraRaw"):
            self.call("ui.menu.invoke", {"id": "filter.cameraRaw", "params": {"ui": {"cancel": True}}})
        self.call("ui.set", {"tool": "move"})

    def fresh(self, context="raster"):
        self.cleanup_ui()
        state = self.state()
        if state.get("session", {}).get("documents"):
            self.engine("file.closeAll")
        self.call("app.open", {"path": "samples/fixture.png"})
        if context != "background":
            self.engine("layer.new.layerFromBackground")
        self.call("ui.set", {"fit": True, "tool": "move"})
        if context == "text":
            self.engine("type.create", {"x": 55, "y": 170, "text": "PhotoCraft", "size": 48, "color": "#ffffff"})
        elif context == "smart":
            self.engine("layer.smartObjects.convertToSmartObject")
        elif context == "shape":
            self.engine("shape.create", {"kind": "rect", "rect": [80, 80, 260, 200], "fill": "#ffaa44"})
        elif context == "group":
            self.engine("layer.duplicate")
            self.engine("layer.groupLayers", {"name": "Audit group"})
        if context != "text":
            self.engine("select.rect", {"x": 65, "y": 65, "width": 300, "height": 220})

    def case(self, identifier, title, level, function):
        if getattr(self.args, "case_filter", "") and self.args.case_filter not in identifier:
            return None
        if getattr(self, "record_error", None):
            raise RuntimeError("Live recording failed: " + self.record_error)
        number = len(self.rows) + 1
        print(f"[{number}] {identifier}: {title}", flush=True)
        row = {"id": identifier, "title": title, "level": level, "status": "failed",
               "seconds": round(time.time() - (self.recording_started or self.started), 2), "evidence": [], "note": ""}
        before = time.perf_counter()
        try:
            result = function(row) or ""
            if row["status"] == "failed":
                row["status"] = "passed"
            row["note"] = result
        except (RuntimeError, AssertionError, ValueError, KeyError) as error:
            row["note"] = str(error)
            text = str(error).lower()
            if any(word in text for word in ["automation", "disabled", "unsupported", "not supported", "not implemented", "not available right now"]):
                row["status"] = "restricted_or_unsupported"
            try:
                row["evidence"].append(self.screenshot(f"{number:04d}-failure"))
            except Exception:
                pass
        row["elapsed_ms"] = round((time.perf_counter() - before) * 1000, 2)
        self.rows.append(row)
        self.report()
        print(f"  {row['status']}: {row['note'][:180]}", flush=True)
        return row

    def capture(self, row, label="after"):
        time.sleep(self.args.dwell)
        row["evidence"].append(self.screenshot(f"{len(self.rows)+1:04d}-{row['id']}-{label}"))
        write_json(self.out / "state" / f"{len(self.rows)+1:04d}-{label}.json", self.state())

    def launch(self):
        if not self.args.app or not self.args.app.is_file():
            raise FileNotFoundError("Build PhotoCraft first, or supply --app PATH")
        env = os.environ.copy()
        env["PHOTOCRAFT_CONFIG_DIR"] = str(self.out / "private/config")
        token_file = self.out / "private/control.token"
        self.process = subprocess.Popen([str(self.args.app.resolve()), "--control", str(self.args.port),
            "--control-token-file", str(token_file), "--automation-read-root", str(self.out),
            "--automation-write-root", str(self.out)], cwd=ROOT, env=env, stdout=self.app_log, stderr=self.app_log)
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                raise RuntimeError(f"PhotoCraft exited with {self.process.returncode}; see app.log")
            if token_file.exists():
                try:
                    self.rpc = RPC(self.args.port, token_file.read_text().strip(), self.log)
                    break
                except (OSError, ValueError):
                    pass
            time.sleep(0.5)
        else:
            raise TimeoutError("PhotoCraft control server did not become ready")
        self.call("ui.resize", {"width": 1280, "height": 800})
        self.call("ui.focus")
        write_json(self.out / "initial-state.json", self.state())
        self.engine_catalog = self.call("engine.commands")
        write_json(self.out / "engine-commands.json", self.engine_catalog)
        write_json(self.out / "live-menus.json", self.call("ui.menu.list"))
        if getattr(self.args, "keep_visible", False) and os.name == "nt":
            self.visibility_lease = hold_app_visible(self.process.pid)
            write_json(self.out / "window-visibility.json", {"temporary": True, "set_succeeded": True,
                       "was_topmost": self.visibility_lease["was_topmost"], "process_id": self.process.pid})
        if self.args.ffmpeg:
            self.start_recording()

    def start_recording(self):
        # GDI window capture misses wgpu pixels. Stream real GPU screenshots
        # from a second authenticated connection, excluding other windows.
        self.record_stop = threading.Event()
        self.record_error = None
        self.record_frames = 0
        self.record_fps = 4
        self.recorder = subprocess.Popen([str(self.args.ffmpeg), "-hide_banner", "-loglevel", "warning",
            "-y", "-f", "image2pipe", "-framerate", str(self.record_fps), "-vcodec", "png", "-i", "pipe:0",
            "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-c:v", "libx264", "-preset", "ultrafast",
            "-crf", "23", "-pix_fmt", "yuv420p", str(self.out / "live-walkthrough.mp4")],
            stdin=subprocess.PIPE, stdout=self.record_log, stderr=self.record_log,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        token = (self.out / "private/control.token").read_text().strip()
        recording_rpc = RPC(self.args.port, token, None)
        frame_path = self.out / "private/recording-frame.png"
        recording_rpc.call("ui.screenshot", {"path": "private/recording-frame.png"}, record=False)
        first_frame = frame_path.read_bytes()
        self.recording_started = time.time()
        def record():
            previous = first_frame
            try:
                while not self.record_stop.is_set():
                    target = int((time.time() - self.recording_started) * self.record_fps)
                    while self.record_frames <= target:
                        self.recorder.stdin.write(previous)
                        self.record_frames += 1
                    self.recorder.stdin.flush()
                    if self.record_stop.wait(1 / self.record_fps):
                        break
                    recording_rpc.call("ui.screenshot", {"path": "private/recording-frame.png"}, record=False)
                    previous = frame_path.read_bytes()
            except Exception as error:
                self.record_error = str(error)
            finally:
                recording_rpc.close()
                self.recorder.stdin.close()
        self.record_thread = threading.Thread(target=record, daemon=True)
        self.record_thread.start()

    def tool_cases(self):
        for tool in self.tools:
            def activate(row, tool=tool):
                self.cleanup_ui()
                self.call("ui.set", {"tool": tool})
                actual = self.state()["tool"]
                assert actual == tool, f"Expected tool {tool}, got {actual}"
                self.capture(row)
                return "Tool selected and options captured. Gesture/output correctness not established by this activation test."
            self.case("tool." + tool, tool + " options and activation", "activation", activate)

    def gesture_cases(self):
        """Exercise every tool's canvas path; assert only observable state changes."""
        for tool in self.tools:
            def gesture(row, tool=tool):
                self.fresh("shape" if tool in ["PathSelection", "DirectSelection", "AddAnchorPoint", "DeleteAnchorPoint"] else "raster")
                self.engine("select.deselect")
                self.call("ui.set", {"tool": tool, "brushSize": 32})
                before = self.state()
                if tool in ["CloneStamp", "Healing"]:
                    self.pointer(tool, [(150, 130), (150, 130)], {"alt": True})
                if tool in ["Type", "VerticalType", "HorizontalTypeMask", "VerticalTypeMask"]:
                    self.pointer(tool, [(70, 180), (70, 180)])
                    self.call("ui.type", {"text": "Craft"})
                    self.call("ui.key", {"key": "Enter", "command": True})
                elif tool in ["PolygonLasso", "MagneticLasso", "Pen", "FreeformPen", "CurvaturePen"]:
                    for x, y in [(85, 85), (280, 85), (280, 250), (85, 250), (85, 85)]:
                        self.pointer(tool, [(x, y), (x, y)])
                    self.call("ui.key", {"key": "Enter"})
                elif tool in ["Eyedropper", "Count", "Note", "SingleRowMarquee", "SingleColumnMarquee", "Zoom"]:
                    self.pointer(tool, [(155, 140), (155, 140)])
                else:
                    self.pointer(tool, [(95, 100), (135, 125), (180, 150), (240, 195), (310, 255)])
                    if tool in ["Crop", "PerspectiveCrop"]:
                        self.capture(row, "preview")
                        self.call("ui.key", {"key": "Enter"})
                after = self.state()
                relevant = lambda s: {key: s.get(key) for key in ["document", "views", "textEdit", "magnetic", "perspectiveCrop", "distort"]}
                changed = relevant(before) != relevant(after) or before.get("session", {}).get("foreground") != after.get("session", {}).get("foreground")
                self.capture(row)
                if not changed:
                    row["status"] = "needs_dedicated_fixture"
                    return "Gesture delivered, but no relevant state change established. Needs tool-specific setup or manual validation."
                return "Canvas gesture produced an observable document/tool/view change. Recorded for review; artistic quality and complete tool semantics not asserted."
            self.case("gesture." + tool, tool + " canvas demonstration", "gesture_smoke", gesture)

    def pointer(self, tool, points, modifiers=None):
        events = [{"kind": "down" if i == 0 else "up" if i == len(points)-1 else "move",
                   "x": p[0], "y": p[1], "pressure": p[2] if len(p) > 2 else 0.7}
                  for i, p in enumerate(points)]
        if getattr(self.args, "animate_input", False):
            for event in events:
                result = self.call("ui.pointer", {"tool": tool, "events": [event], "modifiers": modifiers or {}})
                time.sleep(.06)
            return result
        return self.call("ui.pointer", {"tool": tool, "events": events, "modifiers": modifiers or {}})

    def functional_cases(self):
        def selection(row):
            self.fresh()
            self.engine("select.deselect")
            self.pointer("RectMarquee", [(75, 75), (180, 130), (290, 220)])
            d = self.state()["document"]
            assert d["hasSelection"] and d["selectionBounds"], "Marquee failed to produce selection"
            self.capture(row)
            return "Real UI marquee drag created selection; bounds recorded."
        self.case("workflow.marquee", "Draw a rectangular selection", "behavior", selection)

        for tool in ["Brush", "Pencil", "Eraser", "ColorReplacement", "Blur", "Sharpen", "Smudge", "Dodge", "Burn", "Sponge"]:
            def stroke(row, tool=tool):
                self.fresh()
                self.engine("select.deselect")
                self.call("ui.set", {"tool": tool, "brushSize": 28})
                before = self.state()["document"]["revision"]
                self.pointer(tool, [(90+i*10, 260+25*math.sin(i/3), 0.2+0.7*i/25) for i in range(26)])
                after = self.state()["document"]
                assert after["revision"] > before, "Stroke did not change document revision"
                assert after["canUndo"], "Stroke did not create an undoable edit"
                self.capture(row)
                return "UI stroke committed an undoable edit. Visual quality and real tablet response require manual review."
            self.case("workflow.stroke." + tool, tool + " pressure-ramp stroke", "behavior", stroke)

        def text(row):
            self.fresh()
            self.engine("select.deselect")
            self.pointer("Type", [(60, 145), (60, 145)])
            self.call("ui.type", {"text": "PhotoCraft Live Test"})
            self.call("ui.key", {"key": "Enter", "command": True})
            layers = self.state()["document"]["layers"]
            assert any(str(l["kind"]).lower() in ["text", "type"] for l in layers), "No live type layer created"
            self.capture(row)
            return "Pointer and text input created a type layer; text/state captured for review."
        self.case("workflow.type", "Create editable text on the canvas", "behavior", text)

        def undo(row):
            self.fresh()
            self.engine("select.deselect")
            before = self.engine("document.pixel", {"x": 150, "y": 280})
            self.pointer("Brush", [(100, 280), (150, 280), (210, 280)])
            painted = self.engine("document.pixel", {"x": 150, "y": 280})
            assert before != painted, "Brush did not change the sampled composite pixel"
            self.capture(row, "paint")
            self.engine("edit.undo")
            assert self.engine("document.pixel", {"x": 150, "y": 280}) == before, "Undo did not restore original pixel"
            self.capture(row, "undo")
            self.engine("edit.redo")
            assert self.engine("document.pixel", {"x": 150, "y": 280}) == painted, "Redo did not restore painted pixel"
            self.capture(row, "redo")
            return "Composite pixel restored exactly through undo and redo."
        self.case("workflow.undo-redo", "Paint, undo and redo", "behavior", undo)

        for extension in ["pcraft", "psd", "psb", "png", "jpg", "tiff", "webp", "ora", "pdn"]:
            def roundtrip(row, extension=extension):
                self.fresh("text")
                original = self.state()["document"]
                path = f"samples/roundtrip.{extension}"
                saved = self.call("app.save", {"path": path})
                assert (self.out / path).exists(), "Save produced no output file"
                self.call("app.open", {"path": path})
                restored = self.state()["document"]
                assert (restored["width"], restored["height"]) == (original["width"], original["height"]), "Dimensions changed"
                if extension in ["pcraft", "psd", "psb"]:
                    assert len(restored["layers"]) == len(original["layers"]), "Layer count changed"
                self.capture(row)
                return "Saved and reopened; dimensions checked" + ("; layer count checked" if extension in ["pcraft", "psd", "psb"] else "") + ". Warnings: " + json.dumps(saved.get("warnings", [])) + ". Independent-editor fidelity not tested."
            self.case("workflow.save." + extension, "Save and reopen " + extension.upper(), "roundtrip", roundtrip)

    def menu_cases(self):
        for item in self.menus:
            identifier = item["id"]
            # No ambient file dialogs, external help links, shutdown, destructive
            # preference reset, or clipboard access. Record these gaps explicitly.
            if not identifier.startswith(("filter.", "image.adjustments.", "select.", "layer.", "type.", "view.", "window.panel.", "window.theme.")):
                continue
            if any(part in identifier.lower() for part in ["export", "relink", "replacecontents", "reveal", "import", "delete", "clear", "purge"]):
                continue
            context = "text" if identifier.startswith("type.") else "smart" if "smartFilter" in identifier else "raster"
            def exercise(row, item=item, context=context):
                self.fresh(context)
                before = self.state()
                result = self.call("ui.menu.invoke", {"id": item["id"], "wait": True})
                state = self.state()
                self.capture(row, "opened")
                dialogs = state.get("dialogs", [])
                if dialogs:
                    for dialog in dialogs:
                        # Record actual menu-created UI. Preview/apply only normal
                        # command dialogs; unknown forms stay open/cancel smoke tests.
                        if str(dialog.get("kind", "")).lower() in ["command", "filter", "adjustment"]:
                            self.call("ui.dialog.confirm", {"dialog": dialog["id"]})
                            self.capture(row, "applied")
                            return "Menu opened its dialog and default settings applied. Non-default behavior and output quality not asserted."
                    self.cleanup_ui()
                    return "Menu opened UI; opening/cancel verified. Applying this specialized dialog is not covered."
                changed = self.state() != before
                return "Menu invoked; " + ("UI/document state changed." if changed else "no state change established.") + " This is a smoke test, not a full semantic assertion. Result: " + json.dumps(result)[:250]
            self.case(identifier, " > ".join(item["menu"] + [item["label"]]), "menu_smoke", exercise)

    def fallback_case(self):
        def fallback(row):
            self.fresh()
            result = self.call("ui.gpu.simulateLoss")
            self.capture(row)
            return "Device loss simulated. Renderer/recovery state recorded: " + json.dumps(result)[:300]
        self.case("workflow.gpu-fallback", "Simulate GPU loss and capture recovery UI", "recovery_smoke", fallback)

    def retry_cases(self, path):
        prior = json.loads(path.read_text(encoding="utf-8"))
        catalog = {item["id"]: item for item in self.menus}
        for old in prior:
            identifier = old["id"]
            if old["status"] == "passed" or identifier not in catalog:
                continue
            if not identifier.startswith(("layer.layerMask.", "layer.vectorMask.", "layer.layerStyle.", "layer.smartObjects.", "layer.smartFilter.")):
                continue
            if any(word in identifier.lower() for word in ["relink", "export", "replace", "finder"]):
                continue
            def retry(row, identifier=identifier):
                self.fresh("smart" if identifier.startswith(("layer.smartObjects.", "layer.smartFilter.")) else "raster")
                if identifier.startswith("layer.layerMask."):
                    self.engine("layer.layerMask.revealSelection")
                elif identifier.startswith("layer.vectorMask."):
                    self.engine("path.set", {"path": {"subpaths": [{"closed": True, "knots": [[80, 80], [260, 80], [260, 200], [80, 200]]}]}})
                    if not identifier.endswith("currentPath"):
                        self.engine("layer.vectorMask.currentPath")
                elif identifier.startswith("layer.layerStyle."):
                    self.engine("layer.layerStyle.dropShadow", {"size": 12, "distance": 15})
                elif identifier.startswith("layer.smartFilter."):
                    self.engine("filter.blur.gaussianBlur", {"radius": 4})
                self.call("ui.menu.invoke", {"id": identifier, "wait": True})
                self.capture(row, "opened")
                for dialog in self.state().get("dialogs", []):
                    if str(dialog.get("kind", "")).lower() in ["command", "filter", "adjustment"]:
                        self.call("ui.dialog.confirm", {"dialog": dialog["id"]})
                        self.capture(row, "applied")
                self.cleanup_ui()
                return "Retested with required mask/path/effect/smart-object fixture. Menu smoke evidence; complete semantic behavior not certified."
            self.case(identifier, "Prepared fixture: " + catalog[identifier]["label"], "menu_smoke", retry)

    def extended_cases(self):
        for identifier, params in [
            ("filter.distort.displace", {"horizontal": 18, "vertical": 12, "mapPath": str(self.out / "samples/fixture.png")}),
            ("filter.vanishingPoint", {"planes": [{"corners": [[70, 70], [440, 80], [420, 320], [90, 300]]}], "clone": [{"source": [145, 130], "points": [[300, 230], [315, 240], [330, 250]], "size": 35}], "newLayer": True}),
        ]:
            def supplied(row, identifier=identifier, params=params):
                self.fresh()
                before = self.state()["document"]["revision"]
                self.engine(identifier, params)
                assert self.state()["document"]["revision"] > before, "Prepared filter did not commit an edit"
                self.capture(row)
                return "Supplied required map/plane data and verified an undoable document revision. Artistic quality requires review."
            self.case("extended." + identifier, "Prepared filter: " + identifier, "behavior", supplied)

        for identifier, field, value in [("image.adjustments.brightnessContrast", "brightness", 45), ("filter.blur.gaussianBlur", "radius", 12)]:
            def nondefault(row, identifier=identifier, field=field, value=value):
                self.fresh()
                before = self.engine("document.pixel", {"x": 120, "y": 95})
                self.call("ui.menu.invoke", {"id": identifier, "wait": True})
                dialogs = self.state()["dialogs"]
                assert dialogs, "Menu did not open a parameter dialog"
                dialog = dialogs[-1]["id"]
                self.call("ui.dialog.set", {"dialog": dialog, "field": field, "value": value})
                self.capture(row, "preview")
                self.call("ui.dialog.confirm", {"dialog": dialog})
                after = self.engine("document.pixel", {"x": 120, "y": 95})
                assert after != before, "Non-default dialog settings did not change sampled pixel"
                self.capture(row, "applied")
                return "Changed dialog parameter, applied and verified an altered composite pixel."
            self.case("extended.parameters." + identifier, "Non-default dialog: " + identifier, "behavior", nondefault)

        def native_drag():
            import ctypes
            from ctypes import wintypes
            user32 = ctypes.windll.user32
            user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
            user32.GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
            user32.ClientToScreen.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.POINT)]
            user32.GetForegroundWindow.restype = wintypes.HWND
            self.call("ui.focus")
            hwnd = user32.GetForegroundWindow()
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            assert pid.value == self.process.pid, "PhotoCraft does not own the foreground window"
            rect, origin = wintypes.RECT(), wintypes.POINT(0, 0)
            user32.GetClientRect(hwnd, ctypes.byref(rect))
            user32.ClientToScreen(hwnd, ctypes.byref(origin))
            old = wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(old))
            try:
                user32.SetCursorPos(origin.x + int(rect.right * .31), origin.y + int(rect.bottom * .42))
                user32.mouse_event(2, 0, 0, 0, 0)
                for i in range(1, 16):
                    user32.SetCursorPos(origin.x + int(rect.right * (.31 + .11*i/15)), origin.y + int(rect.bottom * (.42 + .20*i/15)))
                    time.sleep(.04)
            finally:
                user32.mouse_event(4, 0, 0, 0, 0)
                user32.SetCursorPos(old.x, old.y)
            time.sleep(.3)

        for tool, property_name in [("Hand", "center"), ("RotateView", "rotation")]:
            def view_gesture(row, tool=tool, property_name=property_name):
                self.fresh()
                self.call("ui.set", {"tool": tool})
                before = self.state()["views"][0][property_name]
                native_drag()
                assert self.state()["views"][0][property_name] != before, "Native mouse drag did not change " + property_name
                self.capture(row)
                return "Native Windows mouse drag changed view " + property_name + "; foreground ownership checked before input."
            self.case("extended." + tool, tool + " with a native mouse drag", "behavior", view_gesture)

        for tool in ["AddAnchorPoint", "DeleteAnchorPoint", "DirectSelection"]:
            def anchors(row, tool=tool):
                self.fresh()
                self.engine("path.set", {"path": {"subpaths": [{"closed": True, "knots": [[80, 80], [260, 80], [260, 200], [80, 200]]}]}})
                before = self.engine("path.info")
                points = [(170, 80), (170, 80)] if tool == "AddAnchorPoint" else [(80, 80), (80, 80)] if tool == "DeleteAnchorPoint" else [(80, 80), (100, 110), (115, 130)]
                self.pointer(tool, points)
                assert self.engine("path.info") != before, "Anchor gesture did not change prepared path"
                self.capture(row)
                return "Prepared work path changed through the tool gesture; before/after path retained in protocol."
            self.case("extended." + tool, tool + " on a prepared work path", "behavior", anchors)

        for identifier, context in [("layer.new.layerFromBackground", "background"), ("layer.new.artboardFromGroup", "group")]:
            def prepared(row, identifier=identifier, context=context):
                self.fresh(context)
                self.call("ui.menu.invoke", {"id": identifier, "wait": True})
                self.capture(row)
                for dialog in self.state().get("dialogs", []):
                    self.call("ui.dialog.confirm", {"dialog": dialog["id"]})
                    self.capture(row, "applied")
                return "Repeated with the required fixture; menu dispatch/dialog application verified."
            self.case(identifier, "Prepared fixture: " + identifier, "menu_smoke", prepared)

        def freeform(row):
            self.fresh()
            self.engine("select.deselect")
            self.pointer("FreeformPen", [(80+i*8, 160+55*math.sin(i/5)) for i in range(40)])
            paths = self.engine("path.list")
            assert paths.get("workPath"), "Continuous freeform stroke produced no work path"
            self.capture(row)
            return "Continuous pointer stroke created a work path; path structure retained in protocol."
        self.case("extended.FreeformPen", "Freeform pen with a continuous stroke", "behavior", freeform)

        def zoom(row):
            self.fresh()
            self.call("ui.set", {"tool": "Zoom"})
            before = self.state()["views"][0]["zoom"]
            self.call("ui.click", {"x": 480, "y": 390})
            assert self.state()["views"][0]["zoom"] != before, "Zoom click did not change view zoom"
            self.capture(row)
            return "Screen-coordinate synthetic click changed canvas zoom through the rendered UI."
        self.case("extended.Zoom", "Zoom through a screen-coordinate canvas click", "behavior", zoom)

        def mask(row):
            self.fresh()
            self.engine("layer.layerMask.revealSelection")
            assert self.state()["document"]["layers"][0]["hasMask"], "Selection mask missing"
            self.capture(row, "masked")
            self.engine("layer.layerMask.edit", {"density": 70, "feather": 12})
            self.capture(row, "feathered")
            self.engine("edit.undo")
            self.engine("edit.undo")
            assert not self.state()["document"]["layers"][0]["hasMask"], "Undo failed to remove mask"
            return "Selection became a layer mask; density/feather applied; undo restored mask absence."
        self.case("extended.mask", "Selection mask, feather and undo", "behavior", mask)

        def channel(row):
            self.fresh()
            bounds = self.state()["document"]["selectionBounds"]
            self.engine("select.saveSelection", {"name": "Audit selection"})
            self.engine("select.deselect")
            self.engine("select.loadSelection", {"channel": "Audit selection"})
            assert self.state()["document"]["selectionBounds"] == bounds, "Saved selection bounds changed"
            self.call("ui.set", {"dockTabs": {"layers": 1}})
            self.capture(row)
            return "Saved selection in an alpha channel and restored identical bounds."
        self.case("extended.channels", "Save and restore selection through an alpha channel", "behavior", channel)

        def layers(row):
            self.fresh()
            self.engine("layer.duplicate")
            assert len(self.state()["document"]["layers"]) == 2, "Duplicate missing"
            self.engine("layer.setProps", {"opacity": 0.55, "blend": "Multiply", "name": "Multiply 55%"})
            layer = self.state()["document"]["layers"][0]
            assert abs(layer["opacity"] - 0.55) < .001 and layer["blend"] == "Multiply"
            self.capture(row, "blend")
            self.engine("layer.groupLayers", {"name": "Audit group"})
            assert any(l["kind"] == "Group" for l in self.state()["document"]["layers"]), "Group missing"
            self.capture(row, "group")
            return "Duplicated layer, verified opacity/blend state and grouped the active layer."
        self.case("extended.layers", "Duplicate, blend, change opacity and group", "behavior", layers)

        def smart(row):
            self.fresh("smart")
            self.engine("select.deselect")
            self.engine("filter.blur.gaussianBlur", {"radius": 8})
            layer = self.state()["document"]["layers"][0]
            assert layer.get("smartFilters"), "Filter was not retained non-destructively"
            self.capture(row, "blurred")
            self.engine("layer.smartFilter.setParams", {"index": 0, "params": {"radius": 3}})
            self.capture(row, "edited")
            self.engine("layer.smartFilter.setVisible", {"index": 0, "visible": False})
            assert not self.state()["document"]["layers"][0]["smartFilters"][0]["visible"]
            self.capture(row, "disabled")
            return "Smart filter persisted, parameters edited and visibility disabled; source-preservation fidelity not independently compared."
        self.case("extended.smart-filter", "Editable Gaussian smart filter", "behavior", smart)

        for command, value in [("image.mode.bits16", 16), ("image.mode.bits32", 32)]:
            def depth(row, command=command, value=value):
                self.fresh()
                self.engine(command)
                assert self.state()["document"]["depth"] == value
                self.capture(row)
                return "Document depth verified. HDR numerical quality and external interchange require dedicated checks."
            self.case("extended." + command, "Convert document to " + str(value) + " bits/channel", "behavior", depth)

        for mode in ["grayscale", "cmyk", "lab", "indexedColor", "multichannel"]:
            def color_mode(row, mode=mode):
                self.fresh()
                self.engine("select.deselect")
                self.engine("image.mode." + mode)
                actual = self.state()["document"]["mode"]
                assert str(actual).lower() != "rgb", "Mode remained RGB"
                self.capture(row)
                return "Mode converted to " + str(actual) + ". Calibrated print/color accuracy not certified."
            self.case("extended.mode." + mode, "Convert color mode to " + mode, "behavior", color_mode)

        def actions(row):
            self.fresh()
            self.engine("actions.record", {"name": "Audit rotate"})
            self.engine("image.imageRotation.90cw")
            stopped = self.engine("actions.stop")
            assert stopped["steps"] >= 1, "No action steps recorded"
            self.capture(row, "recorded")
            self.fresh()
            result = self.engine("actions.play", {"action": "Audit rotate"})
            assert not result.get("failed") and result["ran"] >= 1
            doc = self.state()["document"]
            assert (doc["width"], doc["height"]) == (384, 512)
            self.capture(row, "played")
            return "Recorded canvas rotation, replayed on a fresh document and verified swapped dimensions."
        self.case("extended.actions", "Record and replay an action", "behavior", actions)

        # Cover the additional source menus that only affect our disposable
        # document or isolated preferences. OS clipboard/file/help flows stay listed.
        for item in self.menus:
            identifier = item["id"]
            included = (identifier.startswith("image.") and not identifier.startswith("image.adjustments.")) or identifier.startswith(("edit.transform.", "edit.freeTransform", "edit.fill", "edit.stroke", "edit.preferences.", "window.workspace.", "window.arrange."))
            included = included or (identifier.startswith("layer.") and any(part in identifier.lower() for part in ["delete", "clear", "reveal"]) and "finder" not in identifier.lower())
            if not included:
                continue
            def menu(row, item=item):
                self.fresh()
                self.call("ui.menu.invoke", {"id": item["id"], "wait": True})
                self.capture(row, "opened")
                self.cleanup_ui()
                return "Additional menu invoked and visible state captured; specialized forms cancelled. Semantic outcome not certified."
            self.case(identifier, " > ".join(item["menu"] + [item["label"]]), "menu_smoke", menu)

    def residual_cases(self):
        def slices(row):
            self.fresh()
            self.engine("select.deselect")
            self.pointer("Slice", [(85, 85), (180, 150), (250, 220)])
            before = self.engine("slice.list")
            self.capture(row, "created")
            self.pointer("SliceSelect", [(120, 120), (150, 140), (180, 160)])
            assert self.engine("slice.list") != before, "Slice Select did not move the prepared slice"
            self.capture(row, "moved")
            return "Created a slice using the canvas tool and changed its bounds using Slice Select."
        self.case("residual.SliceSelect", "Create and move a slice", "behavior", slices)

        def remove(row):
            self.fresh()
            self.engine("select.deselect")
            self.engine("paint.pencil", {"points": [[0, 180], [512, 180]], "size": 700, "color": "#808080"})
            self.engine("paint.pencil", {"points": [[260, 150], [260, 220]], "size": 4, "color": "#000000"})
            self.call("ui.set", {"brushSize": 18})
            before = self.engine("document.pixel", {"x": 260, "y": 180})
            self.capture(row, "before")
            self.pointer("Remove", [(260, 140), (260, 165), (260, 195), (260, 235)])
            deadline = time.monotonic() + 60
            while self.state()["jobs"].get("running") and time.monotonic() < deadline:
                time.sleep(.2)
            assert not self.state()["jobs"].get("running"), "Remove background job did not finish in 60 seconds"
            after = self.engine("document.pixel", {"x": 260, "y": 180})
            assert after != before, "Remove did not change the black mark's sampled pixel"
            self.capture(row, "removed")
            return "Waited for the Remove background job and verified changed pixels on a controlled mark. Natural-photo quality not certified."
        self.case("residual.Remove", "Remove a mark and wait for its background job", "behavior", remove)

    def remaining_cases(self, path):
        remaining = json.loads(path.read_text(encoding="utf-8"))
        for item in remaining:
            identifier = item["id"]
            # Preserve the user's OS clipboard. These need a separate manual session.
            if identifier in ["edit.cut", "edit.copy", "edit.copyMerged", "edit.paste", "edit.purge.clipboard", "edit.purge.all"] or identifier.startswith("edit.pasteSpecial."):
                continue
            def menu(row, item=item):
                self.fresh("text" if item["id"] in ["edit.checkSpelling", "edit.findAndReplaceText"] else "raster")
                self.call("ui.menu.invoke", {"id": item["id"], "wait": True})
                self.capture(row, "opened")
                self.cleanup_ui()
                return "Remaining menu invoked; visible state captured and dialogs cancelled. Filesystem/OS operations may be refused by the application's automation policy."
            self.case(identifier, " > ".join(item["menu"] + [item["label"]]), "menu_smoke", menu)

    def prepared_menu_cases(self, path):
        prior = {row["id"]: row for row in json.loads(path.read_text(encoding="utf-8"))}
        catalog = {item["id"]: item for item in self.menus}
        for identifier, old in prior.items():
            prerequisite = identifier in ["edit.redo", "edit.fade", "edit.autoAlignLayers", "edit.autoBlendLayers", "edit.defineCustomShape", "layer.smartFilter.deleteFilterMask", "layer.smartFilter.clearSmartFilters", "layer.videoLayers.deleteFrame", "view.clearSelectedArtboardGuides", "view.clearSlices"]
            if (old["status"] != "failed" and not (old["status"] == "restricted_or_unsupported" and prerequisite)) or identifier not in catalog:
                continue
            def prepared(row, identifier=identifier):
                context = "text" if identifier.startswith("type.") or identifier in ["layer.rasterize.type", "layer.rasterize.layer"] else "shape" if identifier in ["layer.rasterize.shape", "view.newGuidesFromShape", "edit.defineCustomShape"] else "smart" if identifier == "layer.rasterize.smartObject" or "Warp" in identifier or identifier.startswith("layer.smartFilter.") else "group" if identifier == "layer.ungroupLayers" else "raster"
                self.fresh(context)
                params = {}
                if identifier in ["edit.redo", "edit.fade"]:
                    self.engine("filter.blur.gaussianBlur", {"radius": 4})
                    if identifier == "edit.redo":
                        self.engine("edit.undo")
                elif identifier.startswith("layer.smartFilter."):
                    self.engine("filter.blur.gaussianBlur", {"radius": 4})
                elif identifier == "view.clearSlices":
                    self.engine("slice.new", {"rect": [70, 70, 200, 150]})
                elif identifier == "view.clearSelectedArtboardGuides":
                    self.engine("layer.new.artboard", {"rect": [60, 60, 320, 240]})
                elif identifier == "edit.defineCustomShape":
                    self.engine("path.set", {"path": {"subpaths": [{"closed": True, "knots": [[80, 80], [260, 80], [260, 200], [80, 200]]}]}})
                    params = {"name": "Audit shape"}
                elif "Warp" in identifier:
                    self.engine("edit.transform.warp", {"style": "arc", "bend": 25})
                    if identifier == "edit.transform.removeWarpSplit":
                        self.engine("edit.transform.splitWarpCrosswise")
                elif identifier == "edit.transform.again":
                    self.engine("edit.transform.rotate90Cw")
                elif "video" in identifier.lower():
                    self.engine("layer.videoLayers.newBlankVideoLayer")
                    if identifier == "layer.videoLayers.deleteFrame":
                        self.engine("layer.videoLayers.insertBlankFrame")
                elif identifier.startswith(("layer.arrange.", "layer.distribute.", "layer.linkLayers", "layer.selectLinkedLayers", "layer.merge")) or identifier in ["layer.delete", "edit.autoAlignLayers", "edit.autoBlendLayers"]:
                    self.engine("layer.duplicate")
                    self.engine("layer.duplicate")
                    layers = self.state()["document"]["layers"]
                    for index, layer in enumerate(layers):
                        self.engine("layer.select", {"layer": layer["id"], "mode": "replace" if index == 0 else "add"})
                    if identifier == "layer.selectLinkedLayers":
                        self.engine("layer.linkLayers")
                        self.engine("layer.select", {"layer": layers[0]["id"]})
                    elif identifier == "layer.delete":
                        self.engine("layer.select", {"layer": layers[0]["id"]})
                    elif identifier in ["layer.arrange.bringToFront", "layer.arrange.bringForward"]:
                        self.engine("layer.select", {"layer": layers[-1]["id"]})
                    elif identifier in ["layer.arrange.sendToBack", "layer.arrange.sendBackward"]:
                        self.engine("layer.select", {"layer": layers[0]["id"]})
                elif identifier.startswith("layer.combineShapes."):
                    self.engine("shape.create", {"kind": "rect", "rect": [80, 80, 260, 200], "fill": "#ffaa44"})
                    first = self.state()["document"]["activeLayer"]
                    self.engine("shape.create", {"kind": "rect", "rect": [180, 130, 350, 260], "fill": "#44aaff"})
                    self.engine("layer.select", {"layer": first, "mode": "add"})
                elif identifier in ["layer.layerContentOptions", "layer.rasterize.fillContent"]:
                    self.engine("layer.newFillLayer.solidColor", {"color": "#ee7722"})
                elif identifier in ["layer.vectorMask.delete", "layer.rasterize.vectorMask"]:
                    self.engine("path.set", {"path": {"subpaths": [{"closed": True, "knots": [[80, 80], [260, 80], [260, 200], [80, 200]]}]}})
                    self.engine("layer.vectorMask.currentPath")
                elif identifier in ["layer.rasterize.layerStyle", "layer.rasterize.layer"]:
                    self.engine("layer.layerStyle.dropShadow", {"size": 12, "distance": 15})
                elif identifier == "type.convertToPointText":
                    self.engine("type.convertToParagraphText")
                elif identifier == "type.loadDefaultTypeStyles":
                    self.engine("type.saveDefaultTypeStyles")
                elif identifier == "select.reselect":
                    self.engine("select.deselect")
                elif identifier == "select.findLayers":
                    params = {"name": "Layer 0"}
                elif identifier == "select.loadSelection":
                    self.engine("select.saveSelection", {"name": "Audit selection"})
                    self.engine("select.deselect")
                    params = {"channel": "Audit selection"}
                elif identifier == "filter.lastFilter":
                    self.engine("filter.blur.gaussianBlur", {"radius": 3})
                elif identifier == "filter.distort.displace":
                    params = {"mapDocument": 0, "horizontal": 18, "vertical": 12}
                elif identifier == "filter.vanishingPoint":
                    params = {"planes": [{"corners": [[70, 70], [440, 80], [420, 320], [90, 300]]}], "clone": [{"source": [145, 130], "points": [[300, 230], [315, 240]], "size": 35}], "newLayer": True}
                elif identifier == "view.fitArtboardOnScreen":
                    self.engine("layer.new.artboard", {"rect": [60, 60, 320, 240]})
                self.call("ui.menu.invoke", {"id": identifier, "params": params, "wait": True})
                self.capture(row, "opened")
                for dialog in self.state().get("dialogs", []):
                    if str(dialog.get("kind", "")).lower() in ["command", "filter", "adjustment"]:
                        self.call("ui.dialog.confirm", {"dialog": dialog["id"]})
                        self.capture(row, "applied")
                self.cleanup_ui()
                return "Retested with prerequisite layers/selection/video/path/filter state or explicit input. Menu dispatch smoke check; semantic correctness not fully asserted."
            self.case(identifier, "Prepared fixture: " + catalog[identifier]["label"], "menu_smoke", prepared)

    def evaluation_cases(self):
        # User-supplied evaluation is test input; these are bounded reproductions,
        # not assertions that old issue reports apply to this machine.
        width, height = 512, 384
        pixels = bytes(v for y in range(height) for x in range(width)
                       for v in (220, 80, 40, (0, 128, 255)[min(2, x * 3 // width)]))
        def chunk(kind, data):
            return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
        png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        png += chunk(b"IDAT", zlib.compress(b"".join(b"\0" + pixels[y*width*4:(y+1)*width*4] for y in range(height)))) + chunk(b"IEND", b"")
        (self.out / "samples/alpha.png").write_bytes(png)
        bgra = bytearray(pixels)
        bgra[0::4], bgra[2::4] = pixels[2::4], pixels[0::4]
        (self.out / "samples/alpha.tga").write_bytes(struct.pack("<BBBHHBHHHHBB", 0, 0, 2, 0, 0, 0, 0, 0, width, height, 32, 0x28) + bgra)
        for extension in ["png", "tga"]:
            def alpha(row, extension=extension):
                self.fresh()
                self.engine("file.closeAll")
                self.call("app.open", {"path": "samples/alpha." + extension})
                observed = [self.engine("document.pixel", {"x": x, "y": 150}) for x in [80, 250, 440]]
                write_json(self.out / "state" / (extension + "-alpha-values.json"), observed)
                self.capture(row)
                expected_alpha = [0, 128/255, 1] if extension == "png" else [1, 1, 1]
                for rgba, expected in zip(observed, expected_alpha):
                    assert abs(rgba[3] - expected) < 1/255, f"{extension} alpha: expected {expected}, got {rgba}"
                if extension == "tga":
                    channels = self.state()["document"]["channels"]["alpha"]
                    assert len(channels) == 1 and channels[0]["name"] == "Alpha 1", "TGA alpha channel was not preserved"
                    self.call("app.save", {"path": "samples/alpha-roundtrip.tga"})
                self.call("app.save", {"path": "samples/alpha-import-" + extension + ".pcraft"})
                return ("PNG transparent, half-transparent and opaque composite alpha preserved." if extension == "png" else
                        "TGA imported as opaque Background plus Alpha 1, as designed; TGA export saved for independent alpha-value verification. Initial composite-transparency expectation was incorrect.")
            self.case("evaluation.alpha." + extension, "Evaluation: transparent " + extension.upper() + " import", "behavior", alpha)

        def multilayer(row):
            self.fresh()
            self.engine("select.deselect")
            for i in range(149):
                self.engine("layer.duplicate", {"name": "Audit layer " + str(i + 2)})
            before = self.state()["document"]
            assert len(before["layers"]) == 150
            selected = before["activeLayer"]
            initial = next(l for l in before["layers"] if l["id"] == selected)
            self.capture(row, "before-nudge")
            self.call("ui.key", {"key": "ArrowRight"})
            time.sleep(.8)
            after = self.state()["document"]
            moved = next(l for l in after["layers"] if l["id"] == selected)
            self.capture(row, "after-nudge")
            assert moved["bounds"] != initial["bounds"], "Arrow nudge did not change active layer bounds"
            for i in range(10):
                self.engine("layer.setProps", {"visible": bool(i % 2)})
                self.state()
            self.capture(row, "visibility-toggled")
            self.call("app.save", {"path": "samples/150-layers.pcraft"})
            return "150 populated layers at 512x384: ArrowRight moved the selected layer, 10 visibility toggles completed, GPU screenshots and native save succeeded. Not the original large-document fixture or a release speed benchmark."
        self.case("evaluation.150-layer-nudge", "Evaluation: nudge and visibility in 150-layer document", "behavior", multilayer)

        def histogram_refresh(row):
            self.call("ui.set", {"panels": {"navigator": True}, "dockTabs": {"navigator": 1}})
            assert self.state()["dockTabs"]["navigator"] == 1, "Histogram tab was not activated"
            result = multilayer(row)
            return result + " Histogram panel enabled during edits; worker bounds are established by the Rust regression test, not this recording."
        self.case("evaluation.histogram-refresh", "Histogram visible during 150-layer editing", "behavior", histogram_refresh)

    def layout_cases(self):
        def shape_layout(row):
            self.cleanup_ui()
            self.engine("file.closeAll")
            self.engine("file.new", {"width": 4000, "height": 3000})
            self.engine("edit.fill", {"color": "#f4efe5"})
            self.call("ui.set", {"fit": True, "tool": "move"})
            palette = ["#d6a85b", "#496d60", "#608d98", "#b36b54", "#444b68", "#bd91a6", "#a8b29a", "#d4ba94"]
            for i in range(33):
                if i == 0:
                    rect, color = [180, 570, 3600, 130], "#292d35"
                else:
                    j = i - 1
                    rect, color = [180 + j % 8 * 440, 950 + j // 8 * 400, 350, 280], palette[(j + j // 8) % len(palette)]
                self.engine("shape.create", {"kind": "roundedRect", "rect": rect, "radii": 24,
                            "fill": color, "stroke": {"width": 6, "color": "#faf7f0"}, "name": f"Colour study {i + 1:02d}"})
                self.engine("layer.layerStyle.dropShadow", {"size": 12, "distance": 15})
            target = self.state()["document"]["activeLayer"]
            for x, y, text, size in [(180, 300, "FORM / FLOW", 170),
                                     (190, 450, "33 EDITABLE SHAPES / STROKE + SHADOW", 46),
                                     (180, 2810, "BUILD / EDIT / SAVE", 70)]:
                self.engine("type.create", {"x": x, "y": y, "text": text, "size": size, "color": "#292d35"})
            self.engine("layer.select", {"layer": target})
            before = self.state()["document"]
            assert len(before["layers"]) == 37, "Expected background, 33 shapes and three text layers"
            old_bounds = next(l["bounds"] for l in before["layers"] if l["id"] == target)
            sample = {"x": 3435, "y": 2290}
            pixel = self.engine("document.pixel", sample)
            self.capture(row, "layout-ready")
            for opacity in [.25, .5, .75, 1.0]:
                self.engine("layer.setProps", {"layer": target, "opacity": opacity})
                if opacity == .25:
                    assert self.engine("document.pixel", sample) != pixel, "Opacity did not change the sampled composite"
                    self.capture(row, "opacity-quarter")
            assert self.engine("document.pixel", sample) == pixel, "Restoring opacity changed the original composite"
            self.engine("layer.translate", {"layer": target, "dx": 24, "dy": -12})
            moved = next(l["bounds"] for l in self.state()["document"]["layers"] if l["id"] == target)
            assert moved != old_bounds, "Moving the shape did not change its bounds"
            self.capture(row, "shape-moved")
            self.engine("edit.undo")
            assert next(l["bounds"] for l in self.state()["document"]["layers"] if l["id"] == target) == old_bounds
            self.engine("edit.redo")
            assert next(l["bounds"] for l in self.state()["document"]["layers"] if l["id"] == target) == moved
            self.call("app.save", {"path": "samples/shape-cache-layout.pcraft"})
            self.call("app.save", {"path": "samples/shape-cache-layout.png"})
            self.engine("file.closeAll")
            self.call("app.open", {"path": "samples/shape-cache-layout.pcraft"})
            assert len(self.state()["document"]["layers"]) == 37, "Native reopen lost editable layers"
            self.capture(row, "native-reopened")
            purge_note = ""
            if getattr(self.args, "check_shape_purge", False):
                purge = self.engine("edit.purge.all")
                assert "shape split cache" in purge["purged"], "Purge All did not report the shape cache"
                assert purge["bytes"] > 0, "Purge All reported no accounted retention"
                assert self.engine("document.pixel", sample) == pixel, "Purging caches changed the composite"
                self.capture(row, "after-cache-purge")
                purge_note = " Purge All reported shape-cache retention and preserved the sampled composite."
            return "12 MP, 33 stroked shapes with shadows and three text layers: sampled opacity change/restore, move bounds, undo/redo, native save/reopen and PNG export passed. Live workflow evidence; release benchmark establishes frame timings separately." + purge_note
        self.case("layout.shape-cache", "12 MP editable colour study: 33 stroked shapes", "behavior", shape_layout)

    def rendering_cases(self):
        width, height = 1791, 1083
        rows = bytearray()
        for y in range(height):
            rows.append(0)
            for x in range(width):
                rows.extend(struct.pack(">HHH", 10000 + x * 40000 // width,
                                        12000 + y * 35000 // height,
                                        16000 + 12000 * ((x // 96 + y // 96) % 2)))
        def chunk(kind, data):
            return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
        path = "samples/high-depth.png"
        (self.out / path).write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 16, 2, 0, 0, 0))
                                    + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))
        def preview(row):
            self.fresh()
            self.engine("file.closeAll")
            self.call("app.open", {"path": path})
            self.engine("layer.new.layerFromBackground")
            assert self.state()["document"]["depth"] == 16, "Fixture did not open at 16-bit depth"
            before = self.engine("document.pixel", {"x": 1100, "y": 650})
            self.call("ui.set", {"zoom": .125, "tool": "brush", "brushSize": 500})
            self.capture(row, "before-edit")
            self.pointer("Brush", [(900, 550, 1), (1100, 650, 1), (1400, 900, 1)])
            painted = self.engine("document.pixel", {"x": 1100, "y": 650})
            assert before != painted, "Partial brush edit did not change the sampled pixel"
            # End painting before the separate reduced-preview/navigation demonstration.
            # Keep history assertions strict: navigation must not introduce another edit.
            self.call("ui.set", {"tool": "move"})
            stroke_history = self.state()["document"]["history"]
            assert stroke_history.count("Brush Tool") == 1, "One control gesture must create one brush history entry"
            for zoom in [.25, .125, .03125]:
                self.call("ui.set", {"zoom": zoom})
                self.capture(row, "edited-zoom-" + str(zoom))
                assert self.state()["document"]["history"] == stroke_history, "Preview navigation introduced a document edit"
            self.engine("edit.undo")
            assert self.engine("document.pixel", {"x": 1100, "y": 650}) == before, "Undo failed to restore the source pixel"
            self.capture(row, "undo")
            self.engine("edit.redo")
            assert self.engine("document.pixel", {"x": 1100, "y": 650}) == painted, "Redo failed to restore the edit"
            self.capture(row, "redo")
            self.call("app.save", {"path": "samples/high-depth-edited.pcraft"})
            return "Recorded actual 16-bit canvas after a partial brush edit at three reduced zooms; exact composite-pixel undo/redo and native save passed. GPU mip readback tests establish rendering correctness separately; this UI case is visual smoke evidence."
        self.case("rendering.high-depth", "High-depth partial edit and reduced canvas previews", "rendering_smoke", preview)

    def report(self):
        write_json(self.out / "results.json", self.rows)
        tested = {r["id"] for r in self.rows}
        coverage = [dict(item, status="not_exercised", level="inventory", note="Requires a dedicated fixture, manual interaction or authorization-safe test")
                    for item in self.menus if item["id"] not in tested]
        write_json(self.out / "uncovered-menus.json", coverage)
        counts = dict(collections.Counter(row["status"] for row in self.rows))
        with (self.out / "command-coverage.csv").open("w", newline="", encoding="utf-8-sig") as output:
            writer = csv.DictWriter(output, fieldnames=["id", "label", "calls", "status", "params"])
            writer.writeheader()
            for command in self.engine_catalog:
                writer.writerow({"id": command["id"], "label": command["label"], "calls": self.command_calls[command["id"]],
                                 "status": "invoked_not_semantically_certified" if self.command_calls[command["id"]] else "not_invoked",
                                 "params": command.get("params", "")})
        write_json(self.out / "summary.json", {"cases": len(self.rows), "statuses": counts,
            "run_status": self.run_status, "run_error": self.run_error,
            "levels": dict(collections.Counter(row["level"] for row in self.rows)),
            "catalog_menus": len(self.menus), "tools": len(self.tools), "uncovered_menus": len(coverage),
            "engine_commands": len(self.engine_catalog), "distinct_command_ids_called": len(self.command_calls),
            "uncovered_tools": [tool for tool in self.tools if "tool." + tool not in tested],
            "elapsed_seconds": round(time.time() - self.started, 2),
            "recording": "live-walkthrough.mp4" if (self.out / "live-walkthrough.mp4").exists() else None,
            "scope": "Windows live UI; synthetic fixtures (dimensions recorded in case notes); automation methods and synthetic gestures. Not complete Photoshop parity, performance, tablet, accessibility or independent-export validation."})
        with (self.out / "coverage.csv").open("w", newline="", encoding="utf-8-sig") as output:
            writer = csv.DictWriter(output, fieldnames=["id", "title", "level", "status", "note"])
            writer.writeheader()
            for row in self.rows:
                writer.writerow({key: row.get(key, "") for key in writer.fieldnames})
            for row in coverage:
                writer.writerow({"id": row["id"], "title": row["label"], "level": row["level"], "status": row["status"], "note": row["note"]})
        cards = []
        for row in self.rows:
            screenshots = "".join(f'<a href="{html.escape(path)}"><img loading="lazy" src="{html.escape(path)}" alt="{html.escape(row["title"])}"></a>' for path in row["evidence"])
            cards.append(f'<article><h2>{html.escape(row["title"])}</h2><p><b>{row["status"]}</b> · {row["level"]} · recording {row["seconds"]:.0f}s</p><p>{html.escape(row["note"])}</p>{screenshots}</article>')
        video = '<video controls src="live-walkthrough.mp4"></video>' if (self.out / "live-walkthrough.mp4").exists() else '<p>No live recording has been produced.</p>'
        document = '<!doctype html><meta charset="utf-8"><title>PhotoCraft live feature audit</title><style>body{font:16px system-ui;margin:32px auto;max-width:1100px;padding:0 20px;background:#f5f5f5;color:#222}article{background:white;padding:20px;margin:20px 0;border:1px solid #ddd}img{max-width:100%;height:auto}video{width:100%}h2{font-size:20px}</style><h1>PhotoCraft live feature audit</h1><p>Run status: <b>' + html.escape(self.run_status) + '</b></p><p>Designed to capture the actual app window using synthetic artwork and isolated preferences. Activation and smoke checks do not prove full feature correctness. See coverage.csv for untested features.</p><p>' + html.escape(json.dumps(counts)) + '</p>' + video + '<p><a href="coverage.csv">Coverage ledger</a> · <a href="summary.json">Summary</a> · <a href="results.json">Detailed results</a></p>' + "".join(cards)
        (self.out / "index.html").write_text(document, encoding="utf-8")
        chapters = []
        for row in self.rows:
            seconds = int(row["seconds"])
            chapters.append(f"{seconds//3600:02d}:{seconds//60%60:02d}:{seconds%60:02d} {row['id']} — {row['status']}")
        (self.out / "chapters.txt").write_text("\n".join(chapters), encoding="utf-8")
        def stamp(seconds):
            milliseconds = int(seconds * 1000)
            return f"{milliseconds//3600000:02d}:{milliseconds//60000%60:02d}:{milliseconds//1000%60:02d},{milliseconds%1000:03d}"
        captions = []
        for index, row in enumerate(self.rows):
            end = self.rows[index+1]["seconds"] if index+1 < len(self.rows) else time.time() - (self.recording_started or self.started)
            captions.append(f"{index+1}\n{stamp(row['seconds'])} --> {stamp(max(end, row['seconds']+0.1))}\n{row['title']}\n{row['level']} | {row['status']}\n")
        (self.out / "walkthrough.srt").write_text("\n".join(captions), encoding="utf-8")

    def finish(self):
        if self.recorder:
            self.record_stop.set()
            if getattr(self, "record_thread", None):
                self.record_thread.join(timeout=10)
            if self.recorder.poll() is None:
                try:
                    self.recorder.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    self.recorder.terminate()
                    self.recorder.wait(timeout=10)
            write_json(self.out / "recording-metadata.json", {"method": "live GPU UI screenshot stream", "fps": self.record_fps,
                "frames": self.record_frames, "error": self.record_error, "encoder_exit": self.recorder.returncode})
        if self.rpc:
            try:
                self.call("app.quit")
            except (OSError, RuntimeError):
                pass
            self.rpc.close()
        if self.process and self.process.poll() is None:
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.terminate()
        if self.run_status == "completed":
            failures = sum(row["status"] == "failed" for row in self.rows)
            reasons = [f"{failures} live case(s) failed"] if failures else []
            if self.recorder:
                if self.record_error:
                    reasons.append(f"Recording failed: {self.record_error}")
                if self.recorder.returncode != 0:
                    reasons.append(f"Recording encoder exited with {self.recorder.returncode}")
            if reasons:
                self.run_status = "failed"
                self.run_error = "; ".join(reasons)
        self.report()
        for stream in [self.log, self.app_log, self.record_log]:
            stream.close()


def hold_app_visible(process_id):
    """Keep only the audit app above occluding windows for this recording, without focus changes."""
    import ctypes
    from ctypes import wintypes
    api = ctypes.WinDLL("user32", use_last_error=True)
    callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    api.EnumWindows.argtypes = [callback_type, wintypes.LPARAM]
    api.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    api.IsWindowVisible.argtypes = [wintypes.HWND]
    api.IsWindow.argtypes = [wintypes.HWND]
    api.IsIconic.argtypes = [wintypes.HWND]
    api.GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
    api.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
    api.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.UINT]
    get_style = api.GetWindowLongPtrW if ctypes.sizeof(ctypes.c_void_p) == 8 else api.GetWindowLongW
    get_style.argtypes = [wintypes.HWND, ctypes.c_int]
    get_style.restype = ctypes.c_ssize_t
    candidates = []
    def visit(window, _):
        owner = wintypes.DWORD()
        api.GetWindowThreadProcessId(window, ctypes.byref(owner))
        if owner.value == process_id and api.IsWindowVisible(window):
            rect = wintypes.RECT()
            if api.GetClientRect(window, ctypes.byref(rect)):
                candidates.append(((rect.right - rect.left) * (rect.bottom - rect.top), window))
        return True
    if not api.EnumWindows(callback_type(visit), 0) or not candidates:
        raise RuntimeError("No visible audit-app window found for capture")
    _, window = max(candidates)
    was_topmost = bool(get_style(window, -20) & 8)
    if api.IsIconic(window):
        api.ShowWindow(window, 9)
    if not api.SetWindowPos(window, -1, 0, 0, 0, 0, 0x13):
        raise RuntimeError("Could not keep the audit-app window visible")
    return {"api": api, "window": window, "process_id": process_id, "was_topmost": was_topmost}


def release_app_visible(lease):
    """Restore only the same process's window; a destroyed/reused handle needs no restoration."""
    import ctypes
    from ctypes import wintypes
    api, window = lease["api"], lease["window"]
    if not api.IsWindow(window):
        return {"restored": True, "window_closed": True}
    owner = wintypes.DWORD()
    api.GetWindowThreadProcessId(window, ctypes.byref(owner))
    if owner.value != lease["process_id"]:
        return {"restored": True, "window_closed": True, "handle_reused": True}
    restored = bool(api.SetWindowPos(window, -1 if lease["was_topmost"] else -2, 0, 0, 0, 0, 0x13))
    return {"restored": restored, "window_closed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", type=Path, default=ROOT / "target/debug/photocraft.exe")
    parser.add_argument("--ffmpeg", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/qa/live-feature-audit")
    parser.add_argument("--port", type=int, default=17878)
    parser.add_argument("--dwell", type=float, default=0.35)
    parser.add_argument("--menu-sweep", action="store_true")
    parser.add_argument("--inventory-only", action="store_true")
    parser.add_argument("--phase", choices=["probe", "tools", "gestures", "workflows", "menus", "extended", "residual", "remaining", "prepared", "evaluation", "rendering", "layout", "all"], default="all")
    parser.add_argument("--case-filter", default="")
    parser.add_argument("--retry-results", type=Path)
    parser.add_argument("--remaining-menus", type=Path)
    parser.add_argument("--animate-input", action="store_true", help="Deliver stroke points over successive UI frames")
    parser.add_argument("--keep-awake", action="store_true", help="Temporarily prevent Windows display sleep during capture")
    parser.add_argument("--check-shape-purge", action="store_true", help="Check rebuilt shape-cache Purge All behavior in the layout phase")
    parser.add_argument("--keep-visible", action="store_true", help="Temporarily keep only the audit app above occluding windows during capture")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    audit = Audit(args)
    awake_prior = None
    if args.keep_awake and os.name == "nt":
        import ctypes
        execution_state = ctypes.windll.kernel32.SetThreadExecutionState
        execution_state.argtypes = [ctypes.c_uint32]
        execution_state.restype = ctypes.c_uint32
        awake_prior = execution_state(0x80000003)  # Continuous + display/system required.
        write_json(audit.out / "display-awake.json", {"requested": True, "set_succeeded": bool(awake_prior), "temporary": True})
    try:
        if args.inventory_only:
            audit.report()
            print(json.dumps({"menus": len(audit.menus), "tools": len(audit.tools), "output": str(audit.out)}))
            return 0
        audit.run_status = "running"
        audit.launch()
        audit.fresh()
        if args.phase == "probe":
            audit.case("startup.capture", "Startup and recording validation", "startup", lambda row: audit.capture(row))
            time.sleep(3)
        if args.phase in ["all", "tools"]:
            audit.tool_cases()
        if args.phase in ["all", "gestures"]:
            audit.gesture_cases()
        if args.phase in ["all", "workflows"]:
            audit.functional_cases()
        if args.phase == "extended":
            audit.extended_cases()
            if args.retry_results:
                audit.retry_cases(args.retry_results)
        if args.phase == "residual":
            audit.residual_cases()
        if args.phase == "evaluation":
            audit.evaluation_cases()
        if args.phase == "rendering":
            audit.rendering_cases()
        if args.phase == "layout":
            audit.layout_cases()
        if args.phase == "remaining":
            if not args.remaining_menus:
                raise ValueError("--remaining-menus is required for the remaining phase")
            audit.remaining_cases(args.remaining_menus)
        if args.phase == "prepared":
            if not args.retry_results:
                raise ValueError("--retry-results is required for the prepared phase")
            audit.prepared_menu_cases(args.retry_results)
        if args.phase == "menus" or (args.menu_sweep and args.phase == "all"):
            audit.menu_cases()
        if args.phase == "all":
            audit.fallback_case()
        audit.run_status = "completed"
    except Exception as error:
        audit.run_status = "interrupted"
        audit.run_error = str(error)
        raise
    finally:
        try:
            audit.finish()
        finally:
            if getattr(audit, "visibility_lease", None):
                restored = release_app_visible(audit.visibility_lease)
                write_json(audit.out / "window-visibility.json", {"temporary": True, "set_succeeded": True,
                           "was_topmost": audit.visibility_lease["was_topmost"], **restored})
            if awake_prior:
                restored = execution_state(awake_prior)
                write_json(audit.out / "display-awake.json", {"requested": True, "set_succeeded": True, "temporary": True, "restore_succeeded": bool(restored)})
    return 1 if audit.run_status in {"failed", "interrupted"} else 0


if __name__ == "__main__":
    raise SystemExit(main())
