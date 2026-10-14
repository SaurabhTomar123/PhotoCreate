---
schema: 1
title: "GPU diagnosis and bounded redraw candidate"
kind: "finding"
status: "superseded"
date: "2026-10-13"
evidence: ["docs/implementation-progress-2026-10-13.md"]
---

The fresh baseline failed. Enriched diagnostics show the original direct-path failure at U16 1791x1083 mip5 pixel16,16, and scratch-path failure in the same session at U8 mip5 pixel16,16. Scratch-only policy is therefore not yet a validated fix.

A candidate change redraws and clears levels whose dimensions are both <=64; larger levels retain partial updates. It is under validation, not a completed fix. Root cause and the three native GPU test crashes remain unresolved. See the current execution record.


The candidate is now validated locally; see [current finding](gpu-preview-fix.md). Diagnostic failures remain historical evidence.
