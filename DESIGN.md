---
name: Durge Guide
description: The fan site for a Baldur's Gate 3 mod, built from the grammar of the game's own screens.
colors:
  ink: "#0b0506"
  night: "#140b0c"
  wine-deep: "#1b060a"
  wine: "#2b0a10"
  wine-lift: "#3a1218"
  bone: "#efe6d6"
  ash: "#c6b5a6"
  gold-hi: "#f0d9a4"
  gold: "#dcb76c"
  gold-mid: "#a98a52"
  gold-low: "#7d6540"
  blood: "#b3202e"
typography:
  display:
    fontFamily: "Grenze Gotisch, Grenze Fallback, Georgia, serif"
    fontSize: "clamp(3.2rem, 1rem + 5.4vw, 7.25rem)"
    fontWeight: 700
    lineHeight: 1.04
  headline:
    fontFamily: "Grenze Gotisch, Grenze Fallback, Georgia, serif"
    fontSize: "clamp(2.25rem, 1.5rem + 2.2vw, 3.5rem)"
    fontWeight: 700
    lineHeight: 1.04
  title:
    fontFamily: "Grenze Gotisch, Grenze Fallback, Georgia, serif"
    fontSize: "1.8rem"
    fontWeight: 500
    lineHeight: 1.1
  lede:
    fontFamily: "Grenze, Grenze Fallback, Georgia, serif"
    fontSize: "clamp(1.35rem, 1.15rem + .55vw, 1.625rem)"
    fontWeight: 400
    lineHeight: 1.32
  body:
    fontFamily: "Grenze, Grenze Fallback, Georgia, serif"
    fontSize: "1.25rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Grenze, Grenze Fallback, Georgia, serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.3
  code:
    fontFamily: "ui-monospace, SF Mono, Menlo, Consolas, monospace"
    fontSize: "0.8em"
    fontWeight: 400
    lineHeight: 1.4
rounded:
  control: "3px"
  panel: "10px"
spacing:
  s1: "0.25rem"
  s2: "0.5rem"
  s3: "0.75rem"
  s4: "1rem"
  s5: "1.5rem"
  s6: "2rem"
  s7: "3rem"
  s8: "4.5rem"
  s9: "7rem"
components:
  button-plaque:
    backgroundColor: "{colors.night}"
    textColor: "{colors.gold-hi}"
    rounded: "{rounded.control}"
    padding: "0.35em 1.5em 0.4em"
    height: "48px"
  button-plaque-hover:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.ink}"
  journal-tab:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.ash}"
    rounded: "{rounded.panel}"
    height: "46px"
  journal-tab-active:
    backgroundColor: "{colors.wine}"
    textColor: "{colors.bone}"
  panel:
    backgroundColor: "{colors.night}"
    textColor: "{colors.bone}"
    rounded: "{rounded.panel}"
---

# Design System: Durge Guide

## Overview

**Creative North Star: "The Game's Own Screens"**

The mod's whole idea is that it has no interface of its own: a voice settles into the screens already there. The site works the same way. Its controls and frames are the grammar of Baldur's Gate 3's interface, redrawn in our own CSS and SVG: the question you answer with numbered dialogue lines, the region banner a place's name arrives in, the popup a note sits in, the journal's tabs. Its second idea is withholding. Later-story screenshots sit behind wax seals, because hiding things is what the mod does.

Ambition moves with the job. Home and Tiers persuade, so the world carries the page. Screenshots is a showcase, so the captures lead. Docs are for reading, so the world holds the frame (banner, rail, tabs, tables, notes) and the column stays calm. It is a fan project and must never look official: no Larian logo or logotype, and the footer line stays.

**Key Characteristics:**
- Near-black panels with a gold hairline, on an oxblood ground.
- Blackletter for names and questions, a calm text face for everything read.
- Real captures as the proof. Ornament is only ever our own CSS and SVG.
- One authored motion per moment: a scene spreading from the note, a banner arriving, a seal breaking.
- Works without JavaScript. Scripts only add to it.

## Colors

Dark because it sits beside a dark game and is read by people who play in dim rooms. Oxblood owns the ground, near-black owns the panels, gold draws the edges, and blood is rare.

### Primary
- **Brass** (gold): links, chevrons and the plaque's border. The game's metal.
- **Candle** (gold-hi): the selected dialogue line, the plaque's words, focus rings.
- **Tarnish** (gold-mid, gold-low): hairlines on panels and tabs. Gold-low is the quietest line a control may have.

### Secondary
- **Blood** (blood): the current page's underline, the active tab's fill, the seal, the chosen column's tint. Never text.

### Neutral
- **Parchment** (bone): body text and headings.
- **Ash** (ash): captions, secondary cells, the unselected tab. Warm, never grey.
- **Ink, Night** (ink, night): panels, the bar and the footer.
- **Oxblood** (wine-lift, wine, wine-deep): the ground, in one slow diagonal.

### Named Rules
**The Metal Is Thin Rule.** Gold is a hairline or a small word. It never fills a surface, except a plaque being pressed.

**The Blood Is Rare Rule.** Blood marks where you are or what is sealed. If it marks anything else it stops meaning something.

## Typography

