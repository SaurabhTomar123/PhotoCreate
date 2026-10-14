---
schema: 1
title: "Shape cache working-set investigation"
kind: "finding"
status: "verified"
date: "2026-10-14"
evidence: ["docs/implementation-progress-2026-10-13.md", "crates/compose/src/shape_split.rs", "crates/ui-egui/tests/support/layout_doc.rs"]
---

The old 32-entry split cache could not retain the benchmark's 33 unchanged stroked shapes. An isolated regression reproduced tile reallocation on the next traversal. The implemented cache now bounds retention by 128 entries and 128 MiB of conservatively counted pixel storage, including source pixels pinned to protect address-based identity. Oversized results remain usable without retention. Purge All releases entries and a generation guard blocks stale in-flight admission.

Qualified 2026-10-14: combined native/corpus/UI 4,904 passed, zero failed, 34 ignored; compositor 204 passed, one ignored; geometry/stroke/canvas pixel oracle at U8/U16/F32 and ignored adversarial panic-hunt passed. Lint, formatting, layers, all 24 wasm checks and the normal HEIF desktop rebuild passed. Failed storage attempts are retained separately.

Quiet paired release workload: 4000x3000, 174 layers, 60 text layers, nine repetitions, same AMD integrated Vulkan adapter/driver. Opacity median 398.06 -> 25.48 ms; pixel-move commit 401.95 -> 31.35 ms; text visibility 421.71 -> 25.63 ms. One sequential pair; not a physical input-latency or cross-device guarantee. The 16 ms goal, larger working sets, demanding text moves and earlier parallel native crashes remain open.

Both recorded 12 MP colour-study workflows passed; every decoded exported PNG pixel is identical. The after case verifies Purge All preserves the composite. An initial after recording timed out; an app-only temporary visibility lease passed on retry and was cleared at finish. The screenshot timeout cause is not established. See the execution record and its review-page links for videos, native outputs, failures and limits.
