#!/usr/bin/env python3
# Builds the site into docs/, which GitHub Pages serves. Stdlib only. usage: python3 build.py
# Pages are src/pages/*.html. The first line is <!-- title | description | section -->, and these shortcuts expand:
#   [[shot name | alt | caption | pan:900]]     a screenshot that links to its full size. "pan:900" shows a very wide one 900px wide on a phone, scrolling sideways.
#   [[split name | alt | caption]]              the same, for one that shares its row with words
#   [[gate reason | name | alt | caption]]      the same, hidden behind a spoiler seal
#   [[row 2]] ... [[/row]]                      shots and gates side by side, 2 or 3 to a row (2s when the row sits in a narrow column)
#   [[wipe label]] ... [[/wipe]]                two aligned shots, side by side. site.js turns them into one with a sliding divide.
#   [[summary reason | action]]                 a spoiler seal for a hand-written <details class="gate">
#   [[hero tier | alt | caption]]               one tier's scene in the home page's switch
#   [[art name | phone-crop | alt | caption]]   a screenshot with a tighter crop for phones
#   [[icon name]]                               one of the mod's icons, cut from a screenshot. The words beside it carry the meaning.
import html, json, re, shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC, OUT = ROOT / "src", ROOT / "docs"
SIZES = json.loads((SRC / "sizes.json").read_text())
MAIN = [("tiers", "Tiers"), ("in-game", "In the game"), ("screenshots", "Screenshots"), ("install", "Docs")]
DOCS = [("install", "Install"), ("using", "Using it"), ("compatibility", "Compatibility"), ("how-it-works", "How it works"), ("faq", "FAQ"), ("credits", "Credits")]
WIDTHS = (480, 800, 1280, 1920)  # images.py makes the same sizes
FULL = "(max-width: 1272px) 100vw, 1240px"
ACROSS = {"2": "(max-width: 640px) 100vw, (max-width: 1272px) 50vw, 620px", "3": "(max-width: 640px) 100vw, (max-width: 1272px) 33vw, 410px"}
SIDE = "(max-width: 900px) 100vw, (max-width: 1272px) 62vw, 760px"
SITE = "/durge-guide-site/"


def webp(name):
    w = SIZES[name][0]
    extra = (1600,) if name in ("hero-minimal", "hero-normal", "hero-extensive") else ()
    return ", ".join(f"img/w/{name}-{x}.webp {x}w" for x in [x for x in sorted(WIDTHS + extra) if x < w] + [min(w, WIDTHS[-1])])


def shot(name, alt, caption="", flags="", sizes=FULL):
    w, h = SIZES[name]
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    img = (f'<picture><source type="image/webp" srcset="{webp(name)}" sizes="{sizes}">'
           f'<img src="img/t/{name}.jpg" sizes="{sizes}" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{html.escape(alt, quote=True)}"></picture>')
    link = f'<a href="img/{name}.jpg">{img}</a>'
    if flags.startswith("pan:"):  # the frame scrolls, so a keyboard has to be able to reach it
        link = f'<div class="pan" style="--pan:{flags[4:]}px" tabindex="0" role="group" aria-label="Scroll sideways to see all of it">{link}</div>'
    return f'<figure class="shot">{link}{cap}</figure>'


def seal(reason, action):
    return (f'<summary><span class="seal"></span><span class="why"><span class="hid">Hidden: </span>{reason}</span>'
            f'<span class="show">{action}</span><span class="hide">Hide</span></summary>')


def gate(reason, name, alt, caption="", flags="", sizes=FULL):
    return f'<details class="gate">{seal(reason, "Show screenshot")}<div class="gate-body">{shot(name, alt, caption, flags, sizes)}</div></details>'


def art(name, crop, alt, caption):
    """The same shot, cropped in for a phone, so its words can be read there."""
    source = (f'<source media="(max-width: 640px)" type="image/webp" srcset="{webp(crop)}" sizes="100vw" width="{SIZES[crop][0]}" height="{SIZES[crop][1]}">')
    return shot(name, alt, caption, sizes=SIDE).replace("<picture>", f"<picture>{source}").replace('class="shot"', 'class="shot art"')


