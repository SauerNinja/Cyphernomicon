#!/usr/bin/env python3
import json, os, html

SITE = "/home/claude/work/site"
CHAP = os.path.join(SITE, "chapters")
BUILD = "/home/claude/work/build"
os.makedirs(CHAP, exist_ok=True)

SECTIONS = json.load(open(os.path.join(SITE, "assets/data/sections.json")))
BODIES = {}
for s in SECTIONS:
    BODIES[s["slug"]] = open(os.path.join(BUILD, "rendered", f'{s["slug"]}.html'), encoding="utf-8").read()

def esc(s):
    return html.escape(s, quote=False)

# ---------------------------------------------------------------------------
# Shared fragments
# ---------------------------------------------------------------------------

def sidebar_html(root, active_slug=None):
    items = []
    for s in SECTIONS:
        num = s["slug"].split("-")[0]
        cls = "active" if s["slug"] == active_slug else ""
        items.append(
            f'<li><a href="{root}chapters/{s["slug"]}.html" data-section="{s["slug"]}" class="{cls}">'
            f'<span class="n">{num}</span><span>{esc(s["title"])}</span></a></li>'
        )
    return f'''
  <nav class="sidebar" aria-label="Table of contents">
    <a class="sidebar__brand" href="{root}index.html">
      <span class="title">THE CYPHERNOMICON</span>
      <span class="sub">Interactive Edition · v0.666+</span>
    </a>
    <button class="sidebar__search" data-action="open-search" type="button">
      <span>Search all 20 sections…</span>
      <kbd>⌘K</kbd>
    </button>
    <ul class="sidebar__nav">
      <li><a href="{root}index.html" class="{'active' if active_slug is None else ''}"><span class="n">00</span><span>Foreword &amp; Cover Sheet</span></a></li>
      {''.join(items)}
    </ul>
    <div class="sidebar__foot">
      Original text © 1994 Timothy C. May.<br>
      Interactive edition code, design &amp; foreword © 2026 Setvin Noether, MIT Licensed.<br>
      <a href="https://github.com/SauerNinja/Cyphernomicon">View source on GitHub ↗</a>
    </div>
  </nav>'''

def search_overlay_html():
    return '''
  <div class="search-overlay" id="search-overlay" role="dialog" aria-modal="true" aria-label="Search the Cyphernomicon">
    <div class="search-panel">
      <div class="search-panel__input-row">
        <span aria-hidden="true">⌕</span>
        <input id="search-input" type="text" placeholder="Search 3,800+ passages…" autocomplete="off" spellcheck="false">
        <span class="esc">ESC</span>
      </div>
      <div class="search-panel__results" id="search-results">
        <div class="search-empty">Type at least 2 characters — searches all 20 sections.</div>
      </div>
    </div>
  </div>'''

def masthead_html(root, title):
    return f'''
  <header class="masthead">
    <button class="masthead__btn nav-toggle" type="button" aria-label="Toggle table of contents">☰ Contents</button>
    <a class="masthead__brand" href="{root}index.html"><span class="dot">◆</span> Cyphernomicon</a>
    <div class="masthead__spacer"></div>
    <button class="masthead__btn" data-action="open-search" type="button">⌕ Search</button>
  </header>'''

def head_html(root, title, desc):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}assets/css/style.css">
</head>'''

def page_wrap(root, active_slug, title, desc, body_html):
    return f'''{head_html(root, title, desc)}
<body data-root="{root}" data-section="{active_slug or ''}">
<a class="skip-link" href="#main">Skip to content</a>
{masthead_html(root, title)}
<div class="sidebar-scrim"></div>
<div class="shell">
{sidebar_html(root, active_slug)}
<main id="main">
<div class="content">
{body_html}
</div>
</main>
</div>
{search_overlay_html()}
<script src="{root}assets/js/site.js"></script>
</body>
</html>'''

# ---------------------------------------------------------------------------
# Index page
# ---------------------------------------------------------------------------

FOREWORD = open(os.path.join(BUILD, "foreword.html"), encoding="utf-8").read()

toc_cards = []
for s in SECTIONS:
    num = s["slug"].split("-")[0]
    toc_cards.append(f'''
    <a class="toc-card" href="chapters/{s["slug"]}.html">
      <span class="num">§{num}</span>
      <span class="name">{esc(s["title"])}</span>
      <span class="meta">{esc(s["desc"])}</span>
    </a>''')

index_body = f'''
<div class="hero">
  <div class="hero__eyebrow">Cypherpunks FAQ &amp; More · Est. 1994</div>
  <h1>The Cyphernomicon<span class="accent">.</span></h1>
  <p class="hero__dek">Timothy C. May's sprawling, unfinished manifesto-FAQ of the Cypherpunks
  mailing list — 20 sections, ~700 questions, and the clearest statement anyone wrote of what
  strong cryptography would do to states, money, and identity. This edition makes the outline
  navigable, searchable, and readable end to end.</p>
  <div class="hero__actions">
    <a class="btn btn--solid" href="chapters/01-Introduction.html">Begin reading →</a>
    <a class="btn" data-action="open-search" href="#" onclick="return false;">Search the text</a>
    <a class="btn" href="https://github.com/SauerNinja/Cyphernomicon">Source on GitHub</a>
  </div>

  <div class="headerblock">
    <div class="field"><span class="k">From</span><span class="v">tcmay@netcom.com (Timothy C. May)</span></div>
    <div class="field"><span class="k">Subject</span><span class="v">THE CYPHERNOMICON: Cypherpunks FAQ and More</span></div>
    <div class="field"><span class="k">Version</span><span class="v dim">0.666, 1994-09-10 — reproduced in full below</span></div>
    <div class="field"><span class="k">Status</span><span class="v dim">Historical document · reformatted, not rewritten</span></div>
  </div>
