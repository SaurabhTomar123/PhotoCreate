# Claude lane: editorial poster progress

Owner of this file: Claude (work plan [codex-claude-work-plan-2026-10-15.md](codex-claude-work-plan-2026-10-15.md), packets L1–L4). Codex consolidates it into the canonical backlog and memory at integration.

## Batch 1 — 15 October 2026: L1 specification, command map, manual proof

**Branch:** `claude/editorial-poster`, cut from PhotoCreate `main` at `388a0077`. This is the current accepted base, **not** the qualified upstream candidate (`df055f3`) Codex is still qualifying; no shared dependency has been coded, so nothing here needs rebasing yet. Head: the commit that adds this file (see `git log`).

**Scope delivered (L1, plus the inputs L2/L3 need):**

| File | What it is |
|---|---|
| `docs/claude-editorial-poster-spec.md` | "Make an editorial poster": inputs, three art directions with layer stacks, deterministic variations, flow, progressive depth, empty/error/warning states, keyboard and accessibility, acceptance tests, decisions needed |
| `docs/claude-editorial-poster-command-map.md` | Every command the recipe uses, with parameters, returns, real preconditions and observed behaviour; readiness predicates bounded to those commands; one-step apply/rollback design reusing the existing compound-command pattern; the shared-file patches Codex would apply |
| `records/2026-10-15/claude-editorial-poster/` | Three rendered prototypes (one per direction), their exact command logs, layer trees (`info --compact`), a reproduction script and image sources |
| `docs/claude-editorial-poster-progress.md` | This report |

No product source, shared registration file, Cargo manifest, lock file or xtask file was changed.

**Commands run and results**

| Check | Command | Result |
|---|---|---|
| Registry dump | `photocraft-cli commands --json` (0.9.0) | 909 commands; recipe commands and parameters recorded in the map |
| Direction A (square photo) | `reproduce.sh`, section A | Exit 0; 7 layers (smart object clipped to shape, 3 type, 2 shapes, background) |
| Direction B (landscape photo) | section B | Exit 0; photo, gradient map, gradient fill (Multiply), 2 type |
| Direction C (landscape photo) | section C | Exit 0; 2 shapes, clipped photo, clipped black-and-white, 5 type |
| Missing font | `type.create` with an unknown family | Succeeds with a fallback face and a `warnings` entry |
| Clip the bottom layer | `layer.setProps {"clipped":true}` on a one-layer document | Returns `null`, no error, nothing visible: a silent no-op |
| History granularity | `file.new` + 3 commands | 4 history entries: one per command |
| Candidate-base drift | `git diff c699e3c df055f3` for the recipe's commands and `ops/src/lib.rs` | Parameter docs unchanged; Free Transform frame now follows a selection; history folding API unchanged |

Tools: official signed `photocraft-cli` 0.9.0 (`c699e3cda`, Windows x64), Git Bash. Nothing was compiled; no GPU test or benchmark was run, so this batch did not use the shared hardware queue.

**Recordings:** none yet. The prototypes are still renders (`*-preview.jpg`), not screen recordings; the recorded end-to-end recipe belongs to L4.

**Known gaps and limits**

- The previews use fonts installed on this machine (Playfair Display, Bebas Neue, Montserrat Black). Only Inter is bundled; on another machine the fallback chain applies and the look changes. Bundling open-licence display fonts needs an owner decision and the craft-fonts process.
- Layout numbers in the prototypes were computed by hand for two images. The recipe engine must compute them from returned bounds; title fitting (`type.info` → `type.setStyle`) is designed but not exercised.
- 16-bit, CMYK and Lab photos, very large photos, `document.sampleColor` contrast checks and `layer.select` were not exercised.
- No one-step undo or rollback exists yet; §5 of the map is a design to implement in L3 and test (history trimming under the memory budget is a named risk).
- The registry and runs come from 0.9.0, two commits after this branch's base; the map must be re-checked against the base Codex pins before L3 code depends on it.

**Decisions needed (owner / Codex):** new document always (recommended); default format (Portrait 4:5 at 150 ppi proposed); recipe command id and the shared-file patches in map §6; display fonts.

**Next (pending the qualified base SHA from Codex):** L2 readiness for the mapped commands only; L3 `recipe_cmds` module with deterministic layout, fitting, variations and the fold/rollback; L4 guided tray in a new `ui-egui` module.
