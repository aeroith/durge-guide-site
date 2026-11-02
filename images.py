#!/usr/bin/env python3
# Turns the full-size captures into the site's images, thumbnails and tier comparisons, then derives the crops and WebP sizes.
# usage: uv run --with pillow python images.py CAPTURE_DIR    remake everything from the captures
#        uv run --with pillow python images.py --derive       remake only what comes from docs/img: crops, WebP sizes, missing thumbnails, sizes.json
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).parent
out = root / "docs" / "img"
(out / "t").mkdir(parents=True, exist_ok=True)
(out / "w").mkdir(parents=True, exist_ok=True)
SHOTS = {
    "a1-normal-welcome": "normal-a1-welcome", "a1-minimal-welcome": "minimal-a1-welcome", "a1-extensive-welcome": "extensive-a1-welcome",
    "a1-minimal-grymforge": "minimal-a1-grymforge-3", "a1-normal-grymforge": "normal-a1-grymforge-2", "a1-extensive-grymforge": "extensive-a1-grymforge-2",
    "a1-normal-glint": "normal-a1-buried-chest-2", "a1-extensive-sazza": "extensive-a1-hollow-sazza-1", "a1-extensive-buried-chest": "extensive-a1-buried-chest-2",
    "a1-normal-map": "normal-a1-map", "a1-extensive-map": "extensive-a1-map", "a1-normal-quest": "normal-a1-quest", "a1-extensive-quest": "extensive-a1-quest",
    "a1-minimal-camp-warning": "minimal-a1-camp-warning",
    "a2-normal-quest": "normal-a2-quest", "a2-extensive-quest": "extensive-a2-quest", "a2-normal-map": "normal-a2-map", "a2-extensive-map": "extensive-a2-map",
    "a3-minimal-note": "minimal-a3-koll-2", "a3-minimal-dialogue": "minimal-a3-dialogue-notag", "a3-minimal-quest": "minimal-a3-quest-urgency", "a3-normal-exit": "normal-a3-exit-3",
    "a3-normal-note-shop": "normal-a3-danthelon-3", "a3-normal-note-pool": "normal-a3-dock-3", "a3-normal-note-last-shop": "normal-a3-koll-2",
    "a3-extensive-box-controller": "extensive-a3-barn-controller-2", "a3-normal-notice-barn": "normal-a3-barn-controller-3",
    "a3-extensive-notice-refugee": "extensive-a3-refugee-controller-2", "a3-normal-dialogue": "normal-a3-dialogue-controller", "a3-normal-tooltip": "normal-a3-tooltip-controller",
    "a3-normal-journal": "normal-a3-journal-note",
    "a1-normal-journal": "normal-a1-journal", "a1-extensive-journal": "extensive-a1-journal",
    "a3-extensive-note-shop": "extensive-a3-danthelon-2", "a3-extensive-note-pool": "extensive-a3-dock-2", "a3-extensive-exit": "extensive-a3-exit",
    "a3-extensive-dialogue": "extensive-a3-dialogue-controller-2", "a3-extensive-tooltip": "extensive-a3-tooltip-controller", "a3-extensive-journal": "extensive-a3-journal-note",
}
# slots cut from other slots, so a retake reproduces them: name -> (source slot, (left, top, right, bottom))
CROPS = {
    # the popup at a size a phone can read, tall enough for Extensive's second note
    **{f"hero-note-{t}": (f"hero-{t}", (130, 86, 720, 906)) for t in ("minimal", "normal", "extensive")},
    # the tier comparisons without their baked-in labels, so each panel can stand alone at phone width
    **{f"note-{t}": ("compare-notes", (16 + 646 * k, 60, 646 + 646 * k, 430)) for k, t in enumerate(("minimal", "normal", "extensive"))},
    **{f"tooltip-{t}": ("compare-tooltips", (16 + 536 * k, 60, 536 + 536 * k, 790)) for k, t in enumerate(("normal", "extensive"))},
    # the Normal archive note at a size a phone can read. Extensive's stays a full frame: its detail is a choice.
    "journal-note-normal": ("a1-normal-journal", (990, 205, 1610, 495)),
    # small proofs on the home page
    "proof-first": ("a1-normal-welcome", (50, 60, 810, 600)),
    "proof-first-note": ("a1-normal-welcome", (104, 104, 540, 520)),
    "proof-word": ("compare-tooltips", (30, 590, 370, 721)),
    "proof-pin": ("pin-before", (246, 72, 586, 203)),
    **{f"party-{k + 1}": ("hero-normal", (16, y, 114, y + 143)) for k, y in enumerate((436, 581, 724, 866))},
    # where the two map tiers differ
    "map-top-normal": ("a1-normal-map", (420, 98, 1200, 628)),
    "map-top-extensive": ("a1-extensive-map", (420, 98, 1200, 628)),
    # the mod's own icons, for the key in the docs
    "icon-arrow": ("hero-extensive", (214, 176, 252, 214)),
    "icon-mark": ("hero-extensive", (208, 271, 244, 307)),
    "icon-star": ("hero-extensive", (212, 710, 250, 748)),
    "icon-die": ("hero-extensive", (208, 618, 246, 656)),
    "icon-skull": ("a1-extensive-welcome", (345, 258, 371, 284)),
    "icon-party": ("a1-extensive-journal", (1020, 396, 1052, 428)),
    "icon-chest": ("a1-extensive-journal", (1021, 674, 1053, 706)),
}
WIDTHS = (480, 800, 1280, 1920)  # build.py asks for the same sizes, and 1600 for the home page's scenes


