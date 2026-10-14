<!-- Generated reference snapshot; edit the canonical source, then run project_memory.py index. -->
Canonical source: [docs/beginner-first-conclusion-2026-10-13.md](../../docs/beginner-first-conclusion-2026-10-13.md)

Source content SHA-256: `9d4619199bcf84add59b808a4cea86ca450226022aa2f55d10842c78f1b545a5`


# PhotoCraft: sophisticated results, simple beginnings

Merged product conclusion, 13 October 2026. Inputs: the owner's 17-page **PhotoCraft Improvement Plan** (`Untitled.pdf`), the recorded audit, the revamp proposal, and the owner's explicit ambition that a beginner, including a 14-year-old, can learn useful workflows within one or two days. Document recommendations are planning evidence; they were not executed as commands. No product fixes or new live recordings were performed during this review.

## Conclusion

Adopt the eight systems in the owner's plan as the foundation for dependable, guided editing. Add an outcome-led creation experience above them. A beginner should start with a desired result, see useful possibilities on their own artwork, make a few understandable decisions, and receive an editable professional-quality output.

The eight systems remove friction and protect trust. They do not, by themselves, teach composition, choose a good starting point, make sophisticated results easy to discover, or establish that the results are better than Photoshop. Those require carefully designed workflows, useful defaults, creative recipes, contextual teaching and measured output quality.

The ambition is **easy to begin, deep enough to grow with**. A professional editing tool contains specialist work that takes longer to master. The one-to-two-day promise should cover a defined set of impressive, useful workflows, rather than mastery of every camera, typography, print and color discipline.

## Corrections before turning the PDF into fix tickets

| PDF statement | Reconciled conclusion |
|---|---|
| All 75 failed menu attempts were context refusals | The raw history has 73 failed menu attempts later resolved with preparation/inputs, plus two TGA assertions based on an incorrect harness expectation. These are not 75 currently broken menu commands. |
| Nine tools cannot be observed; only 56/65 are observable | All nine initially unresolved gestures have successful follow-ups. The baseline now has observable representative results for all 65 tools. A consistent gesture journal and accessibility announcements are still worthwhile. |
| Alpha was `5.96e-8`, proving an unwritten texel | The recorded RGBA value was `[5.9604645e-8, 0, 0, 0]`: the tiny value is red; alpha is zero. The violated opaque-alpha invariant is real. A characteristic half-float value does not establish the root cause. |
| Concurrent GPU devices corrupt memory and may affect real two-window sessions | Native crashes occurred in three targets; serial reruns passed. Device concurrency, backend behavior, test setup and driver issues are hypotheses. Actual multi-window/reset exposure has not been demonstrated. |
| AMD DX12 passes and AMD Vulkan fails on 13 October | This is an additional result reported by the owner document. The retained audit verifies Vulkan failure; matching DX12 evidence was not found in the audit directories during this review. Preserve it as a reported result pending logs/reproduction. |
| Use scratch mip targets immediately as a safe fix | Treat it as a candidate workaround. Validate partial/full equivalence, all supported depths, relevant image sizes and backends before calling it safe. A passing alternate path is not yet a root-cause explanation. |
| All 86 policy refusals are document-only operations | The refusals include genuinely external operations. Classify actual resource use per command. Do not remove protections wholesale or use the prefix-refusal count as the document-only count. |
| 535/622 is an 86% user success rate | It is a latest menu-smoke result with restrictions and prerequisite limits in the denominator. It does not measure first-time user task completion or a 99% guided-success rate. |
| All 631 menu commands should execute without disk access | There are 631 source menu rows, including a duplicate ID and intentionally external actions. Qualify document-only coverage, scoped external coverage, denied/cancelled cases and duplicate rows separately. |
| Every save should report exactly what is lost | Adopt preflight, but retain warnings after completion too: some losses/errors may only become known during export. Pixel equality alone cannot prove that text, masks or filter editability survived. |
| One alpha model means transparency is always recommended | Preserve meaning. An alpha channel may encode a technical mask rather than transparency. Explain the choice, preview it and offer reversible interpretation; do not silently change existing imports. |
| Zero lost work; all kill tests recover every edit | Define the durable-save/autosave boundary and disclosed unsaved interval. Preserve the last valid master and recover eligible checkpoints. A finite test suite cannot guarantee that no future edit can ever be lost. |

The document's reported Photoshop corpus count and timing baselines remain historical/document-reported measurements. Fresh corpus-quality and release-latency results must name the exact run and denominator. The full source extraction and inspected roadmap page are retained locally under `dist/qa/owner-plan-2026-10-13/`.

## The eight systems: adopt, with adjustments

