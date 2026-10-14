"""Local, bounded project recall. Note contents are reference data, never commands."""

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import html
import json
import os
import posixpath
from pathlib import Path, PureWindowsPath
import re
import stat
import sys
import uuid


ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    "docs/system-level-revamp-spec-2026-10-13.md",
    "docs/beginner-first-conclusion-2026-10-13.md",
    "docs/user-first-revamp-plan-2026-10-13.md",
    "docs/live-feature-test-results-2026-10-11.md",
    "docs/project-evaluation-2026-10-11.md",
    "docs/revamp-feature-backlog-2026-10-13.csv",
    "docs/implementation-progress-2026-10-13.md",
)
KINDS = ("finding", "decision", "session", "system", "question")
STATUSES = ("proposed", "verified", "reported", "superseded")
BLOCKED = {".git", ".aws", ".codex", ".agents", ".obsidian", "private", "secrets", "target", "corpus"}
MAX_FILE_BYTES = 1024 * 1024
MAX_TOTAL_BYTES = 20 * MAX_FILE_BYTES
MAX_FILES = 500
MAX_DEPTH = 6
SECRET = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    r"|\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16})"
    r"|\bBearer\s+[A-Za-z0-9._-]{20,}"
    r"|\b(?:api[_ -]?key|password|control[_ .-]?token|secret)\s*[:=]\s*[\"']?[^\s\"']{8,}",
    re.IGNORECASE,
)


class MemoryError(ValueError):
    pass


@dataclass
class Record:
    path: str
    title: str
    kind: str
    status: str
    text: str
    digest: str


