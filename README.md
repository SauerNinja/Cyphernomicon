# The Cyphernomicon — Interactive Edition

A navigable, searchable, outline-preserving reader for Timothy C. May's
1994 Cypherpunks FAQ, with a foreword by Setvin Noether on how the
document connects to Bitcoin and cypherpunk history.

**Live site:** https://sauerninja.github.io/Cyphernomicon/
*(update this link if you rename or move the repo)*

## What this is

The original Cyphernomicon is a ~700-question, 20-section outline FAQ,
written in a Mac outline editor and distributed as plain text on the
Cypherpunks mailing list. This edition:

- Parses the original outline structure (section → subsection → nested
  bullets) into a proper tree, preserving May's own numbering
  (`12.5.3`, etc.) as permalinkable anchors.
- Renders it as a collapsible outline in the browser — expand a
  section, collapse back to headings, jump straight to a numbered
  passage.
- Adds full-text client-side search across all ~3,900 indexed passages
  (`⌘K` / `/`).
- Adds a foreword connecting the document's digital-cash and
  crypto-anarchy sections to what came after, including Bitcoin.

No build step, no framework, no dependencies — static HTML/CSS/vanilla
JS, deployable as-is on GitHub Pages.

## Structure

```
index.html              cover sheet + foreword + table of contents
chapters/*.html          the 20 sections
assets/css/style.css      design system
assets/js/site.js         sidebar, search, outline controls
assets/data/search-index.json   flattened search index
assets/data/sections.json       section metadata
LICENSE                   MIT — covers the code/design/foreword only
NOTICE.md                 explains what is and isn't MIT-licensed
```

## Regenerating the site

The HTML pages are generated from the original per-section Markdown
source (kept in `src/` if you're rebuilding from scratch) via a small
Python pipeline: an outline parser converts each section's plain-text
outline into JSON, then a template step renders that JSON into the
final HTML pages and search index. No third-party packages required —
standard library only.

## License

- **Code, design, and the foreword** — MIT. See `LICENSE`.
- **The Cyphernomicon text** — © 1994 Timothy C. May, all rights
  reserved, reproduced here for historical/educational reference. See
  `NOTICE.md` before reusing the document text elsewhere.
