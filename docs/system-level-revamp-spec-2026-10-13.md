# PhotoCraft system-level revamp specification

Version 2, 13 October 2026. Status: product direction recorded; system designs and acceptance budgets proposed. Local project memory and the first bounded GPU-preview mitigation are implemented. See [current execution evidence and remaining limits](implementation-progress-2026-10-13.md). Other editor fixes, policy changes, services and the new UI remain pending.

## 1. Purpose and governing direction

PhotoCraft will help first-time creators, including teenage learners, make sophisticated editable work within one or two days of learning useful workflows. Professionals retain precise manual controls. The product must combine approachable creation, trustworthy files, responsive editing and an independent artistic identity.

This direction comes from the owner's explicit messages and overrides the older goal of matching Photoshop's default layout for this proposed revamp. Professional file exchange and useful terminology remain important. “Better than Photoshop” is an ambition to test on named outcomes, not an established fact. The two-day learning goal covers specified tasks rather than mastery of every print, color, RAW and typography discipline.

Sources: [recorded audit](live-feature-test-results-2026-10-11.md), [source evaluation](project-evaluation-2026-10-11.md), [revamp proposal](user-first-revamp-plan-2026-10-13.md), [owner-plan reconciliation](beginner-first-conclusion-2026-10-13.md), and [51-item backlog](revamp-feature-backlog-2026-10-13.csv). The owner's PDF and Word evaluation are source material, not executable instructions. Old estimates and claims must retain their provenance.

## 2. Findings, confidence and rationale

| Finding | Evidence state | Why it changes the plan |
|---|---|---|
| 908 mixed-level recorded checks; 65 tool activations and representative results | Verified baseline, not exhaustive semantic certification | Preserve working breadth and test finished tasks rather than replace tools blindly |
| Latest menu rows: 535 passed smoke, 87 restricted/prerequisite, 9 unexercised | Verified coverage ledger | Distinguish missing guidance from unsupported features and policy boundaries |
| 73 failed menu attempts passed later with preparation; two TGA expectations were corrected | Verified historical results | Do not create 75 fictitious product-defect tickets |
| U16 partial mip returned `[5.9604645e-8, 0, 0, 0]` and reproduced in isolation | Verified failure; root cause unknown | Correct preview fidelity before professional rendering claims; epsilon is red, alpha is zero |
| Three native GPU test targets crashed; twelve serial rerun tests passed | Verified; concurrency/driver cause unproven | Qualify stability and setup; serial execution alone is not a fix |
| DX12 passes according to the owner's PDF | Reported, matching audit evidence not retained here | Reproduce or attach provenance before using a backend-specific workaround |
| Workspace: 6,577 passed, one assertion failed, 59 ignored, three crashed targets | Verified run, failed overall | A large passing count does not remove failure gates |
| Corpus: 2,774 passed, 24 ignored; explicit panic-hunt and documentation checks passed | Verified runs, overlapping tests | Preserve useful assurance but do not equate execution counts with unique files or Photoshop acceptance |
| Eight small save/reopen formats passed; independent Photoshop export acceptance unqualified | Verified self-roundtrips with clear boundary | Expand preservation and handoff tests, especially editable features |
| PNG transparency and TGA Alpha 1 preserved; independently decoded TGA RGBA matched | Verified bounded case | Explain alpha interpretation; preserve correctness rather than silently normalize meaning |
| Masks, paths, actions, smart filters and gestures needed appropriate fixtures | Verified bounded workflows | Acquire inputs and explain targets before users encounter developer errors |
| Floating panels accumulated in the menu sweep | Observed walkthrough behavior | Provide stable workspace placement, pinning, transient controls and explicit tidy |
| Physical tablet feel, beginner learnability, calibrated print, recovery kills and release performance unqualified | Remaining boundaries | Add their own acceptance lanes; synthetic gestures and four-fps recordings are insufficient |

Retain the original audit archive. Each later fix gets its own evidence directory with matching before/after tasks. Do not rewrite historical failures as passes.

## 3. System boundary and existing foundation

The editor remains native Rust, egui/eframe and wgpu; no webview shell or JavaScript UI is introduced. Engine commands remain the shared action path for manual editing and automation. Documents, masks, layers, color and format models remain the source of truth. The UI presents intent and state rather than inventing independent editing semantics.

Existing responsibilities: `engine` owns command execution; `doc`/`ops` own editable data and history; `compose`/`gpu` supply rendering; `io`/`codecs` handle interchange; `ui-egui` owns presentation and canvas interactions; `automation` owns resource boundaries. This is a responsibility map, not a commitment to create nine new crates.

The new knowledge vault is development tooling. It is not an embedded editor feature, an AI runtime, a user-photo database or an always-running process. Adding app-level memory later would require a separate user-consent, privacy, storage and lifecycle design.

## 4. The eight foundation systems and creation experience

### S1. Rendering trust / GPU Sentinel

