#!/usr/bin/env python3
# Turns the full-size captures into the site's images, thumbnails and tier comparisons.
# usage: uv run --with pillow python images.py CAPTURE_DIR
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

src, root = Path(sys.argv[1]), Path(__file__).parent
out = root / "docs" / "img"
(out / "t").mkdir(parents=True, exist_ok=True)
SHOTS = {
    "a1-normal-welcome": "normal-a1-welcome", "a1-minimal-welcome": "minimal-a1-welcome", "a1-extensive-welcome": "extensive-a1-welcome",
    "a1-minimal-grymforge": "minimal-a1-grymforge-3", "a1-normal-grymforge": "normal-a1-grymforge-2", "a1-extensive-grymforge": "extensive-a1-grymforge-2",
    "a1-normal-glint": "normal-a1-buried-chest-2", "a1-extensive-sazza": "extensive-a1-hollow-sazza-1", "a1-extensive-buried-chest": "extensive-a1-buried-chest-2",
    "a1-normal-map": "normal-a1-map", "a1-extensive-map": "extensive-a1-map", "a1-normal-quest": "normal-a1-quest", "a1-extensive-quest": "extensive-a1-quest",
    "a1-minimal-camp-warning": "minimal-a1-camp-warning",
    "a2-normal-quest": "normal-a2-quest", "a2-extensive-quest": "extensive-a2-quest", "a2-normal-map": "normal-a2-map", "a2-extensive-map": "extensive-a2-map",
    "a3-minimal-note": "minimal-a3-box", "a3-minimal-dialogue": "minimal-a3-dialogue-notag", "a3-minimal-quest": "minimal-a3-quest-urgency", "a3-minimal-exit": "minimal-a3-point-of-no-return-1",
    "a3-normal-note-shop": "normal-a3-danthelon-3", "a3-normal-note-pool": "normal-a3-dock-3", "a3-normal-note-last-shop": "normal-a3-koll-2",
    "a3-normal-box-controller": "normal-a3-box-controller", "a3-normal-notice": "normal-a3-voss-2", "a3-normal-notice-barn": "normal-a3-barn-controller-2",
    "a3-normal-notice-refugee": "normal-a3-refugee-controller-2", "a3-normal-dialogue": "normal-a3-dialogue-controller", "a3-normal-tooltip": "normal-a3-tooltip-controller",
    "a3-normal-journal": "normal-a3-journal-note",
    "a3-extensive-note-shop": "extensive-a3-danthelon-3", "a3-extensive-note-pool": "extensive-a3-dock-2", "a3-extensive-exit": "extensive-a3-checklist-1",
    "a3-extensive-dialogue": "extensive-a3-dialogue-controller-2", "a3-extensive-tooltip": "extensive-a3-tooltip-controller", "a3-extensive-journal": "extensive-a3-journal-note",
}
for new, old in SHOTS.items():
    Image.open(src / f"{old}.png").convert("RGB").resize((1920, 1080), Image.LANCZOS).save(out / f"{new}.jpg", quality=84, optimize=True, progressive=True)
# the hero is cropped in, so the note can be read at page width
for tier in ("minimal", "normal", "extensive"):
    Image.open(src / f"{tier}-a1-waukeens-rest-3.png").convert("RGB").crop((0, 50, 1880, 1108)).save(out / f"hero-{tier}.jpg", quality=86, optimize=True, progressive=True)
for new in ("pin-before", "pin-after"):
    Image.open(src / f"{new}.jpg").convert("RGB").save(out / f"{new}.jpg", quality=86, optimize=True)

font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 34)


def compare(name, crops, box, stack=False):
    """The same region of each capture under its tier's name, side by side or stacked."""
    ims = [Image.open(src / f"{n}.png").convert("RGB").crop(box) for _, n in crops]
    w, h = ims[0].size
    pad, top, n = 16, 60, len(ims)
    size = (w + 2 * pad, n * (h + top) + pad) if stack else (n * w + (n + 1) * pad, h + top + pad)
    o = Image.new("RGB", size, (28, 6, 10))
    d = ImageDraw.Draw(o)
    for k, ((label, _), m) in enumerate(zip(crops, ims)):
        x, y = (pad, k * (h + top)) if stack else (pad + k * (w + pad), 0)
        o.paste(m, (x, y + top))
        d.text((x + 4, y + 12), label, font=font, fill=(238, 228, 210))
    if o.width > 2560:
        o = o.resize((2560, round(o.height * 2560 / o.width)), Image.LANCZOS)
    o.save(out / f"compare-{name}.jpg", quality=88, optimize=True)


T = ("Minimal", "Normal", "Extensive")
compare("notes", list(zip(T, ("minimal-a1-waukeens-rest-3", "normal-a1-waukeens-rest-3", "extensive-a1-waukeens-rest-3"))), (130, 130, 760, 760))
compare("notes-act3", list(zip(T, ("minimal-a3-box", "normal-a3-danthelon-3", "extensive-a3-danthelon-3"))), (130, 130, 760, 660))
compare("quest-lines", list(zip(T, ("minimal-a3-quest-urgency", "normal-a1-quest", "extensive-a1-quest"))), (1240, 270, 2400, 760))
compare("dialogue", list(zip(T, ("minimal-a3-dialogue-notag", "normal-a3-dialogue-controller", "extensive-a3-dialogue-controller"))), (360, 960, 2240, 1400), stack=True)
compare("tooltips", list(zip(T[1:], ("normal-a3-tooltip-controller", "extensive-a3-tooltip-controller"))), (1780, 480, 2300, 1270))
compare("map-pins", list(zip(T[1:], ("normal-a1-map", "extensive-a1-map"))), (500, 80, 2200, 1390))

sizes = {}
for p in sorted(out.glob("*.jpg")):
    im = Image.open(p)
    sizes[p.stem] = im.size
    im.convert("RGB").resize((800, round(im.height * 800 / im.width)), Image.LANCZOS).save(out / "t" / p.name, quality=72, optimize=True, progressive=True) if im.width > 800 else im.save(out / "t" / p.name)
(root / "src" / "sizes.json").write_text(json.dumps(sizes))
print(len(sizes), "images")
