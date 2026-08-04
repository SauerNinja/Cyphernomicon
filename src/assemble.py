#!/usr/bin/env python3
import json, os, html

SITE = "/home/claude/work/site"
CHAP = os.path.join(SITE, "chapters")
BUILD = "/home/claude/work/build"
os.makedirs(CHAP, exist_ok=True)

BASE_URL = "https://sauerninja.github.io/Cyphernomicon"
GA_ID = "G-MWKBNFBLHE"

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
    <button class="sidebar__collapse-bar" data-action="collapse-nav" type="button" aria-label="Collapse contents panel">
      <span class="arrows">«</span><span>Collapse panel</span>
    </button>
    <div class="sidebar__head">
      <a class="sidebar__brand" href="{root}index.html">
        <span class="title">THE CYPHERNOMICON</span>
        <span class="sub">Interactive Edition · v0.666+</span>
      </a>
    </div>
    <button class="sidebar__search" data-action="open-search" type="button">
      <span>Search all 20 sections…</span>
      <kbd>⌘K</kbd>
    </button>
    <ul class="sidebar__nav">
      <li><a href="{root}index.html" class="{'active' if active_slug is None else ''}"><span class="n">00</span><span>Foreword &amp; Cover Sheet</span></a></li>
      <li><a href="{root}about-tim-may.html" data-section="about-tim-may" class="{'active' if active_slug == 'about-tim-may' else ''}"><span class="n">★</span><span>About Tim May</span></a></li>
      {''.join(items)}
    </ul>
    <div class="sidebar__foot">
      Original text © 1994 Timothy C. May.<br>
      Interactive edition code, design &amp; foreword © 2026 Setvin Noether, MIT Licensed.<br>
      <a href="https://github.com/SauerNinja/Cyphernomicon">View source on GitHub ↗</a>
    </div>
  </nav>
  <button class="sidebar-reopen" data-action="expand-nav" type="button" aria-label="Show contents panel">
    <span class="arrows">»</span><span>Contents</span>
  </button>'''

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
    # Mobile-only floating toggle — replaces the old full-width top bar.
    # The sidebar itself (always visible on desktop) covers brand + search + nav.
    return f'''
  <button class="mobile-nav-toggle nav-toggle" type="button" aria-label="Toggle contents panel">☰</button>'''

def consent_and_ga_html():
    return f'''
<!-- Google Analytics 4 (gtag.js), Consent Mode v2 default: granted -->
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{ dataLayer.push(arguments); }}
  gtag('consent', 'default', {{
    'ad_storage': 'granted',
    'analytics_storage': 'granted',
    'ad_user_data': 'granted',
    'ad_personalization': 'granted'
  }});
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'''

def consent_banner_html():
    return '''
  <div class="consent-banner" id="consent-banner" role="dialog" aria-label="Cookie notice">
    <p>This site uses Google Analytics to see which sections get read. No accounts, no ad network, nothing sold.</p>
    <div class="consent-banner__actions">
      <button type="button" data-consent="accept">OK</button>
      <button type="button" data-consent="reject">Opt out</button>
    </div>
  </div>'''

def head_html(root, title, desc, canonical_path, og_type="website", og_image=None, keywords=None):
    canonical = f"{BASE_URL}/{canonical_path}".rstrip("/") if canonical_path else BASE_URL + "/"
    if canonical_path == "index.html":
        canonical = BASE_URL + "/"
    img = og_image or f"{BASE_URL}/assets/og-image.jpg"
    kw = keywords or "cyphernomicon, cypherpunks, tim may, crypto anarchy, cryptography faq, pgp, digital cash, bitcoin history, anonymity, remailers, satoshi nakamoto"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(kw)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Setvin Noether">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#060605">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://www.googletagmanager.com">

<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="The Cyphernomicon — Interactive Edition">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="The Cyphernomicon, bound as a leather volume">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{img}">

<link rel="icon" href="{root}assets/favicon-32x32.png" sizes="32x32" type="image/png">
<link rel="icon" href="{root}assets/favicon-16x16.png" sizes="16x16" type="image/png">
<link rel="icon" href="{root}assets/icon-512.png" sizes="512x512" type="image/png">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<link rel="manifest" href="{root}assets/site.webmanifest">
<link rel="stylesheet" href="{root}assets/css/style.css">
{consent_and_ga_html()}
</head>'''

