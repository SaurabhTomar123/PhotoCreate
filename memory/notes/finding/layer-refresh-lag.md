---
schema: 1
title: "Layer refresh improved; interaction budgets remain open"
kind: "finding"
status: "verified"
date: "2026-10-14"
evidence: ["docs/implementation-progress-2026-10-13.md"]
---

The reproduced shape-cache working-set cliff is fixed locally. Quiet paired 12 MP / 174-layer release opacity median improved 398.06 -> 25.48 ms; pixel-move commit 401.95 -> 31.35 ms; text visibility 421.71 -> 25.63 ms. These replace the earlier unknown-cause status for that contribution, not the historical measurements kept in the execution log.

Histogram worker accumulation was separately bounded; its earlier paired run had no consistent overall speedup. The shape-cache change now provides measured improvement. Stage tracing showed render/submission dominating a representative slow baseline refresh, with repeated tile uploads, no effect rebuilds/evictions and a short final GPU wait.

Several operations still exceed 16 ms, and demanding text moves remain slower. Larger sets, different devices, physical input latency and the original parallel/native crash conditions are not qualified. See [shape-cache finding](shape-cache-working-set.md) and [execution record](../../reference/implementation-progress-2026-10-13.md).
