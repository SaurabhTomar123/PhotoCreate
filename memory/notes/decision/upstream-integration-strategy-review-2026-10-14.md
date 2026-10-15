---
schema: 1
title: "Proposed upstream integration with a protected experience layer"
kind: "decision"
status: "proposed"
date: "2026-10-14"
evidence: ["docs/upstream-and-nextgen-strategy-review-2026-10-14.md", "docs/implementation-progress-2026-10-13.md", "docs/system-level-revamp-spec-2026-10-13.md"]
---

Fetched upstream ed7df56: 750 commits and 870 changed files from local base d45b371. A per-file text preview finds conflicts in the shape cache and two historical/current assessment docs; a textually clean Purge merge calls the shape cache twice. No merge, rebase, commit, product edit or integration qualification occurred.

The preceding paragraph records the review-time state on 14 October. The owner subsequently authorized publication and merge; the protected baseline and pinned integration were executed and qualified on 14–15 October. See [[upstream-integration-2026-10-15]] and `docs/upstream-integration-results-2026-10-14.md`. Broader strategy proposals remain proposals; that authorization does not authorize upstream maintainer messages or cloud/AI services.

Recommend a restorable local snapshot and separate pinned integration candidate, preserving our 128-entry/128 MiB cache policy, purge-generation guard, mip mitigation, histogram coalescing, QA evidence and beginner-first direction. Prioritize GPU harness serialization, uniform preflight/error containment, missing-sidecar recovery with its cleanup dependency, disabled-command metadata, Navigator and Export As improvements. Re-run acceptance and performance before promoting a candidate.

The owner supplied a next-generation strategy advocating upstream infrastructure and an additive guided experience. Review supports that direction with amendments: avoid automatic shipping-branch rebases; define document-only transactions and authoritative capability checks; export only the representable Actions subset; resolve current L6 dependency restrictions; separate future audit targets from measured evidence; build one guided recipe before complete metadata or AI/ML. Publication, external accounts, image/model network calls and nightly automation were not authorized by the review request.