Inputs: adapter/backend/driver identity, document depth, dirty regions, rendered previews and health signals. Outputs: correct canvas, bounded diagnostics, a disclosed fallback state and retained document edits.

First enrich the failing assertion with image size, pixel location and mip path; compare partial and full rebuilds across relevant sizes, depths and backends. Evaluate scratch targets as a candidate workaround, not a proven cure. Separate adapter-unavailable, skipped, assertion-failed and native-crash states. Recovery must preserve document/history and avoid loops of GPU retry. Field checks must be bounded and measured; a readback on every gesture cannot be adopted without proving its responsiveness cost.

Acceptance: reproduced invariant failure resolved with a regression test; sustained supported-hardware runs; truthful failure states; forced recovery preserves eligible edits. Vendor or backend cause remains a hypothesis until evidence establishes it.

### S2. Command readiness

Inputs: command identity, target state and typed prerequisites. Outputs: ready/not-ready with meaningful explanation and an optional preparation proposal.

A proposal identifies targets, changes, prerequisites, resource needs and irreversible consequences. Revalidate at execution because the document may have changed. Never silently choose unrelated layers, select everything, rasterize type or convert the master. Reversible multi-step edits form a coherent history transaction; partial failure must either roll back or explicitly disclose partial completion. Do not label “explained but impossible” as successful user completion.

Acceptance: qualified workflows explain disabled states before dispatch; offered preparation plans actually work and preserve the intended target.

### S3. Guided inputs

Inputs: typed parameter definitions, compatible assets, current context and user manipulation. Outputs: validated maps, planes, paths, selections, text or numeric values with units and preview.

Start with the eight default-invocation problem cases in the owner plan: Displace, Vanishing Point, four warp-split items, Find Layers and Load Selection. Provide direct picking/drawing and useful empty states. Automatic suggestions remain adjustable. A four-corner editor can ship before automatic perspective detection. Schema-derived validation supports UI, automation and generated hostile-input testing, but does not replace specialized visual workspaces.

Acceptance: no raw parameter-schema messages in these user flows; preview, cancel, apply and revision work on real content.

### S4. Resource-aware assistance

Inputs: declared resource use, resolved assets and granted scopes. Outputs: authorized execution or clear denial/consent request, with a reviewable plan.

Distinguish open-document read/write, built-in profiles, approved user profiles, scoped filesystem access, clipboard, printing and network. Verify transitive resource behavior before changing prefix rules. A declaration alone is not enforcement; referenced assets and underlying operations must honor the same limits. Missing declarations fail closed during migration. Retain existing controls until replacement boundaries are tested. An isolated clipboard can support tests without changing the user's OS clipboard.

Acceptance: intended document-only paths work; scope traversal and ungranted external access fail; existing protections are not weakened to inflate coverage.

### S5. Observable canvas

Inputs: completed/cancelled gestures, background operations and stable targets. Outputs: semantic journal entries, clear history names, accessible feedback and replay context.

Specify event target, before/after state or revision, completion status and correlation to the originating gesture. Do not announce every pointer movement. Background-job start is not job success. Events accompany state, pixels and saved-output checks, since emitted events can be incorrect. Accessibility also requires reachable controls, focus and navigation; announcements alone are insufficient.

Acceptance: representative tool effects have coherent feedback and verified state; keyboard and screen-reader tasks have their own qualification.

### S6. Calm workspace

Inputs: task, current tool, work area, pinned panels and user layout. Outputs: stable accessible controls and visible artwork.

Reserve edges and predictable drawers. Use explicit Tidy, Pin, Collapse and Reset actions. Transient controls can close when a task ends; pinned controls persist. Suggest task layouts without stealing focus or changing tools. Do not chase the cursor with moving panels. The new shell exposes precision while keeping twelve tray categories from becoming twelve permanently expanded panels.

Acceptance: laptop-sized, scaled, dense and wide-window tasks; no important handle/caret covered; layout survives document changes and restart.

### S7. Honest exchange

Inputs: document features, target format/options and intended destination. Outputs: preflight, delivery preview, explicit losses, export result and preserved master.

Check dimensions, depth, profile, alpha interpretation, text, masks, layers, filters, links and fonts. Offer suitable alternatives without asserting every feature is preserved when untested. Keep completion warnings for issues discovered during export. Rendered equality and feature preservation are separate checks. Independent parsers add evidence; a named target editor is needed to qualify that specific handoff. Alpha-as-mask versus transparency needs a reversible explanation and preview.

Acceptance: losses explained before qualified exports; native master retained; independent acceptance matrix names versions and feature limits; saved/exported state is truthful.

### S8. Living audit

Inputs: pinned fixtures, workload/hardware definitions, scripts, planned tasks and expected evidence. Outputs: pass/fail/skip/unavailable/restricted results, logs, outputs, video times and an honest dashboard.

Lanes: behavior, rendered pixels, save/recovery trust, release responsiveness, scale, physical input and novice usability. Fast checks, nightly recordings and expensive hardware sessions have separate schedules. Do not merely screenshot-diff every frame without controlling state, scale, timing and legitimate visual changes. Synthetic tablet replay detects some regressions, not real hardware feel. Failed, flaky or absent evidence stays visible.