def page_wrap(root, active_slug, title, desc, body_html, canonical_path="", og_type="website", jsonld="", keywords=None):
    return f'''{head_html(root, title, desc, canonical_path, og_type, keywords=keywords)}
<body data-root="{root}" data-section="{active_slug or ''}">
<script>if(localStorage.getItem("cyphernomicon-nav")==="collapsed")document.body.classList.add("nav-collapsed");</script>
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
{consent_banner_html()}
{jsonld}
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
  <div class="hero__figure">
    <img src="assets/images/cyphernomicon-cover.jpg" alt="The Cyphernomicon, styled as a leather-bound volume" width="530" height="599" loading="eager">
    <div class="cap"><span>Interactive Edition — 2026</span><span>Fig. 0.1</span></div>
  </div>

  <div class="hero__eyebrow">Cypherpunks FAQ &amp; More · Est. 1994</div>
  <h1>The Cyphernomicon<span class="accent">.</span></h1>
  <p class="hero__dek">Timothy C. May's sprawling, unfinished manifesto-FAQ of the Cypherpunks
  mailing list — 20 sections, ~700 questions, and the clearest statement anyone wrote of what
  strong cryptography would do to states, money, and identity. This edition makes the outline
  navigable, searchable, and readable end to end.</p>
  <div class="hero__actions">
    <a class="btn btn--solid" href="#chapter-start">Begin reading →</a>
    <a class="btn" data-action="open-search" href="#" onclick="return false;">Search the text</a>
    <a class="btn" href="about-tim-may.html">About Tim May</a>
    <a class="btn" href="https://github.com/SauerNinja/Cyphernomicon">Source on GitHub</a>
  </div>

  <div class="headerblock headerblock--centered">
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
  work by Setvin Noether and are MIT licensed; see <a href="https://github.com/SauerNinja/Cyphernomicon/blob/master/LICENSE">LICENSE</a>
  and <a href="https://github.com/SauerNinja/Cyphernomicon/blob/master/NOTICE.md">NOTICE.md</a> for the full breakdown.
</div>

<div id="chapter-start" style="scroll-margin-top:1.5rem;">
<div class="chapter-head" style="margin-top:3rem;">
  <div class="num">§01 / 20</div>
  <h2 style="font-family:var(--font-mono); font-size:clamp(1.6rem,4vw,2.2rem); margin:0.3rem 0 0; font-weight:600;">Introduction</h2>
</div>
<div class="chapter-toolbar">
  <button class="chapter-toolbar__btn" data-action="expand-all" type="button">Expand all</button>
  <button class="chapter-toolbar__btn" data-action="collapse-all" type="button">Collapse to headings</button>
  <span class="chapter-toolbar__sep">·</span>
  <button class="chapter-toolbar__btn" data-action="open-search" type="button">⌕ Search this document</button>
</div>
{BODIES["01-Introduction"]}
<nav class="chapter-pager">
  <a class="prev" href="#main" onclick="window.scrollTo({{top:0,behavior:'smooth'}});return false;"><span class="lbl">↑ Back to</span>Cover &amp; Foreword</a>
  <a class="next" href="chapters/02-MFAQ.html"><span class="lbl">Next →</span>§02 Most Frequently Asked Questions</a>
</nav>
</div>

<footer class="site-footer">
  <div>THE CYPHERNOMICON — interactive edition. Original text © 1994 Timothy C. May, reproduced for
  historical/educational reference. Interactive edition (code, design, foreword) © 2026 Setvin Noether — MIT License.</div>
</footer>
'''

