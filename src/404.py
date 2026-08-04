import sys
sys.path.insert(0, '/home/claude/work/build')
from assemble import page_wrap
body = '''
<div class="hero">
  <div class="hero__eyebrow">Error 404</div>
  <h1>Page not <span class="accent">found</span>.</h1>
  <p class="hero__dek">Whatever you were looking for isn't at this address. It might have moved,
  or the anchor you followed points somewhere that no longer exists.</p>
  <div class="hero__actions">
    <a class="btn btn--solid" href="/Cyphernomicon/index.html">Back to the cover sheet →</a>
  </div>
</div>
'''
html_out = page_wrap('/Cyphernomicon/', None, "404 — The Cyphernomicon", "Page not found.", body,
                      canonical_path="404.html")
html_out = html_out.replace('<meta name="robots" content="index, follow, max-image-preview:large">',
                             '<meta name="robots" content="noindex, follow">')
with open('/home/claude/work/site/404.html', 'w', encoding='utf-8') as f:
    f.write(html_out)
print("wrote 404.html")
