#!/usr/bin/env python3
import json, os, html, re

DATA = "/home/claude/work/build/data"
SITE = "/home/claude/work/site"
CHAP = os.path.join(SITE, "chapters")

SECTIONS = [
    ("01-Introduction", "Introduction", "Why this document exists, and how to read it."),
    ("02-MFAQ", "Most Frequently Asked Questions", "The questions newcomers ask first, answered plainly."),
    ("03-Cypherpunks", "Cypherpunks — History, Organization, Agenda", "How the list started, who was on it, and what it stood for."),
    ("04-Goals-and-Ideology", "Goals and Ideology", "Privacy, freedom, and the new approaches crypto makes possible."),
    ("05-Cryptology", "Cryptology", "The technical foundations: keys, ciphers, and trust."),
    ("06-The-Need-For-Strong-Crypto", "The Need for Strong Crypto", "Why weak, escrowed, or government-approved crypto defeats the point."),
    ("07-Summary-PGP", "Summary — PGP", "Pretty Good Privacy: the tool that made the list possible."),
    ("08-Anonymity", "Anonymity, Digital Mixes, and Remailers", "Untraceable mail, mix networks, and the mechanics of not being seen."),
    ("09-Policy", "Policy — Clipper, Key Escrow, and Digital Telephony", "The government's counter-moves, and why they failed."),
    ("10-Legal-Issues", "Legal Issues", "Export controls, the First Amendment, and crypto as speech."),
    ("11-Surveillance", "Surveillance, Privacy, and Intelligence Agencies", "What the state can see, and what strong crypto takes away."),
    ("12-Digital-Cash", "Digital Cash and Net Commerce", "Chaum, blinding, double-spending — money before Bitcoin existed."),
    ("13-Activism-and-Projects", "Activism and Projects", "What the list actually built, not just argued about."),
    ("14-Other-Advanced-Crypto-Applications", "Other Advanced Crypto Applications", "Voting, timestamping, and other uses beyond mail and money."),
    ("15-Reputations-and-Credentials", "Reputations and Credentials", "Trust without identity — proving things without saying who you are."),
    ("16-Crypto-Anarchy", "Crypto Anarchy", "The core thesis: what happens when the state can no longer intercept."),
    ("17-The-Future", "The Future", "Predictions — some wrong, some eerily exact."),
    ("18-Loose-Ends", "Loose Ends and Miscellaneous Topics", "Everything that didn't fit cleanly elsewhere."),
    ("19-Appendices", "Appendices", "Reference material, glossary fragments, and source lists."),
    ("20-Readme", "README", "Tim May on the document itself — style, scope, and disclaimers."),
]

def anchor_id(num):
    return "h-" + num.replace(".", "-")

def esc(s):
    return html.escape(s, quote=False)

def linkify_and_escape(text):
    """Escape text, then turn bare URLs into links."""
    text = esc(text)
    url_re = re.compile(r'((?:https?|ftp)://[^\s<>\)\]]+)')
    return url_re.sub(r'<a href="\1" rel="nofollow noopener">\1</a>', text)

SEARCH_INDEX = []

def flat_snippet(node, limit=220):
    """Flatten a node + shallow children text for search snippet purposes."""
    parts = [node.get("title") or node.get("text") or ""]
    if node.get("title") and node.get("text"):
        parts.append(node["text"])
    for c in node.get("children", [])[:4]:
        t = c.get("text") or c.get("title") or ""
        if t:
            parts.append(t)
    s = " — ".join([p for p in parts if p])
    return s[:limit]

def render_bullet(node, section_slug, path_titles):
    children = node.get("children", [])
    text = linkify_and_escape(node["text"])
    if children:
        inner = "".join(render_bullet(c, section_slug, path_titles) for c in children)
        return (f'<li><details><summary>{text}</summary>'
                f'<ul class="outline">{inner}</ul></details></li>')
    else:
        return f'<li>{text}</li>'