**Display Font:** Grenze Gotisch (with a metric-matched Georgia fallback)
**Body Font:** Grenze (with the same fallback)
**Code Font:** the system monospace, for code and file names only

**Character:** The two faces are one family's two voices: Grenze Gotisch is the game speaking, and Grenze is it being clear. Both are variable fonts, self-hosted, Latin only.

### Hierarchy
- **Display** (700, up to 7.25rem): the home question and the closing line.
- **Page name** (700, up to 4.75rem): inside a region banner.
- **Headline** (700, up to 3.5rem): section heads.
- **Title** (500, 1.8rem): sub-heads and tier labels.
- **Lede** (400, up to 1.625rem): the opening paragraph of a persuading page, and the narrator's line.
- **Body** (400, 1.25rem, 1.5): running text, at 54ch, which sets about 70 characters in this narrow face.
- **Label** (400, 1.0625rem): captions and table notes. Never smaller.

### Named Rules
**The Blackletter Is For Names Rule.** Grenze Gotisch is only for headings of 1.5rem or more. Its capital A reads as an R at small sizes, so small labels use Grenze.

**The Lining Numbers Rule.** Tables use lining tabular figures. Prose keeps the face's old-style figures.

## Layout

The page is 1240px with 16px gutters and safe-area insets. Sections sit 4.5rem apart, joined by a hairline with a diamond at its centre. The home scene is full-bleed, and tiers stack from 1099px down. Space uses a 4-based scale.

- **Home:** the first viewport is one scene. The notes keep the left 37%, and the conversation takes the rest, on a curtain of dark that never touches a note, at any tier. Below 1100px the words come first and the scene follows, and on a phone the scene is a crop of the note so it can be read.
- **Tiers:** the three choices sit directly above the table's three columns, so one column reads from advice down to counts.
- **Docs:** rail, column, contents at 1280px and up. Rail and column at 901px. Tabs and column below.
- **Tables:** never scroll sideways. On a phone the row's name goes on top with the three tiers under it, and docs tables stack.

## Elevation & Depth

Flat. Depth comes from tone: oxblood ground, near-black panel, gold line. Nothing casts a shadow except the hero heading's soft dark glow, which separates it from the scene.

**The Line Not Shadow Rule.** If a surface needs lifting, it gets a darker ground and a hairline.

## Shapes

Two radii: 10px for panels, 3px for controls and code. Region banners are square-cornered with a dashed outer line, like the game's. Round nodes sit on edges: the drop on a popup's top left, the compass star under a banner, the handle on a slider. Diamonds mark the centre of a divider and the ends of a plaque.

## Components

### Dialogue lines (the tier switch)
Numbered lines, the way the game's conversations are. They are radio buttons under the labels, so the switch runs on CSS alone. A short hint sits above them. The chosen line takes double chevrons, Candle text and a gold wash that fades to the right. The scene behind it is revealed from the note outward over a second, and the home page always starts at Normal. Inside the group, 1, 2 and 3 answer, and the hint says so once focus is there. Your answer follows you to the Tiers page.

### Region banner (`h1`)
Dark band, hairline, dashed outer line, compass node at the bottom centre. It opens from the middle once on arrival, on the persuading pages.

### Popup note (`.note`)
The game's side popup: panel, drop node on the top left edge, a curl of our own in the bottom right corner. It carries a note or a warning, and replaces any callout.

### Plaque (`.btn`)
The primary action. Dark fill, one gold line, a diamond at each end, which part when hovered. The fill turns to gold on hover. Secondary actions are plain links.

### Journal tabs (`.strip`)
Tabs hanging from a gold rule, sticky on long pages, following the reader. The current one fills with blood and takes a diamond. On wide docs pages the same tabs become a rail.

### Spoiler seal (`.gate`)
A native `details`. Near-black panel, wax seal, 'Hidden: reason', and a plain action that says how much is behind it, or what. Opening breaks the seal and the shot comes up out of a blur. One seal per decision, never twin seals with the same label.

### Screenshot (`.shot`)
A plate with a hairline, a caption under it, and a link to the full size. With scripts it opens in a lightbox that grows out of the thumbnail, with Zoom for reading a note on a phone. The lightbox's sequence only holds shots you have chosen to see. A wide comparison pans sideways on a phone rather than shrinking past reading.

### Sliding divide (`.wipe`)
Two aligned shots with a draggable divide. A native range input does the work. Without scripts they sit side by side.

## Do's and Don'ts

### Do:
- **Do** put every fact, count and test result in as written. Design never rounds a number or softens 'not tested'.
- **Do** keep later-story captures behind a seal, and keep 'earlier cut' with any shot that carries it.
- **Do** cut new crops from `docs/img` and declare them in `images.py`.
- **Do** give every motion a reduced-motion path that keeps the state change.
- **Do** keep the site fully working with scripts off.

### Don't:
- **Don't** use a kicker above a heading, section numbers, gradient text or glass.
- **Don't** use a thick coloured edge on a callout. Use the popup.
- **Don't** use radial glows. The ground is a slow linear shift.
- **Don't** draw particles or anything else over a capture. Specks on a note read as dirt on the words, which is why the embers were cut.
- **Don't** copy Larian's logo, or make the site look official.
- **Don't** add a light theme as the identity.
