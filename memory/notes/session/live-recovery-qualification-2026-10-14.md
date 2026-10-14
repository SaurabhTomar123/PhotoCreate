---
schema: 1
title: "Latest completed autosave recovered in a live interrupted session"
kind: "session"
status: "verified"
date: "2026-10-14"
evidence: ["docs/live-recovery-qualification-2026-10-14.md", "docs/implementation-progress-2026-10-13.md", "docs/system-level-revamp-spec-2026-10-13.md"]
---

The existing native recovery restored revision 6 after a forced test-child termination, superseding revision 5. Three editable layers, inspected layer data and composite samples matched; the recovered document remained unsaved until a native master was saved. Its saved master reopened cleanly. Independent Pillow rendering matched every exported RGBA pixel of the small synthetic RGB8 fixture.

Short first-edit and fresh-launch recovery clips passed. The second edit and real autosave waits are recorded in timestamped commands, not continuously filmed. Five failed attempts remain retained: a 30-second control idle limit required polling during the real one-minute autosave wait, and subsequent idle capture attempts timed out. Capture root cause is unknown; temporary display-awake/visibility settings are not product fixes. A historical Saved status message remained visible while the tab correctly marked newer unsaved edits.

Added the Python recovery auditor and three regression tests; existing audit and memory tests passed with the known real-symlink permission skip. No Rust product code changed. F03 has bounded local qualification; interrupted writes, power loss, large/high-depth/multi-document cases and broader devices remain open. F02 crashes and long idle capture remain open; Atelier and guided studios remain planned.