def hero(tier, alt, caption):
    full, note = f"hero-{tier}", f"hero-note-{tier}"
    w, h = SIZES[full]
    first = tier == "normal"
    load = 'fetchpriority="high"' if first else 'loading="lazy"'
    return (f'<a class="{tier}" href="img/{full}.jpg" data-caption="{html.escape(caption, quote=True)}"><picture>'
            f'<source media="(max-width: 640px)" type="image/webp" srcset="{webp(note)}" sizes="100vw" width="{SIZES[note][0]}" height="{SIZES[note][1]}">'
            f'<source type="image/webp" srcset="{webp(full)}" sizes="100vw" width="{w}" height="{h}">'
            f'<img src="img/t/{full}.jpg" width="{w}" height="{h}" {load} decoding="async" alt="{html.escape(alt, quote=True)}"></picture></a>')


def expand(body):
    def parts(m):
        return [p.strip() for p in m[1].split("|")]

    def row(m):
        sizes = "(max-width: 640px) 100vw, 240px" if m[2] else ACROSS[m[1]]  # "2s": side by side in a narrow column
        inner = re.sub(r"\[\[shot ([^\]]+)\]\]", lambda g: shot(*parts(g), sizes=sizes), m[3])
        inner = re.sub(r"\[\[gate ([^\]]+)\]\]", lambda g: gate(*parts(g), sizes=sizes), inner)
        return f'<div class="row n{m[1]}">{inner}</div>'

    def wipe(m):
        inner = re.sub(r"\[\[shot ([^\]]+)\]\]", lambda g: shot(*parts(g), sizes=ACROSS["2"]), m[2])
        return f'<div class="row n2" data-wipe="{html.escape(m[1].strip(), quote=True)}">{inner}</div>'

    body = re.sub(r"\[\[wipe ([^\]]+)\]\](.*?)\[\[/wipe\]\]", wipe, body, flags=re.S)
    body = re.sub(r"\[\[row (\d)(s?)\]\](.*?)\[\[/row\]\]", row, body, flags=re.S)
    body = re.sub(r"\[\[split ([^\]]+)\]\]", lambda m: shot(*parts(m), sizes=SIDE), body)
    body = re.sub(r"\[\[shot ([^\]]+)\]\]", lambda m: shot(*parts(m)), body)
    body = re.sub(r"\[\[gate ([^\]]+)\]\]", lambda m: gate(*parts(m)), body)
    body = re.sub(r"\[\[summary ([^\]]+)\]\]", lambda m: seal(*parts(m)), body)
    body = re.sub(r"\[\[hero ([^\]]+)\]\]", lambda m: hero(*parts(m)), body)
    body = re.sub(r"\[\[art ([^\]]+)\]\]", lambda m: art(*parts(m)), body)
    return re.sub(r"\[\[icon ([a-z-]+)\]\]", lambda m: f'<img class="icon" src="img/icon-{m[1]}.jpg" width="{SIZES["icon-" + m[1]][0]}" height="{SIZES["icon-" + m[1]][1]}" alt="" loading="lazy">', body)


def links(items, current):
    return "".join(f'<a href="{n}.html"{" aria-current=page" if n == current else ""}>{label}</a>' for n, label in items)


