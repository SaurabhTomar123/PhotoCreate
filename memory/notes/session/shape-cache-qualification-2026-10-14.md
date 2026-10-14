---
schema: 1
title: "Shape-cache optimization qualified with recordings"
kind: "session"
status: "verified"
date: "2026-10-14"
evidence: ["docs/implementation-progress-2026-10-13.md", "docs/system-level-revamp-spec-2026-10-13.md", "docs/gaps.md", "docs/target-app-parity.md"]
---

Implemented bounded shape split reuse and Purge All integration after reproducing the old 33-shape/32-entry cliff. Native/corpus/UI, compositor, pixel oracle, adversarial input, lint, formatting, layers, wasm and desktop checks passed; ignored conditions remain identified. Quiet paired medians: opacity 398.06 -> 25.48 ms, pixel move 401.95 -> 31.35 ms. No global readiness score or cross-device guarantee changed.

Recorded before/after 12 MP workflows with 37 editable layers, native reopen and PNG export. Decoded output pixels match exactly. After also validates cache purge. Retained disk-full builds and a screenshot-timeout attempt; generated compiler caches/symbols recovered storage. A temporary visibility lease enabled the retry and was cleared when the audit app closed. Its cause remains unknown.

Current system specification, backlog, gap/parity evidence, execution log and vault snapshots carry these results. The 16 ms target, larger workloads, native crashes and beginner-first UI/creation work remain open.
