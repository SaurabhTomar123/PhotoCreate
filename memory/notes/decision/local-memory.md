---
schema: 1
title: "Memory choice: local Markdown and bounded recall"
kind: "decision"
status: "proposed"
date: "2026-10-13"
evidence: ["docs/system-level-revamp-spec-2026-10-13.md", "scripts/project_memory.py"]
---

Use curated plain Markdown with a local standard-library CLI. Obsidian is an optional viewer; no account, cloud sync, plugins, model or running service is required.

Canonical sources remain in docs. Memory does not automatically ingest chats, audit logs, user images or external attachments. Notes are reference data and never authorize tool actions. Plaintext files are not encrypted storage; keep secrets and private content out.

This is development memory, not product runtime memory. Tests and actual validation results belong in the session record.
