#!/usr/bin/env python3
# Builds the site into docs/, which GitHub Pages serves. Stdlib only. usage: python3 build.py
# Pages are src/pages/*.html. The first line is <!-- title | description | section -->, and these shortcuts expand:
#   [[shot name | alt | caption]]               a screenshot that links to its full size
#   [[gate reason | name | alt | caption]]      the same, hidden behind a spoiler bar
#   [[grid]] ... [[/grid]]                      a gallery of shots
import html, json, re, shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC, OUT = ROOT / "src", ROOT / "docs"
SIZES = json.loads((SRC / "sizes.json").read_text())
MAIN = [("tiers", "Tiers"), ("in-game", "In the game"), ("screenshots", "Screenshots"), ("install", "Docs")]
DOCS = [("install", "Install"), ("using", "Using it"), ("compatibility", "Compatibility"), ("how-it-works", "How it works"), ("faq", "FAQ"), ("credits", "Credits")]


def shot(name, alt, caption, sizes="(max-width: 900px) 100vw, 1000px"):
    w, h = SIZES[name]
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return (f'<figure class="shot"><a href="img/{name}.jpg"><img src="img/t/{name}.jpg" srcset="img/t/{name}.jpg 800w, img/{name}.jpg {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" loading="lazy" alt="{html.escape(alt, quote=True)}"></a>{cap}</figure>')


def expand(body):
    def parts(m):
        return [p.strip() for p in m[1].split("|")]

    def grid(m):
        return '<div class="grid">' + re.sub(r"\[\[shot ([^\]]+)\]\]", lambda g: shot(*parts(g), sizes="(max-width: 640px) 100vw, 360px"), m[1]) + "</div>"

    body = re.sub(r"\[\[grid\]\](.*?)\[\[/grid\]\]", grid, body, flags=re.S)
    body = re.sub(r"\[\[shot ([^\]]+)\]\]", lambda m: shot(*parts(m)), body)

    def gate(m):
        reason, *rest = parts(m)
        return f'<details class="gate"><summary><span>Hidden: {reason}</span><span class="show">Show screenshot</span></summary>{shot(*rest)}</details>'

    return re.sub(r"\[\[gate ([^\]]+)\]\]", gate, body)


def links(items, current):
    return "".join(f'<a href="{n}.html"{" aria-current=page" if n == current else ""}>{label}</a>' for n, label in items)


def page(path, layout):
    title, desc, section = [s.strip() for s in re.match(r"<!--(.*?)-->", path.read_text(), re.S)[1].split("|")]
    body = expand(path.read_text().split("-->", 1)[1])
    name = path.stem
    current = "install" if section == "docs" else name
    if section == "docs":
        body = f'<div class="docs"><nav class="docs-nav" aria-label="Docs">{links(DOCS, name)}</nav><article class="prose">{body}</article></div>'
    return (layout.replace("{title}", title if name == "index" else f"{title}: Durge Guide").replace("{desc}", html.escape(desc, quote=True))
            .replace("{nav}", links(MAIN, current)).replace("{body}", body))


def check():
    """Every local link and image points at something that exists, and every #anchor is on its page."""
    pages = {p.name: p.read_text() for p in OUT.glob("*.html")}
    bad = []
    for name, text in pages.items():
        for ref in re.findall(r'(?:href|src)="([^"]+)"', text) + [u.split()[0] for s in re.findall(r'srcset="([^"]+)"', text) for u in s.split(", ")]:
            if re.match(r"https?:|mailto:|data:", ref):
                continue
            file, _, anchor = ref.partition("#")
            target = file or name
            if not (OUT / target).exists():
                bad.append(f"{name}: {ref}")
            elif anchor and f'id="{anchor}"' not in pages.get(target, ""):
                bad.append(f"{name}: {ref} (no such anchor)")
        if "[[" in text:
            bad.append(f"{name}: unexpanded shortcut")
    assert not bad, "\n".join(bad)
    print(f"{len(pages)} pages, all links and images found")


def main():
    for old in OUT.glob("*.html"):  # docs/img stays: images.py owns it
        old.unlink()
    layout = (SRC / "layout.html").read_text()
    for p in sorted((SRC / "pages").glob("*.html")):
        (OUT / p.name).write_text(page(p, layout))
    shutil.copy(SRC / "style.css", OUT)
    (OUT / ".nojekyll").touch()
    check()


if __name__ == "__main__":
    main()