def contents(body):
    """Gives each h2 an id, and returns the page's contents. Docs pages get theirs beside the text."""
    found = []

    def slug(m):
        text = html.unescape(re.sub(r"<[^>]+>", "", m[1]))
        found.append((re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-"), m[1]))
        return f'<h2 id="{found[-1][0]}">{m[1]}</h2>'

    return re.sub(r"<h2>(.*?)</h2>", slug, body), found


def pager(name):
    names = [n for n, _ in DOCS]
    k = names.index(name)
    prev = f'<a class="prev" href="{DOCS[k - 1][0]}.html" rel="prev">{DOCS[k - 1][1]}</a>' if k else ""
    next_ = f'<a class="next" href="{DOCS[k + 1][0]}.html" rel="next">{DOCS[k + 1][1]}</a>' if k + 1 < len(DOCS) else ""
    return f'<nav class="pager" aria-label="Previous and next">{prev}{next_}</nav>'


def preload():
    """The hero's first image, found before the stylesheet is parsed."""
    return "".join(f'<link rel="preload" as="image" type="image/webp" imagesrcset="{webp(n)}" imagesizes="100vw" media="{q}" fetchpriority="high">\n'
                   for n, q in (("hero-note-normal", "(max-width: 640px)"), ("hero-normal", "(min-width: 641px)")))


def page(path, layout):
    title, desc, section = [s.strip() for s in re.match(r"<!--(.*?)-->", path.read_text(), re.S)[1].split("|")]
    body = expand(path.read_text().split("-->", 1)[1])
    name = path.stem
    current = "install" if section == "docs" else name
    if section == "docs":
        body, found = contents(body)
        toc = "".join(f'<a href="#{i}">{t}</a>' for i, t in found)
        toc = f'<nav class="toc" aria-label="On this page"><p>On this page</p>{toc}</nav>' if len(found) > 2 else ""
        body = (f'<div class="docs"><nav class="docs-nav strip" aria-label="Docs">{links(DOCS, name)}</nav>'
                f'<article class="prose">{body}{pager(name)}</article>{toc}</div>')
    missing = name == "404"
    text = (layout.replace("{title}", title if name == "index" else f"{title}: Durge Guide").replace("{desc}", html.escape(desc, quote=True))
            .replace("{path}", "" if name == "index" or missing else f"{name}.html")
            .replace("{head}", preload() if name == "index" else "")
            .replace("{bodyclass}", f"on-{section}")
            .replace("{nav}", links(MAIN, current)).replace("{footnav}", links(MAIN, "")).replace("{body}", body))
    # GitHub serves the 404 at any depth, so its links can't be relative
    return re.sub(r'(href|src)="(?!https?:|data:|#)', rf'\1="{SITE}', text) if missing else text


def check():
    """Every local link, image and font points at something that exists, every #anchor is on its page, and nothing private is published."""
    pages = {p.name: p.read_text() for p in OUT.glob("*.html")}
    bad = []
    for name, text in pages.items():
        for ref in re.findall(r'(?:href|src)="([^"]+)"', text) + [u.split()[0] for s in re.findall(r'srcset="([^"]+)"', text) for u in s.split(", ")]:
            if re.match(r"https?:|mailto:|data:", ref):
                continue
            file, _, anchor = ref.removeprefix(SITE).partition("#")
            target = file or name
            if not (OUT / target).exists():
                bad.append(f"{name}: {ref}")
            elif anchor and f'id="{anchor}"' not in pages.get(target, ""):
                bad.append(f"{name}: {ref} (no such anchor)")
        if "[[" in text:
            bad.append(f"{name}: unexpanded shortcut")
    for ref in re.findall(r'url\("?((?!data:)[^")]+)"?\)', (OUT / "style.css").read_text()):
        if not (OUT / ref).exists():
            bad.append(f"style.css: {ref}")
    for private in ("PRODUCT.md", "DESIGN.md", "STYLE.md", ".impeccable"):
        if (OUT / private).exists():
            bad.append(f"{private} must not be published")
    assert not bad, "\n".join(bad)
    print(f"{len(pages)} pages, all links and images found")


def main():
    for old in OUT.glob("*.html"):  # docs/img stays: images.py owns it
        old.unlink()
    layout = (SRC / "layout.html").read_text()
    for p in sorted((SRC / "pages").glob("*.html")):
        (OUT / p.name).write_text(page(p, layout))
    for f in ("style.css", "print.css", "site.js"):
        shutil.copy(SRC / f, OUT)
    shutil.copytree(SRC / "fonts", OUT / "fonts", dirs_exist_ok=True)
    (OUT / ".nojekyll").touch()
    check()


if __name__ == "__main__":
    main()