</div>

<div class="foreword">
  <div class="foreword__byline">Foreword to the Interactive Edition — <strong>Setvin Noether</strong> (SauerNinja), 2026</div>
  {FOREWORD}
</div>

<div class="notice">
  <strong>On the text and the license.</strong> The original Cyphernomicon is copyright
  Timothy C. May (1994) and is reproduced here for historical and educational reference, in the
  same spirit every prior mirror has reproduced it — his own README asks only that readers
  "don't put your name on my words." The code, layout, search, and this foreword are original
  work by Setvin Noether and are MIT licensed; see <a href="https://github.com/SauerNinja/Cyphernomicon/blob/main/LICENSE">LICENSE</a>
  and <a href="https://github.com/SauerNinja/Cyphernomicon/blob/main/NOTICE.md">NOTICE.md</a> for the full breakdown.
</div>

<h2 style="font-size:1rem; letter-spacing:.06em; text-transform:uppercase; color:var(--ink-faint); margin: 2.5rem 0 0.5rem;">Table of Contents</h2>
<div class="toc-grid">
  {''.join(toc_cards)}
</div>

<footer class="site-footer">
  <div>THE CYPHERNOMICON — interactive edition. Original text © 1994 Timothy C. May, reproduced for
  historical/educational reference. Interactive edition (code, design, foreword) © 2026 Setvin Noether — MIT License.</div>
</footer>
'''

with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
    f.write(page_wrap("", None, "The Cyphernomicon — Interactive Edition", "An interactive, searchable edition of Timothy C. May's 1994 Cypherpunks FAQ, with a foreword by Setvin Noether.", index_body))

# ---------------------------------------------------------------------------
# Chapter pages
# ---------------------------------------------------------------------------

for i, s in enumerate(SECTIONS):
    slug, title, desc = s["slug"], s["title"], s["desc"]
    num = slug.split("-")[0]
    prev_s = SECTIONS[i - 1] if i > 0 else None
    next_s = SECTIONS[i + 1] if i < len(SECTIONS) - 1 else None

    pager_bits = []
    if prev_s:
        pager_bits.append(f'<a class="prev" href="{prev_s["slug"]}.html"><span class="lbl">← Previous</span>§{prev_s["slug"].split("-")[0]} {esc(prev_s["title"])}</a>')
    else:
        pager_bits.append('<a class="prev" href="../index.html"><span class="lbl">← Back</span>Cover &amp; Foreword</a>')
    if next_s:
        pager_bits.append(f'<a class="next" href="{next_s["slug"]}.html"><span class="lbl">Next →</span>§{next_s["slug"].split("-")[0]} {esc(next_s["title"])}</a>')
    else:
        pager_bits.append('<a class="next" href="../index.html"><span class="lbl">End →</span>Back to cover sheet</a>')

    body = f'''
<div class="chapter-head">
  <div class="num">§{num} / 20</div>
  <h1>{esc(title)}</h1>
</div>
<div class="chapter-toolbar">
  <button class="chapter-toolbar__btn" data-action="expand-all" type="button">Expand all</button>
  <button class="chapter-toolbar__btn" data-action="collapse-all" type="button">Collapse to headings</button>
  <span class="chapter-toolbar__sep">·</span>
  <button class="chapter-toolbar__btn" data-action="open-search" type="button">⌕ Search this document</button>
</div>
{BODIES[slug]}
<nav class="chapter-pager">{''.join(pager_bits)}</nav>
'''
    with open(os.path.join(CHAP, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(page_wrap("../", slug, f"§{num} {title} — The Cyphernomicon", desc, body))

print("Wrote index.html and", len(SECTIONS), "chapter pages")
