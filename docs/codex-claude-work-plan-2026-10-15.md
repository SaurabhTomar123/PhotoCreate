# Codex and Claude delivery plan

15 October 2026. Owner requested approximately equal work between Codex and Claude, with upstream reuse. This is an agreed allocation proposal, not evidence that Claude has accepted or started. Balance by estimated effort and completed outcomes, not lines or commit counts. Rebalance at each completed batch.

## Current checkpoint and fresh upstream review

PhotoCreate main is `001e8eec9182219271e3dc3c214e66e0f0cb296d`, containing the qualified upstream `ed7df56` merge. Baseline `918d422f` remains on `baseline/revamp-2026-10-14`. See [qualification](upstream-integration-results-2026-10-14.md) and [records](../records/README.md).

Fetched both remotes on 15 October. PhotoCreate had no additional remote changes. Upstream main advanced to `df055f3dcb0bb0312af97548ee6c6f9628f21dd7`: **176 commits, 370 changed files, 28,147 insertions and 2,716 deletions** since ed7df56. Tag v0.9.0 was fetched; a tag is not local qualification. No new upstream source has been merged or tested in this review.

Object-only merge preview (`git merge-tree --write-tree --name-only main origin/main`) found **one text-conflicted file**, `apps/photocraft/src/services.rs`. Upstream `7250e6e2` independently makes the autosave retry test wait for the requested revision, matching our correction. Reconcile both comments and assertions rather than dropping either wholesale. The preview does not change the working tree and cannot establish runtime compatibility.

| Upstream work | Reuse decision / qualification |
|---|---|
| `47cf5af9`, `dbfe8ba4`: effect-cache pins and history memory accounting | Import in candidate; verify retained bytes and existing shape-cache generation/128-entry policy. Shape-split source itself is unchanged in this upstream range. |
| `84286453`: scratch mips default to Intel DX12 only; environment override | Import only with local U16 mitigation preserved and repeat AMD Vulkan/DX12 partial/full mip matrix plus app-default routing checks. Both paths passing previously does not prove the newly merged routing. |
| `90b3f9e8`: background redraw for damage above GPU budget | Measure large-edit responsiveness and eventual full-quality redraw; do not infer that it fixes our opacity timing or extra brush history. |
| `3ebc42a2`, `ad96df56`: Export As sizing/presets/profiles and PDF writing | Reuse instead of building duplicate export controls; verify size, color, transparency and actual warnings. PDF support is not evidence of editable Photoshop acceptance. |
| `c7d9ade9`, `cb8ed762`, `5cb5ab52`: subject selection, content-aware fill/crop | Use as foundations; review difficult boundaries and reversibility before calling them professional quality or ML. |
| `38b96f27`, `602344ba`, `37f57f2e`: selected-layer transform bounds, filter drag preview, per-document layer scroll | Reuse and exercise in named workflows. |
| `7b08b565`, `56c5b355`: layer listing and command search keywords | Build guided targeting/search on these public command paths; avoid a duplicate layer catalogue. |
| `df055f3d`: CI fixes and compressed wasm packaging | Review new app/layer registration and packaging gates; changes to CI are not proof CI passes on our fork. |

## Equal ownership of the first delivery cycle

Four substantial outcomes per owner. The upstream batch comes first; feature branches then share its exact qualified commit. Claude can prepare the workflow specification and isolated prototype against the current base while Codex qualifies upstream, but must reconcile API assumptions before integration.

| Owner | Work packet | Deliverable and completion evidence |
|---|---|---|
| Codex C1 | Upstream intake and integration | Pinned candidate, semantic review, autosave conflict resolved, local fixes preserved, appropriate native/corpus/clippy/layers/wasm/build gates, recorded changed workflows. Promote only passing reviewed candidate; retain checkpoint. |
| Codex C2 | Live input/capture reliability | Reproduce extra Brush/Move history separately from capture; trace press/move/release and frame boundaries; distinguish native events from injected events. One synthetic stroke, preview navigation, one undo/redo, exact document samples; retained failures and passing regression. Root cause must be demonstrated. |
| Codex C3 | Interaction performance | Profile opacity, visibility, selection and group movement on fixed 12 MP and 24–36 MP workloads. Preserve comparable Layer/Group targets, adapters and build settings. Fix measured bottlenecks and report distributions, output correctness and remaining budget misses. |
| Codex C4 | Integration and trust qualification | Review Claude's command use, cancellation and history; verify native save/reopen, recovery and export, record finished beginner task; publish one combined evidence package and consolidate canonical backlog/memory. |
| Claude L1 | First outcome and interaction specification | Specify “Make an editorial poster”: user-supplied image, title, palette, composition. Define three art directions, plain-language controls, empty/error states, keyboard path and progressive depth. No generated visual claim without an actual preview. |
| Claude L2 | Bounded command readiness | Typed prerequisites/inputs/effects for only commands used by the recipe. Check against registry and real enabled behavior; explain missing image/text/target and offer explicit preparation. Unknown commands remain unsupported by guidance. No invented complete metadata or security guarantees. |
| Claude L3 | Editable poster recipe and variations | Deterministic versioned recipe with adjustable parameters and seeded layout/color variations, ordinary editable layers/text/adjustments, preview and cancellation. Reuse normal dispatch. Add document-only transaction support only if required and agreed interface first; failed execution must not leave a half-applied document. No filesystem/network step inside document rollback. |
| Claude L4 | Guided tray and creation surface | Native egui entry/tray in an isolated module, image/title/style/variation controls, Apply/Cancel and ability to reveal manual controls. Existing theme tokens, readable focus, canvas kept visible, final state adjustable. Screenshots, meaningful tests and recorded end-to-end recipe. |