| Owner system | User-facing decision | Important adjustment |
|---|---|---|
| GPU Sentinel | Correct previews and recoverable rendering failure come first | Diagnose the reproduced defect; bounded self-checks and targeted recovery must not create new lag. CPU fallback availability and fidelity need qualification. |
| Command Readiness | Explain what is needed before the user reaches a dead end | Offer a visible plan. Never silently select unrelated layers, rasterize text, merge layers or convert the master to satisfy a tool. |
| Guided Inputs | Acquire maps, planes, paths and targets directly on the artwork | Let users adjust proposed inputs. Automatic perspective detection is optional assistance, not a prerequisite for shipping a usable four-corner editor. |
| Capability-scoped automation | Make approved editing assistance powerful within explicit bounds | Migrate verified resource behavior incrementally. Open-document access, profiles, clipboard, files and network are different capabilities. |
| Observable Canvas | Provide precise feedback, useful history, replay context and announcements | Events complement state/pixel/output checks. An emitted event can be wrong; it cannot replace correctness assertions or accessible navigation. |
| Calm Workspace | Keep the work visible and arrange controls for the current task | Use reserved edges and explicit Tidy/Pin actions. Panels must not chase the cursor or move away while someone is trying to click them. |
| Honest Exchange | Explain format losses and delivery suitability before export | Check feature preservation and independent acceptance, not just rendered pixels. Make assurances specific to tested format/version/features. |
| Living Audit | Preserve recorded evidence and catch regressions continually | Separate quick checks, recorded workflow runs, bounded GPU tests, release performance and hardware sessions. Synthetic replay cannot replace actual pen or beginner testing. |

Readiness and input descriptions support several systems, but no single catalog change automatically completes them. Recovery and output fidelity belong in the earliest trust work, even while richer self-healing and exchange coverage continue later. Remove the need for users to understand error messages without removing their ability to understand the change.

## The missing product layer: start with the result

The opening question should be **What would you like to make or change?** Show a few concrete tasks and allow direct manual editing immediately. Plain-language search can recognize intent; task tiles and recipes also work without AI or a network connection.

Initial task choices:

- Make a poster or social graphic.
- Cut out a subject and replace the background.
- Remove distractions from a photograph.
- Improve light and color.
- Create an artistic print or textured artwork.

The same document supports three levels of control:

| Level | User experience | Continuity |
|---|---|---|
| Create | Choose an outcome and compare a few strong starting points | Result is built from editable layers, masks, text and adjustments |
| Explore | Adjust understandable controls such as warmth, contrast, softness and background | Reveal the affected layer or step; explain what changes |
| Precise | Open detailed curves, masks, paths, blending, type and color controls | Same artwork and history; no conversion into a separate advanced app |

These are progressively revealed controls, not three incompatible file types or a mandatory beginner/expert switch. Pin precise controls and stay there if desired. A learner can open detail for one operation without exposing every advanced tray.

## How sophisticated results become achievable

**Art-directed starting points.** Offer editable layouts and recipes designed for actual use: a music poster, product hero, travel grade, cutout composition and limited-ink print. Layouts respond to the uploaded image, text length, subject position and output size. Include original/licensed material with clear provenance. Attractive sample thumbnails alone do not demonstrate adaptability.

**Image-aware defaults.** Suggest a subject region, usable crop, text-safe area, palette or contrast correction, then make the proposal visible and adjustable. Avoid forcing the same saturation, skin treatment or generic style onto every photograph. Show the limitations when recognition is uncertain.

**A few meaningful choices.** Lead with three differentiated previews of the user's actual image. Give simple controls first, with exact values and detailed settings one step away. A strength slider represents a defined editable operation; it is not an unexplained collection of destructive changes.

**Visible, reversible assistance.** Before a significant transformation, show the target and change. Apply it into an editable step with Undo and Before/After immediately available. Protect pinned layers and user edits. Conversions, destructive changes, remote processing or paid operations require clear disclosure and the relevant authorization.

**Professional finishing guidance.** Offer concrete checks: text legibility at final size, accidental edge halos, subject cropping, inconsistent alignment, missing fonts, small source resolution and output/profile mismatches. Let the user inspect the issue and choose a remedy. Composition and style suggestions are advice, not objective verdicts on the artist's taste.

**Teaching at the moment of use.** One short explanation: “A mask hides the background while keeping the original image.” Offer Show Me and Why options. Repeatable practice projects and useful tooltips replace a long mandatory tutorial. Hints can be dismissed or turned off.

**Reliable delivery.** Ask where the work will go: web, social, print or editable handoff. Prepare the appropriate dimensions and output settings, explain losses, retain the master and let the user inspect the final export. A novice should not need to learn file-format internals before producing a suitable first deliverable.

## Example: a first-session poster

1. Choose Make a Poster and add an image plus a title.
2. See three proposed compositions using that actual content, with different hierarchy and image placement.
3. Pick one; inspect and refine the cutout if needed.
4. Adjust palette, typography and atmosphere with a handful of clear controls.
5. Compare Before/After, inspect any legibility or resolution issues and refine.
6. Export for the intended size; retain an editable master.
7. Open the layer/recipe view to learn how the result was made.

Behind the simple flow may be selection refinement, masks, responsive layout, editable type, adjustment layers and precise export settings. Those sophisticated capabilities must work reliably; simplifying their presentation does not eliminate them.

## Change the UI priority