index_jsonld = f'''
<script type="application/ld+json">
{json.dumps({
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": BASE_URL + "/#website",
      "name": "The Cyphernomicon — Interactive Edition",
      "url": BASE_URL + "/",
      "description": "An interactive, searchable edition of Timothy C. May's 1994 Cypherpunks FAQ.",
      "author": {"@type": "Person", "name": "Setvin Noether", "alternateName": "SauerNinja"},
      "isBasedOn": {"@id": BASE_URL + "/#originalwork"}
    },
    {
      "@type": "Book",
      "@id": BASE_URL + "/#originalwork",
      "name": "The Cyphernomicon: Cypherpunks FAQ and More",
      "author": {"@type": "Person", "name": "Timothy C. May"},
      "datePublished": "1994-09-10",
      "version": "0.666",
      "copyrightHolder": {"@type": "Person", "name": "Timothy C. May"},
      "copyrightYear": 1994,
      "genre": "Cryptography / Political philosophy",
      "numberOfPages": "20 sections",
      "url": BASE_URL + "/"
    },
    {
      "@type": "ItemList",
      "@id": BASE_URL + "/#toc",
      "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": s["title"], "url": f'{BASE_URL}/chapters/{s["slug"]}.html'}
        for i, s in enumerate(SECTIONS)
      ]
    }
  ]
}, indent=None)}
</script>'''

with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
    f.write(page_wrap("", None, "The Cyphernomicon — Interactive Edition",
                       "An interactive, searchable edition of Timothy C. May's 1994 Cypherpunks FAQ, with a foreword by Setvin Noether.",
                       index_body, canonical_path="index.html", og_type="website", jsonld=index_jsonld))

# ---------------------------------------------------------------------------
# About Tim May
# ---------------------------------------------------------------------------

