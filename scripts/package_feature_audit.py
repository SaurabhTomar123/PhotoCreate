"""Make a local, searchable viewing package from completed live audit sessions."""
import argparse
import collections
import csv
import html
import hashlib
import json
import re
import zipfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sessions", type=Path, nargs="+", required=True)
    parser.add_argument("--validation", type=Path, nargs="+", required=True)
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    rows, summaries, sections = [], [], []
    latest_positions = {}
    for position, directory in enumerate(args.sessions):
        for case in json.loads((directory / "results.json").read_text(encoding="utf-8")):
            latest_positions[case["id"]] = (position, case)
    catalog = None
    for index, session in enumerate(args.sessions):
        prefix = "../" + session.name + "/"
        summary = json.loads((session / "summary.json").read_text(encoding="utf-8"))
        cases = json.loads((session / "results.json").read_text(encoding="utf-8"))
        catalog = json.loads((session / "catalog.json").read_text(encoding="utf-8"))
        captions = (session / "walkthrough.srt").read_text(encoding="utf-8")
        captions = re.sub(r"(\d\d:\d\d:\d\d),(\d{3})", r"\1.\2", captions)
        (session / "walkthrough.vtt").write_text("WEBVTT\n\n" + captions, encoding="utf-8")
        summaries.append(dict(summary, session=session.name))
        cards = []
        for case in cases:
            row = dict(case, session=session.name)
            rows.append(row)
            images = "".join('<a href="' + prefix + html.escape(path) + '"><img loading="lazy" src="' + prefix + html.escape(path) + '" alt="' + html.escape(case["title"]) + '"></a>' for path in case["evidence"])
            seek = f"document.getElementById('video{index}').currentTime={case['seconds']};document.getElementById('video{index}').scrollIntoView();document.getElementById('video{index}').play()"
            retest = latest_positions.get(case["id"])
            if case["id"].startswith("gesture."):
                tool = case["id"].split(".", 1)[1]
                retest = latest_positions.get("residual." + tool) or latest_positions.get("extended." + tool) or retest
            annotation = ""
            if case["status"] != "passed" and retest and retest[1]["status"] == "passed":
                ri, later = retest
                jump = f"document.getElementById('video{ri}').currentTime={later['seconds']};document.getElementById('video{ri}').scrollIntoView();document.getElementById('video{ri}').play()"
                annotation = '<p><b>Later retest passed.</b> <button onclick="' + jump + '">Watch retest</button> The initial result remains below; read both notes for fixture or assertion corrections.</p>'
            cards.append('<article data-search="' + html.escape((case["title"] + " " + case["id"] + " " + case["status"] + " " + case["level"]).lower()) + '"><h3>' + html.escape(case["title"]) + '</h3><p><b>' + case["status"] + '</b> | ' + case["level"] + '</p>' + annotation + '<button onclick="' + seek + '">Watch at ' + str(round(case["seconds"])) + ' seconds</button><p>' + html.escape(case["note"]) + '</p><details><summary>Screenshot evidence</summary>' + images + '</details></article>')
        sections.append('<section><h2>' + html.escape(session.name) + '</h2><p>' + html.escape(json.dumps(summary["statuses"])) + '</p><video id="video' + str(index) + '" controls preload="metadata" src="' + prefix + 'live-walkthrough.mp4"><track kind="captions" src="' + prefix + 'walkthrough.vtt" srclang="en" label="Test cases" default></video><p><a href="' + prefix + 'walkthrough.srt">Caption sidecar</a> | <a href="' + prefix + 'chapters.txt">Chapter times</a> | <a href="' + prefix + 'command-coverage.csv">Engine command attempts</a></p>' + "".join(cards) + '</section>')
    validation = []
    ignored_tests = {}
    for directory in args.validation:
        if not (directory / "validation-results.json").exists():
            continue
        for result in json.loads((directory / "validation-results.json").read_text(encoding="utf-8")):
            result["directory"] = directory.name
            log = (directory / result["log"]).read_text(encoding="utf-8", errors="replace")
            totals = [tuple(map(int, match)) for match in re.findall(r"test result: \w+\. (\d+) passed; (\d+) failed; (\d+) ignored", log)]
            result["test_executions"] = {key: sum(row[i] for row in totals) for i, key in enumerate(["passed", "failed", "ignored"])}
            result["crashed_targets"] = [{"executable": binary, "exit": status} for binary, status in re.findall(r"process didn't exit successfully: `([^`]+)` \(exit code: ([^)]+)\)", log)]
            for test, reason in re.findall(r"^test (.+?) \.\.\. ignored(?:, (.*))?$", log, re.MULTILINE):
                ignored_tests[test] = {"test": test, "reason": reason.strip(), "source_log": directory.name + "/" + result["log"]}
            validation.append(result)
    tested = {r["id"] for r in rows}
    uncovered = [r for r in catalog["menus"] if r["id"] not in tested]
    counts = dict(collections.Counter(r["status"] for r in rows))
    latest = {r["id"]: r for r in rows}
    with (args.output / "latest-menu-results.csv").open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "label", "status", "session", "note"])
        writer.writeheader()
        for item in catalog["menus"]:
            outcome = latest.get(item["id"], {})
            writer.writerow({"id": item["id"], "label": item["label"], "status": outcome.get("status", "not_exercised"), "session": outcome.get("session", ""), "note": outcome.get("note", "")})
    with (args.output / "ignored-tests.csv").open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["test", "reason", "source_log"])
        writer.writeheader()
        writer.writerows(ignored_tests.values())
    tool_coverage = []
    for tool in catalog["tools"]:
        initial = latest.get("gesture." + tool)
        followup = latest.get("residual." + tool) or latest.get("extended." + tool) or latest.get("workflow.stroke." + tool)
        outcome = followup if followup and followup["status"] == "passed" else initial
        tool_coverage.append({"tool": tool, "activation": latest.get("tool." + tool, {}).get("status", "not_exercised"),
            "initial_gesture": initial["status"] if initial else "not_exercised", "representative_result": outcome["status"] if outcome else "not_exercised",
            "evidence_case": outcome["id"] if outcome else "", "level": outcome["level"] if outcome else "inventory"})
    with (args.output / "tool-coverage.csv").open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=list(tool_coverage[0]))
        writer.writeheader()
        writer.writerows(tool_coverage)
    summary = {"sessions": summaries, "cases": len(rows), "statuses": counts,
               "levels": dict(collections.Counter(r["level"] for r in rows)),
               "menu_rows": len(catalog["menus"]), "menu_rows_exercised": len(catalog["menus"]) - len(uncovered),
               "menu_rows_not_exercised": len(uncovered), "tool_coverage": tool_coverage,
               "latest_menu_statuses": dict(collections.Counter(latest.get(item["id"], {}).get("status", "not_exercised") for item in catalog["menus"])),
               "tools_with_observed_representative_result": sum(r["representative_result"] == "passed" for r in tool_coverage), "validation": validation}
    for name, value in [("summary.json", summary), ("results.json", rows), ("uncovered-menus.json", uncovered)]:
        (args.output / name).write_text(json.dumps(value, indent=2), encoding="utf-8")
    with (args.output / "coverage.csv").open("w", newline="", encoding="utf-8-sig") as file:
        fields = ["session", "id", "title", "level", "status", "note", "seconds"]
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
        writer.writerows({"id": r["id"], "title": r["label"], "level": "inventory", "status": "not_exercised"} for r in uncovered)
    checks = "".join('<li><a href="../' + r["directory"] + '/' + r["log"] + '">' + r["name"] + ' (' + r["directory"] + ')</a>: exit ' + str(r["exit_code"]) + ', ' + html.escape(json.dumps(r["test_executions"])) + ', crashed targets: ' + str(len(r["crashed_targets"])) + '</li>' for r in validation)
    document = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>PhotoCraft recorded feature baseline</title>
