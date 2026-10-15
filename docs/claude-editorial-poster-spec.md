# Make an editorial poster: workflow specification (Claude L1)

15 October 2026. Status: **specification and manual proof**. No product code exists yet. The three art directions below were built and rendered with existing engine commands only (evidence: [records/2026-10-15/claude-editorial-poster](../records/2026-10-15/claude-editorial-poster/)); the guided flow, recipe engine and tray are proposals for L2–L4. Command details and observed behaviour are in the [command and API map](claude-editorial-poster-command-map.md).

## 1. Outcome

A first-time creator turns one of their own photos and a title into a sophisticated, print-ready editorial poster, then keeps editing it like any other document: the photo, words and colours stay separate, editable layers. Target for the proposed user test: a good first result within ten minutes, with no unexplained dead end (work plan, step 4). This is a target, not a measured learning-time claim.

What this is not: generative imagery, cloud processing, a template that replaces the user's photo, or a claim of Photoshop parity. Everything runs offline through normal engine commands.

## 2. Principles specific to this recipe

| Principle | Rule |
|---|---|
| Protect the original | The recipe always builds a **new document**. The user's photo file and open document are never modified, converted or flattened. |
| Real previews only | Direction cards and variations are rendered from the user's actual photo and title by the real compositor at proxy size. No stock thumbnails. |
| Editable result | Photo = embedded smart object (non-destructive scale/position); words = live type layers; frames and rules = live shape layers; colour = adjustment and fill layers. Layer names are plain words ("Photo", "Title", "Shade for text"). |
| One step to undo | Applying the recipe is one History step, labelled "Editorial poster (Gallery)". A failure leaves no half-built document (see map §5). |
| Visible defaults | Every automatic choice (crop focus, font substitution, title size, palette) is shown in the tray and can be changed. |
| Never silent | Missing fonts, low resolution, weak text contrast and long titles are explained where the user is looking, with a fix offered. |

## 3. Inputs

| Input | Required | Default | How it is acquired |
|---|---|---|---|
| Photo | Yes | The active document's image when one is open; otherwise none | "Use the open photo" or "Choose a photo…" (file dialog). File access happens **before** the recipe runs and outside its rollback. Drag-and-drop onto the tray also works. |
| Title | Yes | Empty, placeholder "Your title" | Single-line field; Enter moves to the subtitle. |
| Subtitle | No | Empty | Single-line field ("who, where, when"). |
| Palette | Yes | "From your photo" | Three swatches (paper, ink, accent). Choices: From your photo (sampled), four curated palettes, or Custom (colour picker). |
| Format | Yes | Portrait 4:5 | Portrait 4:5, A-series print, Square 1:1, Story 9:16. Size presets map to pixels at 150 ppi (print sizes show the effective ppi of the photo). |
| Art direction | Yes | Gallery | Three cards (§4), each a live preview. |
| Variation seed | Internal | 1 | "Try another" increments it; shown as "Variation 3 of ∞" with Back. |

## 4. The three art directions

All three were built from existing commands and checked visually. Layer stacks are bottom to top.

| Direction | Feel | Layer stack (bottom → top) | User-facing controls |
|---|---|---|---|
| **A. Gallery** | Calm, museum print | Background (paper colour) · Photo frame (shape) · Photo (smart object, clipped to frame) · Title (serif) · Rule (line) · Subtitle (accent) · Credit | Photo focus and zoom; title, subtitle; palette; margin size (Tight / Classic / Generous) |
| **B. Bold overlay** | Cinematic, full bleed | Background · Photo (smart object, cover) · Duotone (gradient map, palette) · Shade for text (gradient fill, Multiply) · Title (condensed) · Subtitle | Photo focus; mood strength (duotone opacity); shade strength; title position (bottom / top) |
| **C. Swiss block** | Graphic, magazine | Background (paper) · Colour block (shape, accent) · Photo frame (shape) · Photo (clipped) · Black and white (adjustment, clipped) · Title line 1, line 2 (heavy sans) · Subtitle · Year · Issue | Photo focus; colour block height; black-and-white on/off; title split point |

Layout is computed, not fixed: the photo is cover-scaled into its frame from the placed image's returned bounds, the focus point decides the crop, and the title is fitted to its column width by measuring the laid-out text (`type.info` lines) and resizing (`type.setStyle`). The prototypes used hand-computed numbers for two images (square and landscape); the recipe engine (L3) must reproduce them from bounds.

### Fonts

Each direction names a fallback chain that ends in **Inter**, which ships with PhotoCraft: A `Playfair Display → Georgia → Times New Roman → Inter`; B `Bebas Neue → Anton → Impact → Inter Black → Inter`; C `Montserrat Black → Archivo Black → Inter Black → Inter`. The recipe resolves the chain against `type.fonts` before running and shows "Title font: Georgia (Playfair Display isn't installed)" in the tray. The prototypes used fonts installed on the recording machine; only Inter is guaranteed (see progress report, known gaps). Bundling open-licence display fonts belongs in the upstream craft-fonts process, not in this repository.