about_body = '''
<div class="chapter-head">
  <div class="num">Biography</div>
  <h1>About Tim May</h1>
</div>

<div class="headerblock">
  <div class="field"><span class="k">Name</span><span class="v">Timothy C. May</span></div>
  <div class="field"><span class="k">Born</span><span class="v">December 21, 1951</span></div>
  <div class="field"><span class="k">Died</span><span class="v">December 13, 2018, at home in Corralitos, California — age 66</span></div>
  <div class="field"><span class="k">Known for</span><span class="v dim">Co-founding the Cypherpunks · "The Crypto Anarchist Manifesto" (1988) · The Cyphernomicon (1994)</span></div>
</div>

<div class="bio-portrait">
  <img src="assets/images/tim-may-portrait.jpg" alt="Illustrative portrait used for this edition" width="810" height="687" loading="eager">
  <div class="cap">Illustrative image, used for this edition — no verified photograph of Tim May circulates publicly; he avoided cameras by design.</div>
</div>

<details class="chunk depth-1" open>
<summary><span class="chunk-num">TM.1</span><span class="chunk-title">Early life: San Diego, a gun club, and Ayn Rand</span></summary>
<div class="chunk-body">
<p>May was born December 21, 1951, and grew up in a San Diego suburb before his family relocated to
Washington, D.C. when his father, a naval officer, was transferred there. He joined a local gun club at
12 at his father's urging and stayed a lifelong collector. By his own account he was a loner, a science
prodigy, and a heavy reader of science fiction — the profile that, decades later, made "write code instead
of asking permission" feel like the obvious move rather than a radical one.</p>
<p>The turn toward libertarianism came early and specifically: the summer before his junior year of high
school, in 1967, he picked up Ayn Rand's <em>Atlas Shrugged</em> and read it in three straight days. He
went on to U.C. Santa Barbara, took graduate physics classes, and from there went straight into
semiconductor work at Intel.</p>
</div>
</details>

<details class="chunk depth-1" open>
<summary><span class="chunk-num">TM.2</span><span class="chunk-title">Intel and the alpha-particle problem</span></summary>
<div class="chunk-body">
<p>May's most cited technical contribution has nothing to do with cryptography: in 1978 he and colleague
Murray Woods traced a mysterious source of memory-chip errors to alpha particles emitted by trace
radioactive elements inside the chip packaging itself — the "alpha-particle soft-error problem." Their
1979 paper on it won the IEEE's WRG Baker Prize, and the finding became a foundational result in
semiconductor reliability engineering.</p>
<p>A hundredfold run-up in Intel's stock through the mid-1980s gave May the option few engineers get: in
1986, at 34, he retired from Intel entirely, cashed in his options, and never had to work again.</p>
</div>
</details>

<details class="chunk depth-1" open>
<summary><span class="chunk-num">TM.3</span><span class="chunk-title">BlackNet, Chaum's epiphany, and the Crypto Anarchist Manifesto (1988)</span></summary>
<div class="chunk-body">
<p>The path to the Manifesto ran through a failed pitch. In 1987, May's friend Chip Morningstar introduced
him to economist Phil Salin, who was building AMiX, an early online marketplace for information. May
thought Salin's e-commerce framing missed the point — he pushed instead toward something closer to a
black market for information itself: a system where whistleblowers or leakers could sell secrets
untraceably. He'd later flesh this idea out as "BlackNet." But he saw the flaw immediately: none of it
worked without untraceable payment, and ordinary payment rails could always be traced back to a person.</p>
<p>Digging for an answer, May found a 1985 <em>Communications of the ACM</em> cover story by cryptographer
David Chaum on using cryptography to make digital transactions untraceable. He called it an epiphany —
"like standing on top of the mountain." Chaum's specific scheme didn't fully convince him, but the
underlying idea did: public-key cryptography, combined with networked computing, could dismantle
existing social and financial power structures. In September 1988, May sat down at his Macintosh Plus for
about ninety minutes and wrote a 497-word essay patterned loosely after <em>The Communist Manifesto</em>.
He titled it <em>The Crypto Anarchist Manifesto</em> and handed it out at that year's CRYPTO conference and
the Hackers Conference. Its central claim — that strong cryptography would let <em>"individuals and groups
to communicate and interact with each other"</em> beyond the reach of any government — reads today less
like speculation and more like a roadmap that got built.</p>
</div>
</details>

<details class="chunk depth-1" open>
<summary><span class="chunk-num">TM.4</span><span class="chunk-title">Founding the Cypherpunks (1992)</span></summary>
<div class="chunk-body">
<p>In September 1992, May and friends — commonly credited as Eric Hughes and John Gilmore, who hosted the
list on his toad.com server — set up a mailing list to keep arguing the ideas out loud. A hundred people
signed up within days; by 1997 it averaged 30 messages a day across roughly 2,000 subscribers. The name
itself, a play on "cyberpunk," was reportedly coined by Hughes' girlfriend at the time. May, Hughes, and
Gilmore later wore masks for the cover of <em>Wired</em>'s second issue, illustrating Steven Levy's 1993
profile of the group.</p>
<p>The list attracted people who'd go on to matter well beyond it. Julian Assange posted there from 1995
under the handle "Proff," years before WikiLeaks existed. May was, by most counts, its single most
prolific contributor across the decade that followed.</p>
</div>
</details>

<details class="chunk depth-1" open>
<summary><span class="chunk-num">TM.5</span><span class="chunk-title">The Cyphernomicon (1994)</span></summary>
<div class="chunk-body">
<p>Two years in, May sat down and wrote the list's sprawling unofficial FAQ — the document this site is
built around. It folded the Crypto Anarchist Manifesto in as source material and expanded it into roughly
seven hundred questions across twenty sections: cryptography basics, remailers and anonymity, the Clipper
Chip fight, digital cash, and the crypto-anarchist thesis in full. He was explicit that it was one person's
view, not a list consensus, and said as much in the document itself.</p>
</div>
</details>

<details class="chunk depth-1" id="tm-later" open>
<summary><span class="chunk-num">TM.6</span><span class="chunk-title">Decline of the list, and later years</span></summary>
<div class="chunk-body">
<p>The list's traffic and influence faded in the years after September 11, 2001 — by May's account, a lot
of people got cold feet about the subject matter — though it never formally dissolved. He grew more
private, living quietly at his home in Corralitos, California. When cryptocurrency itself finally arrived
and boomed, May was unimpressed with what the movement had become: in his last published interview, with
CoinDesk, he criticized crypto exchanges for adopting the KYC and anti-money-laundering rules he'd spent
his life arguing against, and said plainly that he thought Satoshi would have been disgusted by it.</p>
<div class="notice">
  <strong>A fuller picture.</strong> Reporting at the time of his death — including the <em>New York
  Times</em> obituary — noted that in his later years, after the Cypherpunks list had faded, May
  expressed racist views in other online forums, a marked and documented turn from his earlier public
  writing. It's included here because a biography that only tells the flattering half of the story isn't
  an honest one; it isn't the focus of his historical importance to this document, but it belongs in any
  accurate account of the man.</div>
</div>
</details>

<details class="chunk depth-1" id="tm-legacy" open>
<summary><span class="chunk-num">TM.7</span><span class="chunk-title">Death and legacy</span></summary>
<div class="chunk-body">
<p>May died of natural causes at home on December 13, 2018, eight days short of his 67th birthday. His
friend Lucky Green announced it publicly; obituaries ran in the <em>New York Times</em>, <em>Reason</em>,
<em>CoinDesk</em>, and <em>The Register</em>, among others — an unusual spread for a man who spent his
later decades avoiding public life.</p>
<p>The technical line from the Cypherpunks list to Bitcoin is not vague or retrospective — it's traceable
name by name. Adam Back first proposed Hashcash on the list, the proof-of-work scheme Satoshi's white
paper cites directly. Nick Szabo, creator of "Bit Gold" and coiner of the term "smart contracts,"
workshopped his ideas there. Wei Dai proposed his "b-money" digital cash system on the list, crediting May
as a major influence — and Satoshi contacted Dai directly while developing Bitcoin. Hal Finney, quoted at
length in this document's digital-cash sections, took Back's Hashcash idea toward real e-money and
went on to receive Bitcoin's first transaction from Satoshi in January 2009. May himself flagged Stuart
Haber and W. Scott Stornetta's digital timestamping work to the list — an early, direct ancestor of the
blockchain. Whether Satoshi Nakamoto ever posted to the list under another name is unknown and
unknowable. It didn't need to happen that way for the lineage to be real.</p>
</div>
</details>

<h2 style="font-size:0.85rem; letter-spacing:.06em; text-transform:uppercase; color:var(--ink-faint); margin: 2.5rem 0 0.6rem; border-top:1px solid var(--rule); padding-top:1.5rem;">Sources</h2>
<ul class="outline" style="font-size:0.85rem;">
  <li><a href="https://en.wikipedia.org/wiki/Timothy_C._May">Timothy C. May — Wikipedia</a></li>
  <li><a href="https://www.nytimes.com/2018/12/21/obituaries/timothy-c-may-dead.html">Timothy C. May, Early Advocate of Internet Privacy, Dies at 66 — The New York Times</a></li>
  <li><a href="https://reason.com/2018/12/16/tim-may-influential-writer-on-crypto-ana/">Tim May, Father of 'Crypto Anarchy,' Is Dead at 66 — Reason</a></li>
  <li><a href="https://www.theregister.com/2018/12/17/timothy_c_may/">Influential cypherpunk and crypto-anarchist Tim May dies aged 67 — The Register</a></li>
  <li><a href="https://www.coindesk.com/markets/2018/12/17/cypherpunk-legend-timothy-may-has-passed-away">Cypherpunk Legend Timothy May Has Passed Away — CoinDesk</a></li>
  <li><a href="https://cryptoanarchy.wiki/people/timothy-c-may">Timothy C. May — cryptoanarchy.wiki</a></li>
</ul>

<nav class="chapter-pager">
  <a class="prev" href="index.html"><span class="lbl">← Back</span>Cover &amp; Foreword</a>
  <a class="next" href="chapters/01-Introduction.html"><span class="lbl">Next →</span>§01 Introduction</a>
</nav>
'''

