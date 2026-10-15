---
schema: 1
title: "Pinned upstream merge and recorded qualification"
kind: "session"
status: "verified"
date: "2026-10-15"
evidence: ["docs/upstream-integration-results-2026-10-14.md", "docs/implementation-progress-2026-10-13.md", "docs/revamp-feature-backlog-2026-10-13.csv"]
---

Owner authorized publication to SaurabhTomar123/PhotoCreate, then upstream update and merge. Baseline 918d422f was pushed to main and baseline/revamp-2026-10-14 before integration. Merge ee75a490 imports upstream ed7df56, retaining the 128-entry / conservative 128 MiB cache, generation guard, single purge, U16 mitigation and histogram coalescing. The beginner-first product direction is preserved; its guided experience remains planned.

After correcting an autosave-test discovery race and missing GPU guards, the full native suite passed 8,396 tests with 68 ignored and no failures/crashes. Corpus-enabled suite passed 3,532 with 27 ignored. Documentation tests, native strict workspace clippy, 24 wasm checks, layers, scorecard, pinned corpus verification, desktop build and explicit panic hunt passed. Wasm retains a nonfatal upstream dead-code warning. Mip matrix passed on AMD Vulkan and DX12, not all adapters.

Release comparison is mixed, with latency still open. Corrected benchmark explicitly selects Layer because upstream's product default changed to Group; it also asserts the selected headline. The initial mismatched run remains retained. The layout recording passed bounded assertions but showed an unplanned moved tile. Two live brush captures failed single-undo restoration after extra history entries; another timed out before edits. Root cause is unproven. Passing mip tests do not close the live interaction issue. See the execution report for final recovery retry, performance and publication details.

No upstream maintainer issue/PR, external AI call, cloud Obsidian sync or automatic shipping-branch rebase was performed. This vault is local Markdown reference data; no plugins or executable memory were added.