L2–L4 are staged: prove one recipe manually through normal commands before generalizing metadata or a planner. Do not block the first result on all-command schemas, AI or local ML. If a real transaction needs substantial engine work, trade an equivalent later task between owners; do not quietly double Claude's workload.

## Branches, files and handoff contract

- PhotoCreate is the shared delivery repository. Fetch upstream from storytold; push branches to PhotoCreate. `main` contains accepted batches. No direct experiments or automatic rebases of main.
- Codex owns `integration/upstream-2026-10-15`, then `codex/input-reliability` and `codex/interaction-performance`. Claude uses `claude/editorial-poster`, cut from the agreed qualified base. Each agent uses a separate checkout/worktree, never the same active branch or index.
- Codex initially owns existing `canvas.rs`, `control.rs`, `paint_mouse*`, `gpu_canvas*`, `tone.rs`, compose hot paths and live QA scripts. Claude reads these but requests a small integration patch when needed.
- Claude puts new recipe/readiness engine code in new modules and new guided egui controls in a new module. No extra crate until layering/public interfaces justify it. Shared registration in engine `lib.rs`/`commands.rs`, UI `lib.rs`/`state.rs`/`menus.rs`, Cargo manifests/lock and xtask layers belongs to the integrator (Codex). Claude supplies the exact small patch or agrees a temporary ownership window first. Do not have two agents edit those files together.
- Claude records its results in `docs/claude-editorial-poster-progress.md`; Codex records its lane separately. Codex consolidates `docs/implementation-progress-2026-10-13.md`, the CSV backlog, source snapshots and `memory/INDEX.md` at integration. This is documentation ownership, not permission to omit Claude's findings.
- Before each batch, fetch PhotoCreate and upstream, compare changes in owned areas, and pin the SHA. Do not continually chase a moving upstream while a batch is being tested. Review another upstream batch at the next accepted checkpoint; urgent security/data-loss fixes can interrupt this cadence.
- Each handoff supplies base/head SHAs, changed files, exact commands and results, screenshots/video, known failures and dependencies. Cross-review the other owner's work before merging. Claude's branch is not assumed to exist until its refs are fetched and verified.
- Upstream generic fixes are reused first. An upstream feature counts as imported, then qualified, before it counts as complete in our backlog. Do not replace local fixes just because a merge is textually clean.
- Use isolated Cargo target directories where practical, but inspect free space first; this machine previously ran out. Avoid simultaneous full Rust builds or GPU benchmarks/captures on this one adapter. One shared hardware-test queue; one final full integration run after targeted lane checks. Keep target/corpus/executables/private profiles out of Git.

## Sequence and decision gates

1. **Now:** freeze the fetched upstream SHA and share this plan with Claude. Codex qualifies that upstream candidate; Claude delivers L1 and a command/API map without changing shared files.
2. **Next:** both work from the accepted candidate. Codex starts the input reproduction and profiling; Claude builds a thin vertical poster workflow, then readiness and variations. Agree required transaction interface before both depend on it.
3. **Combine:** cross-review and merge one lane at a time into a temporary candidate. Run targeted regressions, then required combined gates. Record poster creation, revision, one-step undo/redo where transactional, editable save/reopen and export. Failed captures remain failures.
4. **User validation:** three first-time users try the same poster task. Target a good first result within ten minutes, with adjustable title/image/colors and no unexplained dead end. This is a proposed test, not recruited participants or a proven learning-time claim. Use their stuck points to select the next studio.
5. **Then:** selection/background or retouch workflow, broader fidelity/recovery and the full Atelier shell. Defer all-command planning, AI co-pilot and ML downloads until the first workflow and permission/fidelity contracts are sound.

## Message to paste to Claude

> We are splitting PhotoCraft development approximately 50/50 by effort. Repository: https://github.com/SaurabhTomar123/PhotoCreate. Read AGENTS.md, docs/system-level-revamp-spec-2026-10-13.md, docs/upstream-integration-results-2026-10-14.md and docs/codex-claude-work-plan-2026-10-15.md. Codex owns upstream integration, live input/capture reliability, performance and combined QA. You own L1–L4: one beginner-first editable editorial-poster recipe, bounded readiness metadata and a native egui guided tray. Start with the workflow specification and exact existing command/API map; coordinate the qualified base SHA before coding shared dependencies. Use a separate checkout and claude/editorial-poster branch. Keep new work in isolated modules; give Codex small registration patches for shared files. Preserve native Rust/egui, editable layers and the owner's distinct beginner-first direction. No cloud AI/ML calls, personal-image upload or universal Photoshop-parity claims. Report base/head SHAs, files, tests, recordings and known gaps in docs/claude-editorial-poster-progress.md. Push your branch to PhotoCreate when ready for review; do not merge main or rebase other owners' work. If you cannot access the repo, say so rather than assuming its contents.

Codex cannot directly operate a separate Claude conversation here. The owner must deliver the handoff or provide an existing connected collaboration channel; no message has been sent to Claude by this plan.
