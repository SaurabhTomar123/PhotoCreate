"""Run repository validation and retain logs/status, continuing after test failures."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/qa/validation")
    parser.add_argument("--corpus", action="store_true")
    parser.add_argument("--only", choices=["workspace", "doc-tests", "panic-hunt", "layers", "scorecard", "fetch-corpus", "corpus", "gpu-mips", "gpu-target", "ui-tests", "ui-gpu", "clippy-ui", "wasm", "build-app", "perf-quick"])
    parser.add_argument("--gpu-binary", type=Path)
    parser.add_argument("--backend", choices=["vulkan", "dx12"], help="Explicit GPU backend for a retained regression run")
    parser.add_argument("--jobs", type=int, choices=range(1, 5), default=4)
    parser.add_argument("--skip-build", action="store_true", help="Reuse the already-built release layout benchmark")
    args = parser.parse_args()
    if args.skip_build and args.only != "perf-quick":
        parser.error("--skip-build is only valid for --only perf-quick")
    args.output.mkdir(parents=True, exist_ok=True)
    cargo = Path(os.environ["USERPROFILE"]) / ".cargo/bin/cargo.exe"
    env = os.environ.copy()
    env["PATH"] = str(cargo.parent) + os.pathsep + env.get("PATH", "")
    env["RUST_BACKTRACE"] = "1"
    if args.backend:
        env["WGPU_BACKEND"] = args.backend
    steps = [
        ("workspace", ["test", "--workspace", "--lib", "--tests", "--locked", "--features", "heif", "-j", "4", "--no-fail-fast"]),
        ("doc-tests", ["test", "--workspace", "--doc", "--locked", "--features", "heif", "-j", "4", "--no-fail-fast"]),
        ("panic-hunt", ["test", "-p", "photocraft-engine", "--test", "panic_hunt", "--locked", "--", "--ignored"]),
        ("layers", ["xtask", "layers"]),
        ("scorecard", ["xtask", "scorecard", "--check"]),
    ]
    if args.corpus:
        steps.extend([
            ("fetch-corpus", ["xtask", "corpus", "--all"]),
            ("corpus", ["test", "-p", "photocraft-psd", "-p", "photocraft-codecs", "-p", "photocraft-io", "-p", "photocraft-engine", "--lib", "--tests", "--features", "corpus,heif", "--locked", "-j", "4", "--no-fail-fast"]),
        ])
    results = []
    if args.only in ["ui-tests", "ui-gpu", "clippy-ui", "wasm", "build-app", "perf-quick"]:
        extra = {
            "ui-tests": ["test", "-p", "photocraft-ui-egui", "--lib", "--tests", "--locked", "-j", "4", "--", "--test-threads=1"],
            "ui-gpu": ["test", "-p", "photocraft-ui-egui", "--lib", "--locked", "-j", "4", "gpu_canvas::", "--", "--nocapture", "--test-threads=1"],
            "clippy-ui": ["clippy", "-p", "photocraft-ui-egui", "--all-targets", "--locked", "-j", "4", "--", "-D", "warnings"],
            "wasm": ["xtask", "wasm"],
            "build-app": ["build", "-p", "photocraft", "--locked", "--features", "heif", "-j", "4"],
            "perf-quick": ["xtask", "perf", "--quick", "--bench", "layout_bench"],
        }
        steps.append((args.only, extra[args.only]))
    if args.only:
        steps = [step for step in steps if step[0] == args.only]
    if args.only in ["gpu-mips", "gpu-target"]:
        if not args.gpu_binary or not args.gpu_binary.is_file():
            parser.error("--gpu-binary must name the compiled UI test executable")
        command = ["--nocapture", "--test-threads=1"]
        if args.only == "gpu-mips":
            command = ["gpu_canvas::mip_tests::canvas_mips_preserve_opaque_pixels_and_partial_updates", "--exact"] + command
        steps = [(args.only, command)]
    for name, command in steps:
        if "-j" in command:
            command[command.index("-j") + 1] = str(args.jobs)
        if name == "perf-quick" and args.skip_build:
            command.append("--skip-build")
        print("Starting " + name, flush=True)
        started = time.time()
        with (args.output / (name + ".log")).open("w", encoding="utf-8") as log:
            executable = args.gpu_binary.resolve() if name in ["gpu-mips", "gpu-target"] else cargo
            process = subprocess.Popen([str(executable)] + command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
            status = process.wait()
        row = {"name": name, "command": [str(executable)] + command, "exit_code": status,
               "elapsed_seconds": round(time.time() - started, 2), "log": name + ".log"}
        if args.backend:
            row["requested_backend"] = args.backend
        results.append(row)
        (args.output / "validation-results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"Finished {name}: exit={status}, seconds={row['elapsed_seconds']}", flush=True)
    return 1 if any(row["exit_code"] for row in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