about_jsonld = f'''
<script type="application/ld+json">
{json.dumps({
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "The Cyphernomicon", "item": BASE_URL + "/"},
    {"@type": "ListItem", "position": 2, "name": "About Tim May", "item": BASE_URL + "/about-tim-may.html"}
  ]
})}
</script>
<script type="application/ld+json">
{json.dumps({
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "mainEntity": {
    "@type": "Person",
    "name": "Timothy C. May",
    "alternateName": "Tim May",
    "birthDate": "1951-12-21",
    "deathDate": "2018-12-13",
    "jobTitle": "Electronic engineer; writer",
    "description": "Co-founder of the Cypherpunks mailing list, author of The Crypto Anarchist Manifesto (1988) and The Cyphernomicon (1994).",
    "worksFor": {"@type": "Organization", "name": "Intel Corporation (1974–1986)"}
  }
})}
</script>'''

with open(os.path.join(SITE, "about-tim-may.html"), "w", encoding="utf-8") as f:
    f.write(page_wrap("", "about-tim-may", "About Tim May — The Cyphernomicon",
                       "Who Timothy C. May was: Intel engineer, author of the Crypto Anarchist Manifesto, co-founder of the Cypherpunks, and writer of the Cyphernomicon.",
                       about_body, canonical_path="about-tim-may.html", og_type="profile", jsonld=about_jsonld,
                       keywords="tim may, timothy c may, cypherpunks founder, crypto anarchist manifesto, cyphernomicon author, intel alpha particle"))