def render_node(node, depth, section_slug, section_title, path_titles):
    if node["type"] == "heading":
        num = node["num"]
        aid = anchor_id(num)
        title = esc(node["title"])
        lede = node.get("text", "").strip()
        children = node.get("children", [])
        d = min(depth, 4)

        new_path = path_titles + [node["title"]]
        # index this heading for search
        SEARCH_INDEX.append({
            "h": f"chapters/{section_slug}.html#{aid}",
            "p": f"{section_title} \u203a " + " \u203a ".join(new_path[-2:]) if len(new_path) > 1 else section_title,
            "t": flat_snippet(node)
        })

        body_bits = []
        bullets_buffer = []

        def flush_bullets():
            nonlocal bullets_buffer
            if bullets_buffer:
                body_bits.append('<ul class="outline">' + "".join(bullets_buffer) + '</ul>')
                bullets_buffer = []

        for c in children:
            if c["type"] == "heading":
                flush_bullets()
                body_bits.append(render_node(c, depth + 1, section_slug, section_title, new_path))
            else:
                bullets_buffer.append(render_bullet(c, section_slug, new_path))
                # also index substantial bullet text (top-level bullets only, to avoid bloat)
                if len(c["text"]) > 40:
                    SEARCH_INDEX.append({
                        "h": f"chapters/{section_slug}.html#{aid}",
                        "p": f"{section_title} \u203a " + " \u203a ".join(new_path[-2:]),
                        "t": flat_snippet(c)
                    })
        flush_bullets()

        open_attr = " open" if d <= 2 else ""
        lede_html = f'<p class="chunk-lede">{linkify_and_escape(lede)}</p>' if lede and d >= 3 else ""
        # For copyright/lede at any depth if it's the only content, still show it
        if lede and d < 3 and not children:
            lede_html = f'<p class="chunk-lede">{linkify_and_escape(lede)}</p>'

        return (
            f'<details class="chunk depth-{d}" id="{aid}"{open_attr}>'
            f'<summary><span class="chunk-num">{esc(num)}</span>'
            f'<span class="chunk-title">{title}</span></summary>'
            f'<div class="chunk-body">{lede_html}{"".join(body_bits)}</div>'
            f'</details>'
        )
    else:
        # stray root-level paragraph/bullet (rare)
        return f'<p>{linkify_and_escape(node["text"])}</p>'

def render_chapter_body(tree, section_slug, section_title):
    out = []
    for node in tree:
        out.append(render_node(node, 1, section_slug, section_title, []))
    return "".join(out)

# ---------------------------------------------------------------------------
print("Rendering chapter bodies...")
rendered = {}
os.makedirs(os.path.join("/home/claude/work/build", "rendered"), exist_ok=True)
for slug, title, desc in SECTIONS:
    tree = json.load(open(os.path.join(DATA, f"{slug}.json"), encoding="utf-8"))
    rendered[slug] = render_chapter_body(tree, slug, title)
    with open(os.path.join("/home/claude/work/build/rendered", f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(rendered[slug])
    print(f"  {slug}: {len(rendered[slug])} chars, index size so far {len(SEARCH_INDEX)}")

os.makedirs(os.path.join(SITE, "assets", "data"), exist_ok=True)

# About Tim May isn't one of the 20 numbered FAQ sections, so it's not in SECTIONS
# above — but it still needs to be searchable. Adding its entries here (rather than
# patching search-index.json by hand afterward) keeps this script the single source
# of truth for the whole index.
ABOUT_TIM_MAY_ENTRIES = [
    {"h": "about-tim-may.html", "p": "About Tim May",
     "t": "Timothy C. May biography — Intel engineer, alpha-particle soft-error problem, retired 1986, wrote The Crypto Anarchist Manifesto in 1988, co-founded the Cypherpunks mailing list in 1992 with Eric Hughes and John Gilmore, wrote The Cyphernomicon in 1994, died December 13 2018."},
    {"h": "about-tim-may.html#tm-later", "p": "About Tim May \u203a Decline of the list, and later years",
     "t": "Cypherpunks list traffic wound down through the early 2000s. May lived privately in Corralitos, California. Reporting at the time of his death, including the New York Times obituary, noted he expressed racist views in other online forums in his later years."},
    {"h": "about-tim-may.html#tm-legacy", "p": "About Tim May \u203a Death and legacy",
     "t": "May died of natural causes at home on December 13 2018. Hal Finney, quoted in the Cyphernomicon digital-cash sections, ran the first Bitcoin transaction with Satoshi Nakamoto."},
]
SEARCH_INDEX = ABOUT_TIM_MAY_ENTRIES + SEARCH_INDEX

with open(os.path.join(SITE, "assets", "data", "search-index.json"), "w", encoding="utf-8") as f:
    json.dump(SEARCH_INDEX, f, ensure_ascii=False)
print("Search index entries:", len(SEARCH_INDEX), f"({len(ABOUT_TIM_MAY_ENTRIES)} About Tim May + {len(SEARCH_INDEX)-len(ABOUT_TIM_MAY_ENTRIES)} FAQ sections)")

with open(os.path.join(SITE, "assets", "data", "sections.json"), "w", encoding="utf-8") as f:
    json.dump([{"slug": s, "title": t, "desc": d} for s, t, d in SECTIONS], f)

print("OK")
