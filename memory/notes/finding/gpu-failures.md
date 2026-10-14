---
schema: 1
title: "Reproduced GPU failure and remaining hypotheses"
kind: "finding"
status: "verified"
date: "2026-10-13"
evidence: ["docs/live-feature-test-results-2026-10-11.md", "dist/qa/validation-gpu-isolated-2026-10-11/gpu-mips.log"]
---

The U16 partial-mip assertion reproduced on AMD Radeon Vulkan. Recorded RGBA: [5.9604645e-8, 0, 0, 0]. The small value is red; alpha is zero. Root cause is not established.

Three native GPU integration targets crashed in the workspace run; serial reruns passed twelve tests. Serial passing does not fix the original failures. Driver/device concurrency and scratch-target remedies remain hypotheses. The owner's PDF reports DX12 success, but matching retained logs were not found during review.

Preserve failing evidence and qualify any workaround before claiming a repair. See [baseline](recorded-baseline.md).


Current-build follow-up: [validated bounded mitigation](gpu-preview-fix.md). The failure above is retained baseline evidence; it does not claim the new build still fails that matrix. General native-crash root cause is unresolved.