print("Wrote about-tim-may.html")

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
    chapter_jsonld = f'''
<script type="application/ld+json">
{json.dumps({
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "The Cyphernomicon", "item": BASE_URL + "/"},
    {"@type": "ListItem", "position": 2, "name": f"§{num} {title}", "item": f'{BASE_URL}/chapters/{slug}.html'}
  ]
})}
</script>
<script type="application/ld+json">
{json.dumps({
  "@context": "https://schema.org",
  "@type": "Chapter",
  "name": f"§{num} {title}",
  "isPartOf": {"@type": "Book", "name": "The Cyphernomicon: Cypherpunks FAQ and More", "author": {"@type": "Person", "name": "Timothy C. May"}},
  "author": {"@type": "Person", "name": "Timothy C. May"},
  "position": i + 1,
  "url": f'{BASE_URL}/chapters/{slug}.html'
})}
</script>'''
    with open(os.path.join(CHAP, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(page_wrap("../", slug, f"§{num} {title} — The Cyphernomicon", desc, body,
                           canonical_path=f"chapters/{slug}.html", og_type="article", jsonld=chapter_jsonld,
                           keywords=f"cyphernomicon, {title.lower()}, tim may, cypherpunks faq, section {num}"))


# ---------------------------------------------------------------------------
# sitemap.xml
# ---------------------------------------------------------------------------
import datetime
BUILD_DATE = datetime.date.today().isoformat()

urls = [(BASE_URL + "/", "1.0"), (f"{BASE_URL}/about-tim-may.html", "0.7")]
for s in SECTIONS:
    urls.append((f'{BASE_URL}/chapters/{s["slug"]}.html', "0.8"))

sitemap_entries = "\n".join(
    f"  <url><loc>{u}</loc><lastmod>{BUILD_DATE}</lastmod><priority>{p}</priority></url>" for u, p in urls
)
sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_entries}
</urlset>
'''
with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap)

print("Wrote index.html,", len(SECTIONS), "chapter pages, and sitemap.xml")