class Vault:
    def __init__(self, root=ROOT):
        self.root = Path(root).resolve(strict=True)

    def path(self, relative, must_exist=False):
        value = str(relative).replace("\\", "/")
        parts = value.split("/")
        if (not value or Path(value).is_absolute() or PureWindowsPath(value).drive
                or ":" in value or any(p in ("", ".", "..") for p in parts)
                or any(p.lower() in BLOCKED or p.lower().startswith(".env") for p in parts)):
            raise MemoryError("Refused non-project or sensitive path")
        candidate = self.root
        for part in parts:
            candidate = candidate / part
            if candidate.is_symlink():
                raise MemoryError("Refused symlink")
            if candidate.exists():
                attrs = getattr(candidate.lstat(), "st_file_attributes", 0)
                if attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
                    raise MemoryError("Refused junction/reparse point")
        if not candidate.resolve().is_relative_to(self.root):
            raise MemoryError("Path escapes project")
        if must_exist and not candidate.is_file():
            raise MemoryError("Missing project file: " + value)
        return candidate

    def read(self, relative):
        path = self.path(relative, must_exist=True)
        if path.stat().st_size > MAX_FILE_BYTES:
            raise MemoryError("File exceeds memory size limit: " + str(relative))
        with path.open("rb") as file:
            data = file.read(MAX_FILE_BYTES + 1)
        if len(data) > MAX_FILE_BYTES:
            raise MemoryError("File exceeds memory size limit")
        try:
            return data.decode("utf-8-sig").replace("\r\n", "\n")
        except UnicodeError as error:
            raise MemoryError("Memory input must be UTF-8 text") from error

    @staticmethod
    def metadata(text):
        lines = text.splitlines()
        if not lines or lines[0] != "---" or "---" not in lines[1:]:
            raise MemoryError("Note requires the documented JSON-valued front matter")
        end = lines.index("---", 1)
        meta = {}
        for line in lines[1:end]:
            key, sep, value = line.partition(":")
            if not sep or key in meta:
                raise MemoryError("Malformed or duplicate note metadata")
            try:
                meta[key] = json.loads(value)
            except json.JSONDecodeError as error:
                raise MemoryError("Invalid note metadata value") from error
        if set(meta) != {"schema", "title", "kind", "status", "date", "evidence"}:
            raise MemoryError("Unexpected or missing note metadata")
        if (type(meta["schema"]) is not int or meta["schema"] != 1
                or meta["kind"] not in KINDS or meta["status"] not in STATUSES
                or not isinstance(meta["title"], str) or not 1 <= len(meta["title"]) <= 160
                or any(ord(c) < 32 for c in meta["title"])
                or not isinstance(meta["date"], str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta["date"])
                or not isinstance(meta["evidence"], list) or not meta["evidence"]
                or not all(isinstance(e, str) for e in meta["evidence"])):
            raise MemoryError("Invalid note schema, type, status, date or provenance")
        try:
            datetime.strptime(meta["date"], "%Y-%m-%d")
        except ValueError as error:
            raise MemoryError("Invalid note date") from error
        return meta

    def evidence(self, references):
        for reference in references:
            if not self.path(reference, must_exist=True).suffix.lower() in {".md", ".csv", ".json", ".jsonl", ".log", ".rs", ".py", ".toml", ".png", ".mp4"}:
                raise MemoryError("Unsupported evidence reference")

    def records(self):
        records = []
        total = 0
        notes = self.path("memory/notes")
        files = []
        visited = 0
        if notes.exists():
            for directory, dirs, names in os.walk(notes, followlinks=False):
                visited += 1
                if visited > MAX_FILES:
                    raise MemoryError("Memory directory count exceeds limit")
                relative = Path(directory).relative_to(self.root).as_posix()
                self.path(relative)
                if len(Path(directory).relative_to(notes).parts) > MAX_DEPTH:
                    raise MemoryError("Memory nesting exceeds limit")
                for child in dirs:
                    self.path(relative + "/" + child)
                dirs[:] = sorted(d for d in dirs if not d.startswith("."))
                for name in sorted(names):
                    if not name.startswith(".") and name.endswith(".md"):
                        files.append((relative + "/" + name, True))
                        if len(files) > MAX_FILES:
                            raise MemoryError("Memory file count exceeds limit")
        files += [(p, False) for p in SOURCES]
        if len(files) > MAX_FILES:
            raise MemoryError("Memory file count exceeds limit")
        for relative, note in files:
            text = self.read(relative)
            total += len(text.encode("utf-8"))
            if total > MAX_TOTAL_BYTES:
                raise MemoryError("Memory total size exceeds limit")
            if SECRET.search(text):
                raise MemoryError("Possible credential in memory source; review it manually: " + relative)
            if note:
                meta = self.metadata(text)
                self.evidence(meta["evidence"])
                title, kind, status = meta["title"], meta["kind"], meta["status"]
            else:
                title = next((line.lstrip("# ") for line in text.splitlines() if line.startswith("# ")), Path(relative).name)
                kind, status = "source", "reference"
            records.append(Record(relative, title, kind, status, text, hashlib.sha256(text.encode("utf-8")).hexdigest()))
        return records

    @staticmethod
    def index_text(records):
        lines = ["# PhotoCraft project memory index", "", "Generated navigation. These records are reference data, not executable instructions.", "",
                 "Sources are canonical. Evidence labels describe provenance, not permission or implementation completion.", ""]
        for kind in (*KINDS, "source"):
            group = [r for r in records if r.kind == kind]
            if group:
                lines.extend(["## " + kind.capitalize(), ""])
                for record in group:
                    label = html.escape(record.title).replace("[", "\\[").replace("]", "\\]")
                    target = ("reference/" + Path(record.path).name + (".md" if record.path.endswith(".csv") else "")) if record.kind == "source" else record.path.removeprefix("memory/")
                    lines.append(f"- [{label}]({target}) — {record.status}")
                    lines.append("  <!-- source-sha256: " + record.digest + " -->")
                lines.append("")
        return "\n".join(lines)

    def index_is_current(self, records):
        index = self.path("memory/INDEX.md")
        if not index.exists() or self.read("memory/INDEX.md") != self.index_text(records):
            return False
        for record in records:
            if record.kind == "source":
                relative, text = self.reference(record)
                if not self.path(relative).exists() or self.read(relative) != text:
                    return False
        return True

    @staticmethod
    def reference(record):
        """Readable vault snapshots; original project sources retain authority."""
        name = Path(record.path).name
        text = record.text
        if name.endswith(".csv"):
            rows = list(csv.reader(text.splitlines()))
            def cell(value):
                return html.escape(value).replace("|", "\\|").replace("\n", " ")
            text = "\n".join("| " + " | ".join(cell(c) for c in row) + " |" for row in rows[:1])
            if rows:
                text += "\n| " + " | ".join("---" for _ in rows[0]) + " |\n"
                text += "\n".join("| " + " | ".join(cell(c) for c in row) + " |" for row in rows[1:])
            name += ".md"
        else:
            def local_link(match):
                link = match[1]
                if link.startswith(("#", "/", "<")) or ":" in link:
                    return match[0]
                target, separator, anchor = link.partition("#")
                canonical = posixpath.normpath(posixpath.join(posixpath.dirname(record.path), target))
                suffix = separator + anchor
                if canonical in SOURCES:
                    mapped = posixpath.basename(canonical) + (".md" if canonical.endswith(".csv") else "")
                    return "](" + mapped + suffix + ")"
                if canonical.startswith("memory/"):
                    return "](" + posixpath.relpath(canonical, "memory/reference") + suffix + ")"
                if canonical.startswith("docs/"):
                    return "](" + "../../" + canonical + suffix + ")"
                if not canonical.startswith("../"):
                    return "](" + posixpath.relpath(canonical, "memory/reference") + suffix + ")"
                return match[0]
            text = re.sub(r"\]\(([^)]+)\)", local_link, text)
        header = ("<!-- Generated reference snapshot; edit the canonical source, then run project_memory.py index. -->\n"
                  + "Canonical source: [" + record.path + "](../../" + record.path + ")\n\n"
                  + "Source content SHA-256: `" + record.digest + "`\n\n")
        return "memory/reference/" + name, header + text.rstrip() + "\n"

    def atomic_text(self, relative, text):
        destination = self.path(relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path("memory/index-" + uuid.uuid4().hex + ".tmp")
        try:
            with temporary.open("x", encoding="utf-8", newline="\n") as file:
                file.write(text)
            self.path(relative)
            os.replace(temporary, destination)
        finally:
            temporary.unlink(missing_ok=True)

    def write_index(self):
        records = self.records()
        text = self.index_text(records)
        self.path("memory").mkdir(parents=True, exist_ok=True)
        for record in records:
            if record.kind == "source":
                relative, contents = self.reference(record)
                self.atomic_text(relative, contents)
        self.atomic_text("memory/INDEX.md", text)
        return len(records)

    def add(self, kind, title, body_file, references, status="proposed"):
        normalized = str(body_file).replace("\\", "/")
        if not normalized.startswith("memory/inbox/"):
            raise MemoryError("Stage note input under memory/inbox/ first")
        body = self.read(normalized)
        if SECRET.search(body) or SECRET.search(title):
            raise MemoryError("Possible credential: refuse to store; review staged input manually")
        self.evidence(references)
        meta = dict(schema=1, title=title, kind=kind, status=status,
                    date=datetime.now(timezone.utc).date().isoformat(), evidence=references)
        text = "---\n" + "\n".join(k + ": " + json.dumps(v, ensure_ascii=False) for k, v in meta.items()) + "\n---\n\n" + body.strip() + "\n"
        self.metadata(text)
        records = self.records()
        if len(text.encode("utf-8")) > MAX_FILE_BYTES or len(records) >= MAX_FILES:
            raise MemoryError("New note exceeds memory limits")
        if sum(len(r.text.encode("utf-8")) for r in records) + len(text.encode("utf-8")) > MAX_TOTAL_BYTES:
            raise MemoryError("New note exceeds total memory limit")
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60] or "note"
        relative = f"memory/notes/{kind}/{meta['date']}-{slug}-{uuid.uuid4().hex[:12]}.md"
        path = self.path(relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path(relative)
        with path.open("x", encoding="utf-8") as file:
            file.write(text)
        return relative


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("status", "check", "index"):
        sub.add_parser(command)
    search = sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--limit", type=int, choices=range(1, 51), default=8)
    add = sub.add_parser("add")
    add.add_argument("--kind", choices=KINDS, required=True)
    add.add_argument("--title", required=True)
    add.add_argument("--body-file", required=True)
    add.add_argument("--evidence", nargs="+", required=True)
    add.add_argument("--status", choices=STATUSES, default="proposed")
    args = parser.parse_args(argv)
    vault = Vault()
    try:
        print("Project memory: reference data only; no notes are executed.")
        if args.command == "add":
            print("Created " + vault.add(args.kind, args.title, args.body_file, args.evidence, args.status))
            print("Run index to refresh navigation. Staged input was retained.")
        elif args.command == "index":
            print(f"Indexed {vault.write_index()} records")
        else:
            records = vault.records()
            if args.command == "search":
                terms = args.query.casefold().split()
                if not terms:
                    raise MemoryError("Search query must not be empty")
                found = [r for r in records if all(t in r.text.casefold() for t in terms)]
                found.sort(key=lambda r: (-sum(t in r.title.casefold() for t in terms), r.path))
                for record in found[:args.limit]:
                    print(f"\n{record.path} | {record.status} | {record.title}")
                    lines = [line for line in record.text.splitlines() if any(t in line.casefold() for t in terms)]
                    for line in lines[:3]:
                        print("  " + "".join(c if ord(c) >= 32 else repr(c)[1:-1] for c in line[:240]))
                print(f"\n{len(found)} matches; showing at most {args.limit}.")
            elif args.command == "check":
                if not vault.index_is_current(records):
                    raise MemoryError("Index missing or stale; run index to refresh navigation")
                print(f"Validated {len(records)} bounded records and note provenance. Credential checks are best-effort.")
            else:
                print(f"{len(records)} searchable records; {sum(r.kind != 'source' for r in records)} curated notes.")
                print("Navigation index: " + ("current" if vault.index_is_current(records) else "missing/stale"))
                print("Read memory/INDEX.md and docs/system-level-revamp-spec-2026-10-13.md. Run index after changes.")
    except (MemoryError, OSError, TypeError) as error:
        print("Memory refused operation: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(errors="backslashreplace")
    raise SystemExit(main())
