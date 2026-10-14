---
schema: 1
title: "Bounded GPU preview mitigation validated"
kind: "finding"
status: "verified"
date: "2026-10-13"
evidence: ["docs/implementation-progress-2026-10-13.md"]
---

The local renderer now clears and redraws complete mip levels at most 64x64; larger levels keep bounded partial updates. The original opaque-alpha failure reproduced before the change. Scratch-only rendering also failed in diagnosis, so no vendor-only scratch workaround was assumed.

Expanded tests cover 54 base cases and 162 center/edge updates across 8/16/32-bit inputs, three alpha backgrounds, three sizes and both rendering paths. Partial outputs match full rebuilds at all mip levels on AMD Vulkan and DX12. The complete serial UI suite passed 2,129 tests, with ten ignored. Lint, formatting, layers and 24 wasm package/feature checks passed.

The rebuilt 16-bit live workflow was recorded successfully in an isolated retry. Root cause, broader hardware coverage and F02 native crashes remain open. This is a local mitigation, not professional-readiness certification. See [current execution record](../../reference/implementation-progress-2026-10-13.md).
