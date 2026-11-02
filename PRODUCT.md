# Product

<!-- impeccable:product-schema 1 -->

Every fact below is taken from the owner's written brief and the site's own copy. No interview happened: no one was available to answer, so `init` ran from that brief.

## Platform

web

## Users

- Baldur's Gate 3 players deciding whether they want this mod. Most are mid-run or about to start a first Dark Urge playthrough, and they are wary of spoilers.
- Modders curious how a native mod can do this without Script Extender. They read the how-it-works page.

## Product Purpose

Durge Guide is a native (no Script Extender) mod for Baldur's Gate 3. A voice settles into the game's own screens: short side-popup notes where you stand, journal detail, quest lines, dialogue marks, item tooltips, map pins and warnings. It comes in three tiers: Minimal, Normal and Extensive.

The site lets a player see exactly what each tier shows and decide how much they want to know. There is no public download yet, and the site says so honestly. Success today is a reader who understands the mod and its tiers, not a download.

## Positioning

It has no overlay and no new menu. Nothing but the game's own screens, saying a little more than they did, and only as much as you allow. The player chooses how much is revealed when installing.

## Operating Context

- Written for a first Dark Urge run with an Open Hand Monk, travelling with Astarion, Karlach and Shadowheart, with a few item mods in the pack.
- Tested on game version 4.1.1.7631656 on the native Linux build. The docs carry the full test record.
- The site is static: GitHub Pages serves `main:/docs`, built by a Python stdlib script. No npm and no framework. It must work fully without JavaScript, so any script is progressive.
- The game box can't be reached for now, so there are no new captures. Crops and re-encodes come from `docs/img`, and each new slot is declared in `images.py`.

## Capabilities and Constraints

- Three tiers, chosen at install. The words are bound into the game's language file, so changing tier means rebuilding with the game closed.
- English only. The native Linux build is the only one tested.
- Tier counts and test results are exact facts held on the Tiers and Compatibility pages. They never change for the sake of a design.
- Undecided: a release date. There is no public download yet, the Install page's steps are the ones used on the test machine, and the site says both plainly. Don't promise a date.

## Brand Commitments

- The voice in `STYLE.md`: Larian's rhythm measured from the game's text, never its lines. British spelling. No semicolons or exclamation marks in copy. `python3 style.py` checks it.
- An unofficial fan project. The footer line stays, and nothing may look official. No Larian logo or logotype.
- "Not released", "not tested" and "earlier cut" statements stay exact.
- AI authorship is stated plainly on the FAQ and Credits pages.

## Evidence on Hand

- Real captures in `docs/img` at all three tiers. Those from later in the story stay behind "Hidden:" gates.
- Counts on the Tiers page and the test table on the Compatibility page.
- There are no testimonials, download figures, press or release date. Don't invent them.

## Product Principles

1. Tell only as much as you were asked. The site withholds like the mod does: later-story screenshots stay gated, and copy says nothing from later in the story (no Bhaal, no butler, no twists). The player is "you", never gendered.
2. Prove it with the real screens. A capture beats a claim, and a test result beats an adjective.
3. Be exact about what isn't done. Limits are stated as flatly as features.
4. Belong to the game. If it could be any other mod's page, it has failed.

## Accessibility & Inclusion

No product-specific requirement was stated. WCAG AA, full keyboard use and reduced motion are the working floor. Spoiler gates must be operable and clear to everyone, since revealing too much can't be undone.