def widths(name, w):
    extra = (1600,) if name in ("hero-minimal", "hero-normal", "hero-extensive") else ()
    return [x for x in sorted(WIDTHS + extra) if x < w] + [min(w, WIDTHS[-1])]


def captures(src):
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
    compare("notes-act3", list(zip(T, ("minimal-a3-koll-2", "normal-a3-koll-2", "extensive-a3-koll-2"))), (130, 130, 760, 660))
    compare("quest-lines", list(zip(T, ("minimal-a3-quest-urgency", "normal-a1-quest", "extensive-a1-quest"))), (1240, 270, 2400, 760))
    compare("dialogue", list(zip(T, ("minimal-a3-dialogue-notag", "normal-a3-dialogue-controller", "extensive-a3-dialogue-controller"))), (360, 960, 2240, 1400), stack=True)
    compare("tooltips", list(zip(T[1:], ("normal-a3-tooltip-controller", "extensive-a3-tooltip-controller"))), (1710, 560, 2230, 1290))
    compare("map-pins", list(zip(T[1:], ("normal-a1-map", "extensive-a1-map"))), (500, 80, 2200, 1390))
    for p in (out / "t").glob("*.jpg"):  # new captures mean new thumbnails
        p.unlink()


def derive():
    for new, (slot, box) in CROPS.items():
        Image.open(out / f"{slot}.jpg").convert("RGB").crop(box).save(out / f"{new}.jpg", quality=88, optimize=True, progressive=True)
        (out / "t" / f"{new}.jpg").unlink(missing_ok=True)
    sizes, keep = {}, set()
    for p in sorted(out.glob("*.jpg")):
        im = Image.open(p).convert("RGB")
        sizes[p.stem] = im.size
        thumb = out / "t" / p.name
        if not thumb.exists():
            (im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS) if im.width > 800 else im).save(thumb, quality=72, optimize=True, progressive=True)
        for w in widths(p.stem, im.width):
            webp = out / "w" / f"{p.stem}-{w}.webp"
            keep.add(webp)
            if not webp.exists() or webp.stat().st_mtime < p.stat().st_mtime:
                (im.resize((w, round(im.height * w / im.width)), Image.LANCZOS) if w < im.width else im).save(webp, quality=74, method=6)
    for stale in set((out / "w").glob("*.webp")) - keep:
        stale.unlink()
    (root / "src" / "sizes.json").write_text(json.dumps(sizes))
    print(len(sizes), "images")


if sys.argv[1] != "--derive":
    captures(Path(sys.argv[1]))
derive()