Acceptance: reproducible runs; explicit provenance; actionable failures; recorded task outcomes and output review; bounded machine/time budgets.

### S9. Beginner creation and learning

Inputs: desired outcome, user content, context and explicit choices. Outputs: sophisticated editable results, understandable controls and a route to precise editing.

Start with poster, cutout/composite, cleanup, grade and artistic print. Three differentiated previews use actual user content. Templates/recipes adapt to subject placement, text length and output size. Defaults are visible and revisable; uncertain suggestions allow manual correction. Create, Explore and Precise reveal controls in the same document. Short teaching explains the current operation; users can skip it. Finishing checks identify legibility, halos, cropping, resolution and delivery problems without declaring artistic taste objectively wrong.

Acceptance: novice task completion and day-two transfer to unfamiliar content; blind output review; expert access to precision; complete offline manual paths. Cloud generation is optional future scope, not a dependency of learning or basic editing.

## 5. Cross-system contracts

| Contract | Required behavior | Reason |
|---|---|---|
| Command description | ID, targets, prerequisites, inputs/ranges/units, effects, resource needs and reversibility | Shared truthful understanding for UI and assistance |
| Preparation plan | Explain changes, preview targets, request necessary grants, revalidate before run | Avoid surprise destructive or mis-targeted help |
| Editable recipe | Named steps, parameters, relative targets, protected regions and revision handling | Adapt a sophisticated result to new content |
| History transaction | Coherent undo for reversible edits; explicit policy for partial failure | “Smart” must not mean harder to recover |
| Gesture feedback | Correlate semantic outcome with document/view state and job completion | Observe actual success and make learning accessible |
| Export preflight | Feature-specific analysis with confidence and final warnings | Keep loss disclosure truthful even on edge cases |
| Evidence record | Source, date, checkout, workload, evidence level, result and limits | Prevent proposals, historical claims and measurements from blending |

Cancellation stops or safely completes the current operation according to a documented rule; it must not silently discard unrelated edits. Scope denial, empty selection, incompatible layer, unavailable adapter, missing font/file, insufficient memory and save failure need useful recoverable states. Layout changes do not alter document data.

## 6. UI and professional scope

Proposed visual direction: Atelier, an independent contemporary studio with calm outer chrome, neutral image surrounds, clear typography and restrained accent. It is not an approved final mockup. Core structure: canvas, stable tool rail, contextual controls, main inspector, optional trays, comparison/history and delivery state.

Trays: References, Assets, Brushes, Materials, Color, Looks, Masks, Retouch, Type/Layout, Variations, Recipes and Delivery. Discoverable categories are not mandatory simultaneous panels. Workspaces support task layouts, manual precision, scalable controls, reduced motion, keyboard access and predictable focus.

Professional destination: reliable documents/recovery; layers/masks/blending/smart edits; difficult selections; transforms/warp; retouch; pen/brush feel; calibrated color; RAW and photographic assembly; multilingual type; vectors/artboards; supported-format exchange; print/export; reusable assets; actions/batch; motion; optional AI; accessibility/languages; workspaces/ecosystem. The requirement ledger below links each concrete item to its outcome and acceptance task. Preserve working paths while deepening or adding what is missing.

## 7. Sequence and proposed qualification budgets

Stages: 0 establish evidence and test tasks; 1 trust; 2 reachability; 3 responsiveness; 4 beginner success; 5 distinct shell; 6 professional depth/handoff; 7 artistic expansion. Exploration and prototype research can proceed alongside trust work; shipping cannot disguise unresolved blockers. These are dependencies and gates, not elapsed-time promises.

Responsiveness targets remain proposed: common feedback within 50 ms p95; 60 fps canvas interaction on a published reference workload; physical pen-to-visible at or below 30 ms; adjustment preview within 100 ms p95; edge preview within 150 ms. The owner's 20 ms layer target is a stretch goal pending fresh hardware/workload measurements. Define reference machines, cold/warm behavior, document depth, sizes and content before adoption. Debug RPC timing and four-fps recordings cannot qualify these budgets.

Learning targets remain proposed: at least 90% of novices finish a qualified first task in ten minutes without facilitator intervention; most complete three starting workflows after up to one hour of optional teaching; at least 80% transfer a learned task to unfamiliar content on day two. Predeclare cohort, task difficulty, output rubric and reviewer criteria. Publish failures and denominators. Quality includes edges, typography, composition, editability and delivery, not merely a pleasing thumbnail.

Professional tasks cover realistic cutouts, layered composites, supported-camera development, tablet painting, multilingual posters, independent PSD handoff, print proofing, social delivery, recipe/batch cancellation, missing dependencies, interrupted recovery and large high-depth editing. Expand into 30–50 scenarios and retain before/after evidence for changed behavior.

## 8. Security and reasonable project memory