<style>body{font:16px system-ui;max-width:1100px;margin:32px auto;padding:0 20px;color:#e7e9ef;background:#171a21}video,img{max-width:100%;width:100%}article{padding:18px;margin:12px 0;background:#232833;border:1px solid #454c5b;border-radius:8px}a{color:#a5ccff}input,button{font:inherit;padding:10px;background:#303949;color:white;border:1px solid #627089;border-radius:5px}input{width:90%;position:sticky;top:8px;z-index:1}details{margin-top:12px}h3{margin-top:0}section{margin-top:40px}</style>
<h1>PhotoCraft recorded feature baseline</h1><p>Real desktop UI captured through GPU screenshots at 4 fps. Synthetic input drives the application's canvas handlers. Activation, menu smoke checks and behavioral assertions are separate evidence levels; a passed smoke check does not certify complete feature correctness.</p>'''
    document += '<p>' + str(len(rows)) + ' recorded cases | ' + str(len(uncovered)) + ' source menu rows not exercised.</p><p><a href="coverage.csv">Full coverage ledger</a> | <a href="summary.json">Run summary</a> | <a href="uncovered-menus.json">Remaining menu coverage</a></p><h2>Repository validation</h2><ul>' + checks + '</ul><label for="search">Find a feature or status</label><br><input id="search" placeholder="Brush, smart, failed, behavior…" oninput="for(const el of document.querySelectorAll(\'article\')) el.hidden=!el.dataset.search.includes(this.value.toLowerCase())">'
    document = document.replace('<h2>Repository validation</h2>', '<p><a href="report.md">Assessment and findings</a> | <a href="evaluation-checklist.csv">Your evaluation: evidence and limits</a> | <a href="guide.md">Reproduction guide</a> | <a href="recording-verification.json">Video verification</a></p><p><strong>Validation failed:</strong> the U16 partial-mip test failed again in isolation. Three GPU targets crashed in the workspace run and passed when rerun serially. Historical menu/input and corrected TGA assertion failures remain in the ledger.</p><h2>Repository validation</h2>')
    document += "".join(sections) + '</html>'
    (args.output / "index.html").write_text(document, encoding="utf-8")
    if args.archive:
        directories = [args.output] + args.sessions + args.validation
        public_files = []
        for directory in directories:
            for file in directory.rglob("*"):
                if file.is_file() and "private" not in file.relative_to(directory).parts and file.name != "artifact-manifest.json" and file.resolve() != args.archive.resolve():
                    public_files.append((file, directory.name + "/" + file.relative_to(directory).as_posix()))
        manifest = [{"path": relative, "bytes": file.stat().st_size, "sha256": hashlib.sha256(file.read_bytes()).hexdigest()} for file, relative in public_files]
        (args.output / "artifact-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        args.archive.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(args.archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            for file, relative in public_files:
                archive.write(file, relative)
            archive.write(args.output / "artifact-manifest.json", args.output.name + "/artifact-manifest.json")
    print(json.dumps({"output": str(args.output), "cases": len(rows), "statuses": counts}))


if __name__ == "__main__":
    main()
