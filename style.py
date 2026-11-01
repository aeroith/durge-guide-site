#!/usr/bin/env python3
# Measures the site's copy against STYLE.md. Fails on what the game never does; prints sentence lengths for the rest.
import html, re, sys
from pathlib import Path

AMERICAN = r"\b(color|armor|honor|favor|recognize|realize|meter|meters|traveling|dialog|license|licenses|gray|center)\b"
PLAIN = {"how-it-works", "credits"}  # these pages are allowed to run long, see STYLE.md


def sentences(page):
    body = re.sub(r"<!--.*?-->|\[\[(?:shot|gate) [^|]*\|[^|]*\|?|<pre>.*?</pre>|<code>.*?</code>", " ", page, flags=re.S)
    text = re.findall(r"<(p|li|h3)(?: [^>]*)?>(.*?)</\1>", body, flags=re.S)
    return [s for _, t in text for s in re.split(r"(?<=[.!?'])\s+", html.unescape(re.sub(r"<[^>]+>", "", t)).strip()) if len(s.split()) > 1]


bad = []
for p in sorted(Path("src/pages").glob("*.html")):
    raw = p.read_text()
    s = sentences(raw)
    lens = sorted(len(x.split()) for x in s)
    median, p90 = lens[len(lens) // 2], lens[len(lens) * 9 // 10]
    print(f"{p.stem:15} {len(s):3} sentences, median {median:2}, longest 10% from {p90:2}")
    text = " ".join(s)
    for pattern, what in ((r";", "semicolon"), (r"—|–", "em or en dash"), (r"!", "exclamation mark"), (AMERICAN, "American spelling"), (r"\bGuide (pick|line)\b", "old label")):
        for m in re.finditer(pattern, text):
            bad.append(f"{p.stem}: {what}: ...{text[max(0, m.start() - 40):m.end() + 20]}...")
    if p.stem not in PLAIN and (median > 13 or p90 > 23):
        bad.append(f"{p.stem}: sentences run long (median {median}, longest 10% from {p90})")
print("\n".join(bad) or "ok")
sys.exit(1 if bad else 0)