Keep Atelier as the proposed visual direction, but evaluate its identity through these beginner tasks. A visually attractive editor that still begins with a wall of unfamiliar tools has missed the goal.

Lead with the canvas, desired outcome, current step, a small set of relevant controls and visible comparison/undo. Keep a stable tools rail, direct layer access and command search for manual work. Present the twelve trays as discoverable depth, not twelve simultaneously visible panels. Use names such as Color, Looks, Background, Text and Export in the first experience; reveal specialist terminology when needed.

Do not redesign all 65 tools before testing the new learning model. Prototype three complete experiences first: poster creation, cutout/composite, and photo cleanup/grade. Test them on a laptop-sized screen with a first-time user. Preserve the user's ability to create freely rather than trapping everyone inside a wizard.

## Revised fix and delivery order

| Order | Work | User proof |
|---|---|---|
| 1. Trust | Diagnose/fix the U16 preview failure; investigate GPU crashes; save/recovery integrity; pre-export losses | Correct previews, retained masters and recoverable interruption |
| 2. Reachability | Readiness explanations, visible transform Apply/Cancel, guided inputs for the known problem tools, predictable panel behavior | No developer-style dead ends in the qualified first workflows |
| 3. Feel | Measure and improve brush/canvas interaction, opacity/blend preview, selection and type editing | Defined release workloads meet published input-to-visible budgets |
| 4. Beginner success | Outcome entry, editable starting points, image-aware defaults, three previews, short contextual teaching | First-time users finish and understand useful work |
| 5. Distinct studio | Prototype and adopt the new shell and contextual tray model around proven workflows | Aesthetic identity improves clarity and completion rather than adding decoration |
| 6. Professional depth and handoff | Deep masking/retouch/type/RAW/color; independent exports; delivery and batch workflows | Outputs retain the required quality and editability in intended destinations |
| 7. Artistic expansion | Reference Desk, palette, print/material recipes, branches and replay; later natural media and generative work | A coherent creative workflow produces distinctive finished pieces |

The ordering is by shipping priority. Design exploration, beginner research and recipe prototyping can proceed alongside trust work; they need not wait for every specialist renderer feature. Conversely, the new shell must not disguise unresolved reliability problems.

Capability migration, gesture feedback and continuing audits support these stages. They are not the beginner-facing product pitch. Do not gate initial user testing on describing every command in the whole registry. Qualify the first complete workflows, then expand the command/workflow coverage honestly.

## Make the one-to-two-day ambition measurable

All targets below are proposed qualification goals, not measured achievements. Recruit a varied beginner cohort, including the target teenage audience as appropriate, using representative hardware and unfamiliar assets. Include returning learners and more experienced users so simplicity does not come at the expense of control.

| Outcome | Proposed first qualification goal |
|---|---|
| Useful first result | At least 90% of novice participants finish one guided core task in ten minutes without facilitator intervention |
| First-day usefulness | Most participants complete three of the five starting workflows after no more than one hour of optional teaching |
| Day-two independence | At least 80% complete a new variant task on unfamiliar content without replaying a step-by-step tutorial |
| Understanding | Users can identify what changed, undo it, edit text and refine a mask rather than merely accepting a generated result |
| Output quality | Blind review against a defined brief finds acceptable edges, typography, composition and delivery settings; review artistic preference separately |
| Professional control | Experienced users can reach needed precision controls without repeatedly leaving the active task |
| Trust and speed | Independently qualify saved outputs, recovery boundaries, input-to-visible timing and supported hardware |

Choose cohort size, recruitment, task difficulty and scoring rubric before testing. Report participant counts, distribution and failures alongside percentages. Do not call a successful tutorial run independent learning. Do not classify “cannot do this” with a helpful message as successful completion.

For the “better than Photoshop” ambition, compare specific outcomes: novice completion time, required help, number of corrections, output quality and editability, using the same brief and assets. Record product versions, user experience levels and reviewer criteria. PhotoCraft can target better beginner workflows without making an unverified claim that it is already better at every specialist task.

## Decisions and records

The [main revamp plan](user-first-revamp-plan-2026-10-13.md) now carries this audience and experience goal. The [feature backlog](revamp-feature-backlog-2026-10-13.csv.md) maps the owner's systems onto existing work and adds the beginner-success deliverables. They remain planning proposals.

Recommended defaults: editable guided recipes; short dismissible teaching; explicit preview of meaningful changes; manual editing always available; no mandatory cloud AI; no automatic master conversion to satisfy a command. Optional capabilities and presets can make the first result approachable without promising instant expertise.

Upstream versus fork, licensed Photoshop qualification access, supported hardware, remote AI services and any optional field reporting remain implementation/delivery decisions. This review does not create a fork, alter automation policy, contact upstream, install services or authorize deployment.

Next concrete planning deliverable: task-level storyboards for poster, cutout/composite and photo cleanup/grade, covering first use, uncertain suggestions, manual refinement, undo, errors and final export. Judge those experiences with novices before locking the entire visual redesign.
