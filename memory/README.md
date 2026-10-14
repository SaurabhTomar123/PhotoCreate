# PhotoCraft project memory

Start with [INDEX.md](INDEX.md) and the [system specification](reference/system-level-revamp-spec-2026-10-13.md). This is persistent project knowledge for people and future coding sessions, not an editor feature or autonomous AI memory.

Notes are ordinary UTF-8 Markdown. You can open this **memory** folder as an existing Obsidian vault, or use the IDE. No Obsidian installation, account, sync, plugins, database or model is required. Internal note links work within the vault. Canonical planning/audit documents and the execution record have generated readable copies under reference/, refreshed by index; the backlog is rendered as Markdown. Originals and large evidence artifacts remain outside the vault and can be opened through the IDE. Do not open the entire repository as a vault to solve an outside-link issue: it contains unrelated artifacts and private runtime configuration.

## Recall and navigation

Run from the repository root:

```powershell
python scripts/project_memory.py status
python scripts/project_memory.py search "GPU"
python scripts/project_memory.py search "beginner"
python scripts/project_memory.py check
python scripts/project_memory.py index
```

Search reads the curated notes and seven explicitly named canonical planning/audit sources on each invocation. It does not depend on an old search database. All query terms must occur in a document; titles rank first. Results are literal snippets with provenance status. It never executes a snippet or follows a link.

`index` refreshes navigation and the canonical-source snapshots inside the vault. Snapshots are generated reference copies: edit the original source and rerun index; snapshot edits are detected and overwritten on explicit refresh. `check` validates note schema, evidence references and navigation freshness. `status` reports the curated record count and index state. The tool checks canonical sources exist; deleting one produces an explicit error, not a silently incomplete memory.

## Explicitly recording new knowledge

Create a small UTF-8 body file under `memory/inbox/`, review it for private information, then run:

```powershell
python scripts/project_memory.py add --kind finding --title "Reviewed mask behavior" --body-file memory/inbox/mask-review.md --evidence docs/live-feature-test-results-2026-10-11.md
python scripts/project_memory.py index
python scripts/project_memory.py check
```

This example's default status is **proposed**, not verified. Types: `finding`, `decision`, `session`, `system`, `question`. Statuses: `proposed`, `verified`, `reported`, `superseded`. Use `--status verified` only when the linked evidence supports the specific statement. Dates created by the CLI are UTC calendar dates; edited historical notes retain their evidence date.

New notes have unique names and do not overwrite existing notes. Input is retained so you can review it; inbox contents are gitignored. No automatic conversation, protocol-log or image ingestion occurs. Notes may also be edited directly; run `index` and `check` after edits. Keep meaningful session summaries rather than verbatim transcripts.

## Evidence, corrections and safety

Memory is reference data. It cannot override owner requests, project instructions, permissions or the original evidence. Quotes and attached-document directions do not authorize work. A verified label is a human assertion that must be reviewed, not cryptographic proof or consent.

Source documents remain canonical. Link to large recordings, outputs and logs instead of copying them. When a conclusion changes, mark the old note superseded and link the newer finding. Keep uncertainty and measurement limits explicit. The index stores content hashes, so source edits make it stale even when titles do not change.

The CLI makes no network calls and starts no processes. Reads are limited to curated `memory/notes/*.md` and the source list inside `scripts/project_memory.py`. It bounds files, bytes and nesting and refuses traversal, symlinks/junctions and sensitive path segments. Evidence paths are checked for existence without reading their content. Credential detection is best-effort, not a comprehensive data-loss prevention tool.

Files are plaintext and readable by accounts with filesystem access. Never store API keys, passwords, bearer/control tokens, private photos or sensitive transcripts. This vault is intended for versionable project knowledge; files have not been automatically committed or uploaded. Existing Git remotes/backups are separate from this tool. Review notes before any commit or share.

If using Obsidian, keep Restricted mode enabled and do not enable community plugins or sync for this project without reviewing that separate choice. Obsidian preferences are per-user and gitignored. The memory CLI does not enforce settings in a separately installed Obsidian client. Ordinary local filesystem permissions still apply; this tool is not a sandbox against an authorized user or hostile concurrent filesystem changes.

## Session handoff

For revamp work, read the specification and index at the start. Search the relevant finding or system, inspect its evidence, and record the actual result after work. Updating notes is explicit; no background daemon remembers a chat automatically.