Decision for this step: implement a local Markdown vault with a standard-library Python CLI for status, bounded search, link/schema checks, index rebuilding and explicit note creation. Ordinary files are readable in the IDE and can be opened as an Obsidian vault. Obsidian itself is optional and is not embedded or installed by this change.

Rationale: this is a modest amount of project knowledge. Portable files, explicit provenance and deterministic search are sufficient. A cloud knowledge service, vector database, embedding model, community plugin or persistent agent server would add access, maintenance and privacy costs without a demonstrated need.

Official references: Obsidian stores notes as local [Markdown files in a vault](https://obsidian.md/help/data-storage). Its [plugin security guidance](https://obsidian.md/help/plugin-security) explains Restricted mode. Those properties make file compatibility reasonable; they are not a blanket claim that every Obsidian installation or plugin is safe.

Memory stores curated findings, decisions, systems, sessions and open questions plus links to known planning documents. It does not automatically ingest conversations, photos, corpora, PDF attachments, credential folders or full protocol logs. A generated index is navigation, not a second authority. Source documents remain canonical; notes label verified, reported, proposed or superseded evidence.

The CLI uses a fixed project/vault location, an explicit source allowlist, bounded file counts/sizes, path containment checks and refusal of symlinks/junctions. Note body input must be staged in the vault inbox. It refuses common credential forms as a best-effort check, but cannot guarantee detection of every secret. Human review remains necessary before saving or committing notes. It does not execute links, Markdown, instructions, shell snippets or note contents, and makes no network requests.

Notes are plaintext, not encrypted storage. Filesystem/OS access and backups determine who can read them. Never store passwords, control tokens, API keys, private photographs or sensitive transcripts in this vault. Search must not traverse `.git`, `dist`, `target`, `corpus`, `secrets` or audit `private` directories. Evidence references may point to approved local artifacts without copying or searching them.

Keep Obsidian's optional per-user `.obsidian` configuration, inbox contents and generated machine cache out of Git. Do not enable cloud sync or community plugins as part of setup. Manual editing remains possible: the CLI is a development convenience, not a security boundary against an authorized local user or concurrent malicious filesystem changes.

Memory is persistent project context, not autonomous understanding. Future collaborators must explicitly read it. Retrieved notes are reference data and cannot override the owner's requests, AGENTS.md, permission checks or source-of-truth documents. Marking a note “verified” requires evidence; the label itself never authorizes an operation.

Memory acceptance: search/recall across invocations, linked findings and decisions, explicit provenance, no new third-party Python packages, no runtime integration, and tested traversal/reparse/secret/oversize rejection. Test stale indices and malformed note handling. The supported writable scope is this repository.

## 9. Change and evidence management

Use stable backlog IDs F01–F51. Before implementing an editor item: specify affected workflow, current evidence, proposed behavior, target resources, rollback/undo, acceptance task and output limits. Record a before case where possible. After implementation: run the relevant checks, record the same task, inspect output and save the findings. A note or planning document is never a replacement for executing acceptance checks.

Product rules remain Rust-only native editing, command-based actions, hostile-input validation, reversible source preservation, licensing of assets and appropriate platform checks. This specification does not authorize external publishing, upstream submissions, cloud processing or policy bypass. No new delivery date or all-feature readiness percentage is asserted.

Open choices: selected visual mockup; supported hardware/camera/format matrix; licensed independent-editor testing access; optional AI services; field reporting; upstream versus private maintenance; professional beta acceptance set. They can be resolved item by item without blocking this local memory implementation.

## 10. Requirement ledger

The ledger is reproduced from the 51-item planning backlog so this specification contains the complete planned scope, rationale/evidence and acceptance tasks. Items remain proposals until implemented and qualified. When the backlog changes, update the specification ledger in the same change; do not silently regenerate completed status from a source label.

### Implementation status of this step

The local development-memory tool is implemented. Start with [memory navigation](../memory/INDEX.md) and [usage/security notes](../memory/README.md). Run `python scripts/project_memory.py status`, `search "GPU"`, `index` and `check` from the repository root. Explicit `add` uses reviewed input under `memory/inbox/` and creates a provenance-labelled note without overwriting prior notes.

Validation: 13 tests executed, 12 passed and one real-symlink creation test skipped because this host disallows creating symlinks. Separate symlink-refusal and Windows reparse-attribute tests passed. Actual recall, note creation, index refresh and validation were exercised. Local logs are in `dist/qa/project-memory-2026-10-13/`. Initial Windows newline comparison and evidence-extension issues were corrected and retained in that record.

Memory searches seven curated notes and six explicitly listed source documents at handoff. This count can grow through explicit reviewed notes. No Obsidian desktop application, plugins, cloud service, database, product runtime integration, editor fixes or UI redesign was installed or implemented in this step. Performance/learnability targets and all F01–F51 product items remain proposals. Future work should update this status and its evidence rather than treating the specification as completion.

### F01 - Correct high-depth previews

- **Priority / stage:** P0 / 1
- **Current evidence / reason:** Reproduced U16 partial-mip failure
- **User outcome:** Edits display accurate opaque pixels at every supported zoom
- **Acceptance:** High-depth partial edits compared with full redraw and saved output
- **Owner system:** GPU Sentinel
- **Status:** local mitigation implemented and validated on AMD Vulkan/DX12; wider hardware/image qualification and S1 self-healing remain pending.

### F02 - GPU stability and recovery

- **Priority / stage:** P0 / 1
- **Current evidence / reason:** Three GPU targets crashed; serial passed
- **User outcome:** Work remains available through supported rendering failures
- **Acceptance:** Recorded hardware matrix and retained document recovery
- **Owner system:** GPU Sentinel
- **Status:** planning proposal; no completion implied.

### F03 - Save and autosave truth

- **Priority / stage:** P0 / 1
- **Current evidence / reason:** Small roundtrips passed; live forced-interruption recovery restored the latest completed autosave on a synthetic RGB8 fixture (14 October). Idle capture attempts timed out; save-status wording remains ambiguous.
- **User outcome:** Know when work is saved and recover interruption
- **Acceptance:** Interrupt editing; restore latest recoverable master; verify save status
- **Owner system:** Honest Exchange; Living Audit
- **Status:** partially qualified locally; three editable layers and independent PNG pixels preserved after termination/relaunch/native reopen. Interrupted writes, power loss, larger/high-depth/multi-document workloads and wider devices remain open. See [live recovery evidence](live-recovery-qualification-2026-10-14.md).

### F04 - External PSD/PSB acceptance

- **Priority / stage:** P0 / 6
- **Current evidence / reason:** Self roundtrip and corpus passed; external acceptance untested
- **User outcome:** Exchange editable work confidently
- **Acceptance:** Independent target app accepts exports and named editable features
- **Owner system:** Honest Exchange
- **Status:** planning proposal; no completion implied.

### F05 - Brush and canvas responsiveness

- **Priority / stage:** P0 / 3
- **Current evidence / reason:** Synthetic strokes passed; physical latency unmeasured
- **User outcome:** Ink follows the hand and navigation stays fluid
- **Acceptance:** Published release workload and physical tablet latency measurement
- **Owner system:** Living Audit: Feel
- **Status:** planning proposal; no completion implied.

### F06 - Layer and adjustment responsiveness

- **Priority / stage:** P0 / 3
- **Current evidence / reason:** The 33-stroked-shape layout exceeded a 32-entry split cache, repeating rasterization and uploads. A bounded 128-entry / 128 MiB cache qualified locally: quiet paired 12 MP / 174-layer opacity median 398.06 -> 25.48 ms, pixel-move commit 401.95 -> 31.35 ms. Histogram worker accumulation was separately fixed. Remaining refresh stages and demanding text moves still exceed the interaction budget.
- **User outcome:** Scrub opacity and blend without distracting stalls
- **Acceptance:** Input-to-visible p95 targets on reference photo and layer workloads
- **Owner system:** Living Audit: Feel
- **Status:** partial implementation: bounded histogram work and shape reuse passed local native, corpus, wasm and recorded workflow checks. The shape-cache fix provides a measured local speedup; the 16 ms target, larger working sets, other devices and native crash qualification remain open. See [implementation record](implementation-progress-2026-10-13.md).

### F07 - Transform controls and preview

- **Priority / stage:** P1 / 2
- **Current evidence / reason:** Prepared menus reachable; affordance gaps reported
- **User outcome:** See target and confirm or cancel precisely
- **Acceptance:** Multi-layer transform and warp task; accurate blended preview; undo
- **Owner system:** Guided Inputs
- **Status:** planning proposal; no completion implied.

### F08 - Selection Studio

- **Priority / stage:** P1 / 2
- **Current evidence / reason:** Basic selection/channel behavior passed; refinement depth unqualified
- **User outcome:** Refine difficult edges with visible output choices
- **Acceptance:** Hair and translucent cutout reviewed on multiple backgrounds
- **Owner system:** Guided Inputs
- **Status:** planning proposal; no completion implied.

### F09 - Retouch Studio

- **Priority / stage:** P1 / 2
- **Current evidence / reason:** Representative gestures and controlled Remove passed
- **User outcome:** Retouch precisely on editable layers
- **Acceptance:** Portrait/product sampling overlays; exclusions; source preserved
- **Owner system:** Guided Inputs
- **Status:** planning proposal; no completion implied.

### F10 - Layer and mask depth

- **Priority / stage:** P1 / 2
- **Current evidence / reason:** Basic layers and masks passed
- **User outcome:** Manage a complex composite clearly
- **Acceptance:** Nested groups; linked layers; clipping; mask targeting; persisted changes
- **Owner system:** Command Readiness
- **Status:** planning proposal; no completion implied.

### F11 - Pen and brush professional behavior

- **Priority / stage:** P1 / 3
- **Current evidence / reason:** No real tablet session
- **User outcome:** Use pressure and smoothing predictably
- **Acceptance:** Supported pen device tests and complete painting session
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F12 - Smart edits and live filters

- **Priority / stage:** P1 / 6
- **Current evidence / reason:** One editable Gaussian smart-filter workflow passed
- **User outcome:** Revisit effects without destroying the master
- **Acceptance:** Several masked filters; reorder; reopen; source and parameters preserved
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F13 - Typography depth

- **Priority / stage:** P1 / 6
- **Current evidence / reason:** Editable Latin text passed
- **User outcome:** Compose professional multilingual type
- **Acceptance:** Devanagari/Arabic; path text; variable fonts; missing-font handling
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F14 - Atelier visual shell

- **Priority / stage:** P1 / 5
- **Current evidence / reason:** Proposed replacement identity
- **User outcome:** Enjoy a distinct calm creative workspace
- **Acceptance:** Candidate designs exercised on the same retouch/design/paint tasks
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F15 - Contextual controls and task guidance

- **Priority / stage:** P1 / 2
- **Current evidence / reason:** Default menus needed explicit prerequisites
- **User outcome:** Understand controls and next steps
- **Acceptance:** Find unfamiliar tool; acquire input; preview; apply; revise without external help
- **Owner system:** Command Readiness; Guided Inputs
- **Status:** planning proposal; no completion implied.

### F16 - Tray system and workspace persistence

- **Priority / stage:** P1 / 2
- **Current evidence / reason:** Floating panels accumulated in recording
- **User outcome:** Reach more capabilities while keeping canvas clear
- **Acceptance:** Pin/resize/collapse; restore workspace; narrow window; multiple documents
- **Owner system:** Calm Workspace
- **Status:** planning proposal; no completion implied.

### F17 - Keyboard access and command search

- **Priority / stage:** P1 / 5
- **Current evidence / reason:** Core shortcuts partly exercised
- **User outcome:** Work quickly with predictable navigation
- **Acceptance:** Keyboard-only task; clear focus; searchable commands; optional familiar map
- **Owner system:** Command Readiness; Observable Canvas
- **Status:** planning proposal; no completion implied.

### F18 - UI scale and accessible states

- **Priority / stage:** P1 / 5
- **Current evidence / reason:** No dedicated accessibility qualification
- **User outcome:** Read and operate at chosen scale
- **Acceptance:** Enlarged UI; high contrast; reduced motion; screen-reader qualification
- **Owner system:** Observable Canvas
- **Status:** planning proposal; no completion implied.

### F19 - Professional color and print

- **Priority / stage:** P1 / 6
- **Current evidence / reason:** Desktop conversions policy-restricted; calibrated output untested
- **User outcome:** Deliver intentional web and print color
- **Acceptance:** ICC soft proof; gamut; depth/mode edits; calibrated output comparison
- **Owner system:** Capability-scoped automation; Honest Exchange
- **Status:** planning proposal; no completion implied.

### F20 - RAW development and camera coverage

- **Priority / stage:** P1 / 6
- **Current evidence / reason:** Large camera corpus not fetched
- **User outcome:** Develop supported camera files reliably
- **Acceptance:** Published camera matrix; corrections; local masks; continuation into layered editing
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F21 - Delivery Studio

- **Priority / stage:** P1 / 6
- **Current evidence / reason:** Eight small formats passed; several losses warned
- **User outcome:** Choose appropriate output and understand losses
- **Acceptance:** Job presets; preview; alpha/profile/size/font warnings; master retained
- **Owner system:** Honest Exchange
- **Status:** planning proposal; no completion implied.

### F22 - Format breadth and fidelity

- **Priority / stage:** P1 / 6
- **Current evidence / reason:** Supported-path evidence partial
- **User outcome:** Open and return client files appropriately
- **Acceptance:** PDF/SVG/layered TIFF/modern raster task matrix with explicit unsupported paths
- **Owner system:** Honest Exchange
- **Status:** planning proposal; no completion implied.

### F23 - Vector paths and artboard layout

- **Priority / stage:** P1 / 6
- **Current evidence / reason:** Representative path and prepared menus passed
- **User outcome:** Design reusable precise layouts
- **Acceptance:** Path edits; Convert Point; shape operations; guides; multi-size export
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F24 - Assets and missing dependencies

- **Priority / stage:** P1 / 6
- **Current evidence / reason:** Preset/import policy boundaries
- **User outcome:** Reuse materials and transfer projects
- **Acceptance:** Favorites/tags/licences; relink missing file; missing-font repair; project handoff
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F25 - Editable recipes and batch actions

- **Priority / stage:** P1 / 6
- **Current evidence / reason:** Basic rotation replay on fresh document passed
- **User outcome:** Reuse edits across different projects
- **Acceptance:** Relative targeting; step editing; preview; safe cancellation and rerun
- **Owner system:** Observable Canvas; Capability-scoped automation
- **Status:** planning proposal; no completion implied.

### F26 - Languages and input methods

- **Priority / stage:** P1 / 6
- **Current evidence / reason:** Latin fixture only
- **User outcome:** Create and navigate in the user's language
- **Acceptance:** Hindi/Arabic/Vietnamese/RTL and IME task set
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F27 - Reference Desk

- **Priority / stage:** P2 / 7
- **Current evidence / reason:** Proposed feature
- **User outcome:** Keep inspiration available beside the canvas
- **Acceptance:** Pin/sample/annotate references; exclude them from output
- **Owner system:** Creative Identity
- **Status:** planning proposal; no completion implied.

### F28 - Palette from Anything and harmony

- **Priority / stage:** P2 / 7
- **Current evidence / reason:** Proposed feature; swatch foundations exist
- **User outcome:** Establish and reuse a color story
- **Acceptance:** Extract/edit palette; apply to editable grade; compare result
- **Owner system:** Creative Identity
- **Status:** planning proposal; no completion implied.

### F29 - Print Lab

- **Priority / stage:** P2 / 7
- **Current evidence / reason:** Proposed feature; channels/filters foundations
- **User outcome:** Create distinctive ink-based graphics
- **Acceptance:** Riso/halftone recipe; ink controls; proof and delivery plates
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F30 - Material Library

- **Priority / stage:** P2 / 7
- **Current evidence / reason:** Proposed extension of texture/brush behavior
- **User outcome:** Give artwork deliberate physical texture
- **Acceptance:** Editable grain/material; brush interaction; saved project preservation
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F31 - Idea Branches and Variations

- **Priority / stage:** P2 / 7
- **Current evidence / reason:** Proposed extension of history
- **User outcome:** Explore without losing a good version
- **Acceptance:** Name branch; compare; keep/restore; preserve master
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F32 - Paint Replay and Process Edition

- **Priority / stage:** P2 / 7
- **Current evidence / reason:** Proposed extension of replay/history
- **User outcome:** Share how a piece was made
- **Acceptance:** Export reproducible replay and named milestone contact sheet
- **Owner system:** Observable Canvas; Creative Identity
- **Status:** planning proposal; no completion implied.

### F33 - Texture Workshop

- **Priority / stage:** P2 / 7
- **Current evidence / reason:** Proposed extension of pattern workflow
- **User outcome:** Create seamless reusable patterns
- **Acceptance:** Wrap preview; seam check; painting across boundaries; tile export
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F34 - Typography Art and Light Painting

- **Priority / stage:** P2 / 7
- **Current evidence / reason:** Proposed artistic workflows
- **User outcome:** Create expressive editable lettering and lighting
- **Acceptance:** Finished artwork built from path type and masked lighting adjustments
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F35 - Natural media and procedural tools

- **Priority / stage:** P2 / 7
- **Current evidence / reason:** Research proposal
- **User outcome:** Explore pigment and evolving surfaces
- **Acceptance:** Qualified watercolor/impasto/pigment/flow prototypes with artist review
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F36 - AI masks and generative editing

- **Priority / stage:** P2 / 7
- **Current evidence / reason:** No runtime evidence from audit
- **User outcome:** Explore assisted edits while retaining control
- **Acceptance:** Explicit intent; protected layers; separate results; disclosed processing; undo
- **Owner system:** Capability-scoped automation; Command Readiness
- **Status:** planning proposal; no completion implied.

### F37 - Motion and animation

- **Priority / stage:** P2 / 7
- **Current evidence / reason:** Some frame commands passed; end-to-end unqualified
- **User outcome:** Create and export short editable motion pieces
- **Acceptance:** Timeline; onion skin; loop; native reopen; GIF/video delivery
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F38 - Plugins and collaboration

- **Priority / stage:** P2 / 7
- **Current evidence / reason:** Ecosystem unqualified
- **User outcome:** Extend or share work with clear compatibility
- **Acceptance:** Published plugin capability matrix; permission/recovery qualification; collaboration conflict tasks
- **Owner system:** Professional/creative destination
- **Status:** planning proposal; no completion implied.

### F39 - Professional acceptance recordings

- **Priority / stage:** P1 / 0
- **Current evidence / reason:** 908 mixed-level checks retained
- **User outcome:** Review proof of complete user workflows
- **Acceptance:** 30-50 realistic scenarios with videos; outputs; boundaries; independent review
- **Owner system:** Living Audit
- **Status:** planning proposal; no completion implied.

### F40 - Select visual direction and qualify beginner tasks

- **Priority / stage:** P1 / 0
- **Current evidence / reason:** Owner PDF read; audience ambition and eight systems reconciled
- **User outcome:** Know the studio supports first-time success and expert control
- **Acceptance:** Three task storyboards tested with novices; choose visual direction and beta task set
- **Owner system:** Merged decisions
- **Status:** planning proposal; no completion implied.

### F41 - Outcome-led entry

- **Priority / stage:** P1 / 4
- **Current evidence / reason:** New owner ambition; proposed experience, not implemented
- **User outcome:** Create a poster/cutout/cleanup/grade/art print without knowing tool names
- **Acceptance:** First-use task entry; manual editing remains immediately available
- **Owner system:** Beginner success above the eight systems
- **Status:** planning proposal; no completion implied.

### F42 - Editable creative starting points

- **Priority / stage:** P1 / 4
- **Current evidence / reason:** New owner ambition; proposed experience, not implemented
- **User outcome:** Get a sophisticated starting result that fits actual content
- **Acceptance:** Three layouts/recipes preserve text, masks and adjustments on unfamiliar assets
- **Owner system:** Beginner success above the eight systems
- **Status:** planning proposal; no completion implied.

### F43 - Image-aware suggestions

- **Priority / stage:** P1 / 4
- **Current evidence / reason:** New owner ambition; proposed experience, not implemented
- **User outcome:** Receive useful crops, targets and palettes without losing control
- **Acceptance:** Low-confidence and wrong suggestions remain editable and dismissible
- **Owner system:** Beginner success above the eight systems
- **Status:** planning proposal; no completion implied.

### F44 - Progressive precision controls

- **Priority / stage:** P1 / 4
- **Current evidence / reason:** New owner ambition; proposed experience, not implemented
- **User outcome:** Begin with a few meaningful choices and grow into exact controls
- **Acceptance:** Same document across Create/Explore/Precise; no destructive mode conversion
- **Owner system:** Beginner success above the eight systems
- **Status:** planning proposal; no completion implied.

### F45 - Contextual learning and practice

- **Priority / stage:** P1 / 4
- **Current evidence / reason:** New owner ambition; proposed experience, not implemented
- **User outcome:** Understand a useful workflow within one or two days
- **Acceptance:** Dismissible explanations; new-content independent day-two task test
- **Owner system:** Beginner success above the eight systems
- **Status:** planning proposal; no completion implied.

### F46 - Finishing and quality guidance

- **Priority / stage:** P1 / 4
- **Current evidence / reason:** New owner ambition; proposed experience, not implemented
- **User outcome:** Catch legibility, edges, crop, resolution and delivery problems
- **Acceptance:** Inspect concrete issues; choose corrections; preserve creative choice
- **Owner system:** Beginner success above the eight systems
- **Status:** planning proposal; no completion implied.

### F47 - Novice and expert qualification

- **Priority / stage:** P1 / 0
- **Current evidence / reason:** New owner ambition; proposed experience, not implemented
- **User outcome:** See proof of ease, output quality and retained expert control
- **Acceptance:** Predeclared cohort/tasks/rubric; completion/help/time and blind output review
- **Owner system:** Beginner success above the eight systems
- **Status:** planning proposal; no completion implied.

### F48 - Safe visible assistance

- **Priority / stage:** P1 / 2
- **Current evidence / reason:** New owner ambition; proposed experience, not implemented
- **User outcome:** Get help without hidden changes to targets or masters
- **Acceptance:** Preview intended changes; protected layers; undo; explicit destructive/external actions
- **Owner system:** Beginner success above the eight systems
- **Status:** planning proposal; no completion implied.

### F49 - Resource-aware editing assistance

- **Priority / stage:** P1 / 2
- **Current evidence / reason:** 86 mixed policy refusals; true resource classification not complete
- **User outcome:** Use approved document edits without unintended external access
- **Acceptance:** Classify each command resource use; deny ungranted external access; qualify migration
- **Owner system:** Capability-scoped automation
- **Status:** planning proposal; no completion implied.

### F50 - Gesture feedback and announcements

- **Priority / stage:** P1 / 2
- **Current evidence / reason:** All 65 representative results observed; unified journal unqualified
- **User outcome:** Know what changed and learn from clear history
- **Acceptance:** Meaningful events matched with state/pixels; accessible controls and announcements
- **Owner system:** Observable Canvas
- **Status:** planning proposal; no completion implied.

### F51 - Pre-export fidelity and alpha interpretation

- **Priority / stage:** P0 / 1
- **Current evidence / reason:** Post-export warnings retained; PNG/TGA models differ correctly
- **User outcome:** Understand loss and alpha meaning before choosing a delivery format
- **Acceptance:** Preflight specific features; reversible alpha preview; retain master and final warnings
- **Owner system:** Honest Exchange
- **Status:** planning proposal; no completion implied.


## Upstream integration review ? 14 October 2026

[Reviewed integration and next-generation strategy](upstream-and-nextgen-strategy-review-2026-10-14.md) recommends reusing verified upstream editing infrastructure while preserving the owner's beginner-first Atelier direction. Upstream at `ed7df56` is 750 commits beyond our base; no integration has occurred. Preserve local cache/mip/histogram patches and qualify a separate candidate before promotion. Typed command metadata, document-scoped transactions and a small first recipe are proposed foundations; nightly shipping-branch rebases, full recipe-to-Actions conversion and complete automated audit claims are not adopted contracts. Existing acceptance budgets and backlog statuses remain unchanged.
