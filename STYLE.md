# How Larian writes

Measured from the game's own English text: 6,850 narrator lines, 2,529 item descriptions and 3,157 journal entries. All new copy on this site follows it. Copy the method, never the lines.

| Voice | Median sentence | Longest 10% start at | "You" per 100 words | Dashes per 100 sentences |
|---|---|---|---|---|
| Narrator | 9 words | 17 | 7.7 | 12 |
| Item text | 13 words | 23 | 0.8 | 10 |
| Journal | 11 words | 19 | 0.2 ("we": 6.0) | 11 |

Semicolons almost never appear (0.4 per 100 sentences), and neither do exclamation marks (0.7). Spelling is British. The dash is a spaced hyphen, " - ". Titles and quoted words take single quotes.

## The narrator

Second person, present tense. It tells you what you feel, and it knows more than it says.

- **Start plain.** The commonest openers are "You feel", "You are", "There is", "It seems", "This is" and "You see".
- **Let the second beat turn.** A flat statement, then a shorter one that bites. "He stares right past you as if you're invisible. Or boring."
- **State consequences flatly.** No alarm and no adjectives. "Defiling a corpse is a crime. Guards are being summoned."
- **Withhold.** Hedges carry the menace: seems, perhaps, something, nothing, might. "There's something strange about the rat. But what?"
- **Stay in the body.** Mind, eyes, blood, hand, head, heart, skin, stomach. Things pulse and shiver and smell.

## Item text

Mostly fragments, with no "you". It names the thing, then adds a dry second thought.

- "A draped robe made with lightweight fabric. Made for seduction rather than battle."
- "The day's catch. The smell suggests it's starting to go off."

Sentences often open with Though, Despite or While, and the joke arrives at the end.

## On this site

| Where | Voice |
|---|---|
| Home, Tiers, In the game | Narrator |
| Captions and table cells | Item text |
| Docs | The narrator's rhythm, with exact instructions. Clarity wins every time. |
| How it works, Credits | Plain. A modder or a lawyer needs the fact. |

## Limits

- Never give up a fact for a flourish. Test results, limits and "not released" stay exact.
- One turn per paragraph at most. Most sentences just say the thing.
- Nothing from later in the story. No Bhaal, no butler, no twists.
- Buttons, tabs and spoiler bars stay plain, the way the game's own interface does.

`python3 style.py` measures every page against these numbers.