### Variations (deterministic)

A variation is a pure function of (recipe version, direction, inputs, seed). Same inputs and seed always give the same document. Variation axes, bounded so every result stays on-brief: title placement within the direction's allowed zones; palette rotation (which swatch is accent); photo focus nudge within the safe crop; type pairing from the direction's chain; frame proportion within ±10%. The recipe version is stored in the document's layer names/metadata note so a later recipe change never silently alters an old poster.

## 5. The flow

1. **Start.** Entry points: (a) Home › Create › "Editorial poster"; (b) with a photo open, the guided tray offers "Make a poster from this photo"; (c) command palette, keywords "poster", "editorial", "magazine". All open the same guided tray beside the canvas; the canvas stays visible.
2. **Photo.** Use the open photo or choose one. Shows the photo with its pixel size and the effective print resolution for the selected format.
3. **Words.** Title (required), subtitle (optional). Live character count; long titles are fitted automatically and flagged if the fitted size falls below the direction's minimum.
4. **Look.** Three direction cards rendered from the user's photo and title, then palette and format. "Try another" varies the selected direction.
5. **Apply.** Builds the poster as a new document in one undoable step, selects the Title layer, and shows the finishing checks. The tray stays open in "Adjust" mode with the same controls, now editing the real layers.
6. **Go further.** "Show layers" reveals the Layers panel with the poster's layers; "Edit by hand" collapses the tray. Nothing in the result depends on the tray: closing it leaves an ordinary document.

Cancel at steps 1–4 discards only the preview; nothing has been created. Cancel during apply (long previews on large photos) stops the job and leaves no new document.

## 6. Progressive depth in one document

| Level | Who | What they see |
|---|---|---|
| Create | First-time | Photo, title, subtitle, three directions, palette, format, Apply |
| Explore | Curious | Variations, mood and shade strength, margin, title position, focus point |
| Precise | Experienced | "Show layers": the real layer stack, type, adjustments and masks in the normal panels |

The levels differ in presentation only. Every control maps to an existing command (map §2).

## 7. Empty, error and warning states

| Situation | What the user sees | Offered action |
|---|---|---|
| No photo chosen | Direction cards show a neutral placeholder with "Add a photo to see your poster" | Use open photo / Choose a photo |
| Photo can't be read | "This file couldn't be opened as an image" with the format | Choose another |
| No title | Apply disabled; field shows "Add a title" | Focus the field |
| Title too long for the column | Title fitted down; if below the direction's minimum size: "Long titles work better in Gallery or split onto two lines" | Switch direction / split line |
| Font missing | "Title font: Inter (Bebas Neue isn't installed)" | Pick another installed font |
| Low resolution | "At A3 this photo prints at 96 ppi; 150+ looks sharp" | Choose a smaller format / continue |
| Weak text contrast | Contrast of title against the pixels behind it below 4.5:1: "The title may be hard to read here" | Raise shade / move title / change ink colour |
| 16-bit, CMYK or Lab photo | Intended: the photo is embedded as a smart object in an RGB 8-bit poster and the source stays untouched, stated in the summary. **Not yet verified**: only 8-bit RGB JPEGs were tested. | To define after testing |
| Apply fails part-way | Nothing is left behind; "The poster couldn't be finished: <reason>. Nothing was changed." | Try again / report |

Finishing checks never call a design choice wrong; they report measurable risks (contrast, resolution, clipping of text by the canvas edge, font substitution).

## 8. Keyboard and accessibility

- Tab order follows the flow: photo → title → subtitle → direction cards (arrow keys move between cards) → palette → format → Apply.
- Enter applies when the form is valid; Esc cancels; Ctrl+Z after apply undoes the whole poster.
- Every control has an accessible name; direction cards announce their name and the selected state; warnings are announced when they appear.
- Focus is always visible with the theme's focus token; the tray respects the UI scale setting; no information is carried by colour alone (warnings have text and an icon).

## 9. Acceptance (for L3, L4 and the user test)

1. Two unfamiliar public-domain photos (square and landscape) × three directions produce six posters whose photo, title and colours are separate editable layers; save as `.pcraft`, reopen, and the stack is unchanged.
2. Apply is one History step; undo returns to the state before apply; a forced failure at the last step leaves no new document and no extra history.
3. The same inputs and seed produce byte-identical `.pcraft` layer trees and equal PNG renders.
4. Missing font, long title, low resolution and weak contrast each show their message and their fix works.
5. The complete path works with keyboard only.
6. The user test (work plan step 4): three first-time users reach a result they'd share within ten minutes, recorded with their stuck points.

## 10. Decisions needed

- **New document always?** Recommended: yes (protects the original). Alternative: also offer "add to this document" later.
- **Default format:** Portrait 4:5 at 150 ppi (1600×2000) proposed; owner may prefer A-series for print.
- **Transaction interface** in the engine: proposal in the map §5; must be agreed with Codex before L3 depends on it.
- **Display fonts:** whether to request open-licence display faces through craft-fonts, so all three directions look as designed on every machine.
