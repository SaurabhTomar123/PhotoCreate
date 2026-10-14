# Upstream integration and next-generation strategy review

14 October 2026. **Recommendation:** adopt upstream's editing depth and reliability work through an isolated, tested integration branch; retain our beginner-first product direction and locally verified fixes. The pasted strategy is a useful architectural proposal, but several contracts and operational claims need revision before implementation.

This is a review, not authorization to publish issues/PRs, fork an account repository, send images to an AI provider, or install nightly automation. No merge, rebase, commit or editor code change occurred in this review. Fetch updated Git references only. The Claude URL returned a shell; its content endpoint required authentication. The owner then pasted the strategy, which is the material reviewed here.

## Verified checkout comparison

Local base: `d45b3718cef1c92a7a19ae9407383ab58dffb9c9`. Fetched upstream: `ed7df56a2455375240959bae6e5273a71d858d84`. **750 commits / 870 changed files**, including dependency/lockfile, rendering, export, tools, typography, tests and documentation changes. This snapshot establishes a large integration, not a future daily commit rate.

The review generated per-file three-way text previews in `dist/qa/upstream-review-2026-10-14`; it did not overwrite working files. `compatibility.json` records the results. Among ten locally modified tracked files, six also changed upstream. Text conflicts occur in `shape_split.rs` (three blocks), `docs/gaps.md` and `docs/target-app-parity.md` (one each). `AGENTS.md`, `gpu_canvas.rs` and `edit_menu_cmds.rs` merge textually; **that does not prove compatibility**.

The apparently clean `edit_menu_cmds.rs` preview calls `shape_split::purge_cache()` twice, under different labels. Reconcile to one call and one report entry. A concurrent admission between those calls could make the duplication observable. Preserve our `cache_bytes()` readiness check and the purge-generation guard. Do not trust clean Git merges as behavioral tests.

Upstream did not change `tone.rs`, `gpu_canvas_mip_tests.rs` or `examples/layout_bench.rs` relative to this base. Its GPU canvas changes extend texture budgets, deferred refresh and memory release; our mip mitigation still needs requalification with those paths. Unchanged mip code is evidence of a retained local patch, not proof that no other upstream change could affect the symptom.

## What to bring in

