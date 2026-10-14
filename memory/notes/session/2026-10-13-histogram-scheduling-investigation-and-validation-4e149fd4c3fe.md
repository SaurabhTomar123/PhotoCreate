---
schema: 1
title: "Histogram scheduling investigation and validation"
kind: "session"
status: "verified"
date: "2026-10-13"
evidence: ["docs/implementation-progress-2026-10-13.md"]
---

The Histogram panel replaced a pending job receiver whenever the document revision changed. Its running worker is not cancelled by receiver replacement, allowing repeated edits to accumulate background thumbnail renders. A candidate change keeps one worker pending, tags delivered cached data with its original revision, and schedules the latest state after completion. Native test, lint, WebAssembly, release comparison and live capture are being checked; F06 is still open. The initial regression attempt failed in the egui test harness because texture deltas were dropped; its setup was corrected and the failed log retained.

Completed: corrected tone regression five passed; UI library 2,036 passed, ten ignored; final clippy, formatting, layers, 24 wasm checks and desktop build passed. Two healthy live clips (14.5 and 13 seconds) and native 150-layer outputs are available through the execution record. Quiet paired release measurements retain hundreds-of-milliseconds canvas refresh lag; F06 and native crash qualification remain open. Failed harness attempts are retained and identified in the report.
