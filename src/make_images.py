#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/claude/work/site/assets"

INK = (24, 22, 15, 255)
PAPER = (233, 227, 208, 255)
PAPER_RAISED = (242, 237, 224, 255)
RED = (165, 52, 42, 255)
TEAL = (43, 100, 89, 255)
AMBER = (146, 114, 31, 255)
RULE = (169, 157, 120, 255)

MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

# ---------------------------------------------------------------------
# Favicons: dark tile, red serif-mono "C" mark (matches assets/favicon.svg)
# ---------------------------------------------------------------------
def make_favicon(size):
    img = Image.new("RGBA", (size, size), INK)
    d = ImageDraw.Draw(img)
    # rounded corners
    radius = max(2, size // 10)
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    bg = Image.new("RGBA", (size, size), INK)
    out = Image.composite(bg, Image.new("RGBA", (size, size), (0, 0, 0, 0)), mask)
    d = ImageDraw.Draw(out)
    f = font(MONO_BOLD, int(size * 0.62))
    text = "C"
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1]), text, font=f, fill=RED)
    return out

for size, name in [(16, "favicon-16x16.png"), (32, "favicon-32x32.png"),
                    (180, "apple-touch-icon.png"), (512, "icon-512.png")]:
    make_favicon(size).save(f"{OUT}/{name}")

# .ico with multiple sizes embedded
ico_img = make_favicon(48)
ico_img.save(f"{OUT}/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

print("favicons done")

# ---------------------------------------------------------------------
# og-image.png (1200x630) — cover-sheet look matching the site
# ---------------------------------------------------------------------
W, H = 1200, 630
img = Image.new("RGB", (W, H), PAPER[:3])
d = ImageDraw.Draw(img)

# faint rule frame
d.rectangle([40, 40, W - 40, H - 40], outline=RULE[:3], width=1)

# eyebrow
f_eyebrow = font(MONO_BOLD, 20)
d.text((80, 90), "CYPHERPUNKS FAQ & MORE · EST. 1994", font=f_eyebrow, fill=(117, 111, 94))

# title
f_title = font(MONO_BOLD, 84)
d.text((78, 130), "THE", font=f_title, fill=INK[:3])
d.text((78, 220), "CYPHERNOMICON", font=f_title, fill=INK[:3])
# red period
bbox = d.textbbox((78, 220), "CYPHERNOMICON", font=f_title)
d.text((bbox[2] + 6, 220), ".", font=f_title, fill=RED[:3])

# dek
f_dek = font(SERIF, 26)
dek_lines = [
    "An interactive, searchable edition of Timothy C. May's",
    "1994 Cypherpunks manifesto-FAQ — with a foreword by",
    "Setvin Noether connecting it to Bitcoin history.",
]
y = 335
for line in dek_lines:
    d.text((80, y), line, font=f_dek, fill=(75, 70, 64))
    y += 38

# header-block strip at bottom, usenet style
d.line([80, 500, W - 80, 500], fill=RULE[:3], width=1)
f_hb_k = font(MONO, 18)
f_hb_v = font(MONO_BOLD, 18)
rows = [("FROM", "tcmay@netcom.com"), ("VERSION", "0.666 · 1994-09-10"), ("EDITION", "Interactive · 2026")]
x = 80
yy = 530
for k, v in rows:
    d.text((x, yy), k, font=f_hb_k, fill=(117, 111, 94))
    d.text((x, yy + 26), v, font=f_hb_v, fill=INK[:3])
    x += 340

# stamp
f_stamp = font(MONO_BOLD, 22)
stamp_text = "20 SECTIONS"
sb = d.textbbox((0, 0), stamp_text, font=f_stamp)
sw, sh = sb[2] - sb[0], sb[3] - sb[1]
stamp_img = Image.new("RGBA", (sw + 40, sh + 30), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp_img)
sd.rectangle([0, 0, sw + 39, sh + 29], outline=RED, width=4)
sd.text((20, 12), stamp_text, font=f_stamp, fill=RED)
stamp_img = stamp_img.rotate(-6, expand=True, resample=Image.BICUBIC)
img.paste(stamp_img, (W - stamp_img.width - 90, 90), stamp_img)

img.save(f"{OUT}/og-image.png")
print("og-image done", img.size)