| Order | Upstream work | Benefit and qualification needed |
|---|---|---|
| First | [`c18ee8c`](https://github.com/storytold/photocraft/commit/c18ee8c88bb2470b951c11e8cc7147d36d345b2f): per-process GPU harness lock | Targets Windows WARP parallel-test crashes. Strong match to our failed targets, but upstream's driver diagnosis does not establish the cause of our original crashes or fix production GPU behavior. Repeat the previously failing parallel tests. |
| First | [`95dbb01`](https://github.com/storytold/photocraft/commit/95dbb01ad9ef770bc9a83c1fd8d2b35e913316fb): compositor uniform-limit preflight | Relevant to our original large-workload uniform-buffer validation failure. Rerun that fixture, not just the new unit tests. |
| First | [`2571423`](https://github.com/storytold/photocraft/commit/2571423bb34b7dddaa826c3f3494d53e26ced60c): contain unwatched GPU work errors | Improve rendering failure containment; verify document retention and fallback locally. |
| First | `c20b81b` plus [`ed7df56`](https://github.com/storytold/photocraft/commit/ed7df56a2455375240959bae6e5273a71d858d84): autosave cleanup and missing-sidecar recovery | Complements our completed-autosave kill test with a real interrupted-publication case. The last patch depends on the earlier orphan-cleanup behavior: importing only the latest diff is insufficient. |
| Next | [`3dd5fc1`](https://github.com/storytold/photocraft/commit/3dd5fc1cdc631efcc213d849b86829602895b7ea): `disabledReason` and `needsDocument` | Reuse for guidance instead of duplicating a command catalogue. This is automation-listing metadata, not a completed guided menu experience. |
| Next | [`cdfec72`](https://github.com/storytold/photocraft/commit/cdfec72f7136d294cb1ba8a25f57a0c6fb1440b7): Navigator uses GPU canvas | Avoid CPU recomposition on common edits. Verify color transforms, fallbacks, mips and paired release timings. |
| Next | [`2e242bd`](https://github.com/storytold/photocraft/commit/2e242bde67c202e4cd16bf3d6f88088b521ab423): large layered Export As freeze | Improves a professional delivery path. Validate preview cancellation, UI responsiveness and saved outputs. |
| Later | Background CPU redraw, raster/selection/brush optimizations, type-on-path, Select and Mask improvements, `.atn` support | Adopt useful engine depth, then expose it through our outcome-led UI. Each affected workflow gets its own acceptance check; commit titles alone do not close our backlog. |

Prefer one pinned upstream integration candidate over hundreds of permanent ad hoc cherry-picks. These priorities determine review and validation order. Small isolated backports can be useful while the larger integration is pending.

## Preserve our local work

Upstream's [`752f611`](https://github.com/storytold/photocraft/commit/752f6112647f3f6b4eaab65de0473747d351bba4) adds a **256 MiB / 32-entry** split-parts cache and purge support. Our qualified implementation uses **128 MiB / 128 entries**, conservative accounting including pinned input surfaces/default bytes, isolated regressions, and a purge-generation guard. Reverting to 32 entries would discard the policy that removed the measured 33-shape cache cliff.

The proposal to “keep upstream's byte budget” therefore needs a deliberate decision. Preserve our currently qualified 128 MiB policy initially; do not silently raise it to 256 MiB or relax accounting. Reconcile the API and upstream intent, then benchmark any policy change separately.

Also preserve the bounded U16 mip mitigation and readback matrix, histogram worker coalescing, geometry/pixel oracle tests, diagnostics, QA scripts, original recordings, system specification and local memory. Historical results stay tied to the old executable hashes; they do not automatically qualify an integrated build.

## Strategy: retain the direction, amend these contracts

1. **Safe integration, not nightly shipping-branch rewrites.** Keep a last-qualified product branch/build. A scheduled job may fetch upstream and create a disposable integration candidate, then report conflicts and tests. Promote only a qualified candidate. Rebase is reasonable for private short-lived patch branches, but is not the default for a shared shipping branch. Upstream squash merges and conflict resolutions also mean local copies do not always disappear automatically. Publishing issues/PRs and enabling CI require their own explicit authorization.

2. **Metadata should support guidance without becoming permission.** Start with one recipe and its commands, structured inputs and typed prerequisites, plus an explicit unknown-metadata fallback. Our latest local catalogue has **871 commands**, not about 700; requiring full rich metadata immediately would block the first useful workflow. The 73 prepared retries are examples, not a complete refusal taxonomy. Runtime errors such as disk failure, cancellation or malformed files are not preconditions. Keep `enabled`, parameter validation and existing `Session::authorize` checks authoritative, including nested actions. A capability declaration describes an operation; it does not grant filesystem, network or model access.

3. **Transactions need a bounded scope.** One undo step is appropriate for supported document edits. It is not rollback of file writes, exports, network calls, preference changes or arbitrary multi-document jobs. Specify affected documents, cancellation/failure rollback, asynchronous completion, memory limits, redo determinism and journal grouping. Start with a single-document recipe without external side effects. Re-check prerequisites at execution: preview state can become stale.

4. **Planner suggestions must respect artistic intent.** A bounded breadth-first search is a reasonable prototype, but “satisfies a predicate” does not mean a change is desirable. Converting color modes, flattening, rasterizing or creating masks changes the artwork. Prefer duplicates/non-destructive paths, disclose changes, and require user choice for destructive repairs. Define depth, candidate/CPU limits and unsupported cases; a three-step cap is not a completeness guarantee.

5. **Actions interoperability is a subset.** PhotoCraft recipes can run ordinary engine commands, but slots, branching, seeded variations, model calls and planner logic are not automatically representable as Photoshop `.atn` files. Export the supported concrete subset and report unsupported steps. `.atn` import/export support does not prove Photoshop accepts every recipe.

6. **The additive crate layout needs a real dependency seam.** Current upstream layering allows only explicitly ordered same-layer dependencies; there is no L6 ordering for the proposed experience/AI/shell crates. Registering every new crate as L6 does not make `ui-egui -> experience` legal. Choose app-level composition with a public shell extension contract, or propose a precise permitted ordering and test it. Large layout/state changes will still touch the shell; “additive” reduces conflicts but cannot guarantee none. The 300-line budget is a review signal, not a correctness gate.

7. **Journal, accessibility and AI context have separate contracts.** Use bounded, versioned/redacted events rather than serializing an unbounded gesture stream into `state.rs`. AccessKit announcements need deliberate semantic messages; not every event should become an announcement. Co-pilot context must exclude private paths, text, images and credentials unless the user explicitly authorizes that data. Model provider choice remains open; the strategy's Claude client is a proposal, not an established product requirement.

8. **ML is a later optional quality lane.** Verify model-weight/runtime licences and redistribution/download conditions per model; “ONNX” is not a licence. Native FFI, packaging and inference budgets need review. A native feature gate preserves a build, not feature parity on the web. The referenced owner issue #41 is reported in the proposal and was not independently verified here. A generated raster on a new layer is editable as pixels; it does not make every generated choice parametrically reversible.

9. **Trust is a release gate throughout.** Keep recovery, fidelity and rendering checks in every phase; do not reserve broad professional trust for the final phase. GPU canaries/readback need their own measured overhead and scope. Preserve existing codec/export warning behavior when adding a pre-save fidelity analysis; a capability matrix alone cannot identify every document-specific loss.

10. **Audit targets are proposals, not current guarantees.** The 908 checks are mixed activation/smoke/workflow evidence. They do not yet assert a unified event journal, per-frame panel coverage, end-to-end release latency or mid-write recovery. Current clips are four fps, unsuitable for measuring 20 ms latency. Cache results of 25–31 ms are selected **medians**, not p95. Keep the existing 16 ms goal unless an explicit budget revision distinguishes rendering from end-to-end interaction. Measure guided success on named tasks with a denominator, sample sizes and excluded unsupported tasks. “100% recovery” can describe a specified test matrix, not all real-world failures. Track useful accepted upstream work rather than incentivizing PR counts.

## Practical next sequence

1. Create a restorable snapshot of tracked and untracked local code/docs/memory; retain ignored recordings separately. Do not rely on a patch alone to preserve untracked work. Keep the current working checkout available.
2. Create a separate integration checkout pinned to the verified upstream hash. Preserve our product direction, then port the three generic local fixes and their tests. Resolve shape-cache policy, duplicate purge and historical/current documentation explicitly.
3. Validate native parallel GPU targets, Vulkan/DX12 readbacks, completed and missing-sidecar recovery, export behavior, corpus, layers, lint and wasm. Record a fresh release comparison using the same fixture and hardware; do not reuse old scores as new qualification. Plan storage before rebuilding: this workstation has already hit disk-full twice.
4. Adopt a small metadata/transaction contract and ship **one finished guided recipe** with the existing engine and no AI dependency. “Poster from photo + editable title + native master/export” is a concrete candidate. Test it with beginners before scaling the studios or adding model infrastructure.
5. Prepare generic patches for review when requested. Keep the artistic Atelier direction, guided creation and progressive precision as our product layer. Sync local memory with each actual implementation result.

The integration has not been built or tested. The text preview is evidence of likely merge work, not assurance that pulling is safe. The existing checkout and all current implementation evidence remain intact.
