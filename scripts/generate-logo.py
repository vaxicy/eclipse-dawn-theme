"""
Eclipse Dawn Theme — logo generation (code-first, PIL).

Produces app-icon style logos: a rounded-rectangle (squircle) background with
a deep navy -> indigo/violet gradient, plus a solar-eclipse motif (dark disc +
glowing periwinkle corona). Some variants add a warm dawn accent.

Palette from manifest.json:
  frame / frame_inactive : rgb(60,61,104) / rgb(79,80,116)
  toolbar                : rgb(45,46,67)
  ntp_background         : rgb(24,24,32)
  ntp_link               : rgb(174,188,214)  (periwinkle)

Outputs: store-assets/icon-candidates/logo-XX-*.png at 512px (preview).
Final 128px is exported once a direction is chosen.
"""

import os
import math
import random
from PIL import Image, ImageDraw

SIZE = 512
C = SIZE / 2.0

# ---------------- palette ----------------
NAVY = (22, 23, 33)
NAVY_TOP = (26, 27, 40)
INDIGO = (60, 61, 104)
VIOLET = (79, 80, 116)
DEEP = (18, 18, 27)
PERI = (174, 188, 214)
PERI_BRIGHT = (222, 232, 250)
DAWN = (255, 196, 142)
DAWN_PINK = (243, 168, 182)

OUT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "store-assets", "icon-candidates")
)


def lerp(a, b, t):
    t = max(0.0, min(1.0, t))
    return (a[0] + (b[0] - a[0]) * t,
            a[1] + (b[1] - a[1]) * t,
            a[2] + (b[2] - a[2]) * t)


def gauss(x, sigma):
    return math.exp(-(x * x) / (2.0 * sigma * sigma))


def blend(px, x, y, col, a):
    """alpha-blend col over the existing pixel (art is opaque background)."""
    if a <= 0.002:
        return
    a = min(1.0, a)
    r, g, b, _ = px[x, y]
    px[x, y] = (int(r + (col[0] - r) * a),
                int(g + (col[1] - g) * a),
                int(b + (col[2] - b) * a),
                255)


def vgrad(top, bot):
    strip = Image.new("RGB", (1, SIZE))
    for y in range(SIZE):
        strip.putpixel((0, y), tuple(int(v) for v in lerp(top, bot, y / (SIZE - 1))))
    return strip.resize((SIZE, SIZE)).convert("RGBA")


def diag_grad(c1, c2):
    img = Image.new("RGBA", (SIZE, SIZE))
    px = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            t = (x + y) / (2.0 * (SIZE - 1))
            col = lerp(c1, c2, t)
            px[x, y] = (int(col[0]), int(col[1]), int(col[2]), 255)
    return img


def apply_round(img, radius_ratio=0.225):
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, SIZE - 1, SIZE - 1], radius=int(radius_ratio * SIZE), fill=255)
    out = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def paint_eclipse(art, cx, cy, rd, sigma, disc_hi, disc_lo,
                  corona, corona_hi, corona_gain=1.15):
    """dark disc + soft glowing ring, painted onto an opaque RGBA art layer."""
    px = art.load()
    reach = rd + sigma * 4.2
    x0, x1 = max(0, int(cx - reach)), min(SIZE, int(cx + reach) + 1)
    y0, y1 = max(0, int(cy - reach)), min(SIZE, int(cy + reach) + 1)
    for y in range(y0, y1):
        for x in range(x0, x1):
            r = math.hypot(x - cx, y - cy)
            if r <= rd:
                t = r / rd
                col = lerp(disc_hi, disc_lo, t)
                px[x, y] = (int(col[0]), int(col[1]), int(col[2]), 255)
            else:
                g = gauss(r - rd, sigma)
                if g < 0.004:
                    continue
                col = lerp(corona, corona_hi, min(1.0, g * 1.3))
                blend(px, x, y, col, min(1.0, g * corona_gain))


def paint_dawn_band(art, col_a, col_b, start=0.62, strength=0.55):
    """warm glow rising from the bottom (dawn)."""
    px = art.load()
    y0 = int(start * SIZE)
    for y in range(y0, SIZE):
        t = (y - y0) / max(1, (SIZE - y0))
        col = lerp(col_a, col_b, t)
        # brighter near the horizon line, fading downward
        a = strength * (1.0 - abs(t - 0.15) / 0.85) ** 1.4
        for x in range(SIZE):
            blend(px, x, y, col, a)


def paint_radial_glow(art, cx, cy, radius, col, strength):
    px = art.load()
    reach = radius * 1.05
    x0, x1 = max(0, int(cx - reach)), min(SIZE, int(cx + reach) + 1)
    y0, y1 = max(0, int(cy - reach)), min(SIZE, int(cy + reach) + 1)
    for y in range(y0, y1):
        for x in range(x0, x1):
            d = math.hypot(x - cx, y - cy)
            if d >= reach:
                continue
            t = 1.0 - d / reach
            blend(px, x, y, col, (t ** 2) * strength)


def paint_vignette(art, strength=0.35):
    px = art.load()
    for y in range(SIZE):
        for x in range(SIZE):
            d = math.hypot(x - C, y - C) / (SIZE * 0.72)
            if d > 0.55:
                a = ((d - 0.55) / 0.45) ** 2 * strength
                blend(px, x, y, (8, 8, 14), a)


def paint_stars(art, n=46, seed=7):
    random.seed(seed)
    px = art.load()
    for _ in range(n):
        x = random.randint(int(0.10 * SIZE), int(0.90 * SIZE))
        y = random.randint(int(0.08 * SIZE), int(0.70 * SIZE))
        rad = random.uniform(0.9, 2.1)
        a = random.uniform(0.25, 0.75)
        rr = int(math.ceil(rad))
        for yy in range(y - rr, y + rr + 1):
            for xx in range(x - rr, x + rr + 1):
                if 0 <= xx < SIZE and 0 <= yy < SIZE:
                    d = math.hypot(xx - x, yy - y)
                    if d <= rad:
                        blend(px, xx, yy, PERI_BRIGHT, a * (1 - d / (rad + 1e-6)))


def paint_top_highlight(art, strength=0.10):
    """soft glassy highlight across the top portion."""
    px = art.load()
    for y in range(0, int(0.42 * SIZE)):
        a = strength * gauss(y - 0.16 * SIZE, 0.16 * SIZE)
        for x in range(SIZE):
            blend(px, x, y, (255, 255, 255), a)


# =========================== variants ===========================

def v1_eclipse():
    art = vgrad(NAVY_TOP, INDIGO)
    paint_vignette(art, 0.30)
    paint_top_highlight(art, 0.06)
    paint_eclipse(art, C, C, 0.255 * SIZE, 0.075 * SIZE,
                  NAVY_TOP, DEEP, PERI, PERI_BRIGHT)
    return apply_round(art)


def v2_dawn_rise():
    art = vgrad(NAVY_TOP, VIOLET)
    paint_dawn_band(art, DAWN, DAWN_PINK, start=0.60, strength=0.60)
    paint_eclipse(art, C, 0.50 * SIZE, 0.235 * SIZE, 0.072 * SIZE,
                  NAVY_TOP, DEEP, PERI, PERI_BRIGHT)
    return apply_round(art)


def v3_rings():
    art = vgrad(NAVY, (44, 45, 74))
    paint_vignette(art, 0.30)
    px = art.load()
    rings = [(0.150, PERI, 1.00),
             (0.240, VIOLET, 0.85),
             (0.340, PERI, 0.55)]
    w = 0.010 * SIZE
    for rr, col, st in rings:
        R = rr * SIZE
        reach = R + w * 3
        x0, x1 = max(0, int(C - reach)), min(SIZE, int(C + reach) + 1)
        y0, y1 = max(0, int(C - reach)), min(SIZE, int(C + reach) + 1)
        for y in range(y0, y1):
            for x in range(x0, x1):
                d = math.hypot(x - C, y - C)
                g = gauss(d - R, w / 2.1)
                if g > 0.02:
                    blend(px, x, y, col, min(1.0, g * st))
    paint_eclipse(art, C, C, 0.095 * SIZE, 0.028 * SIZE,
                  NAVY_TOP, DEEP, PERI, PERI_BRIGHT, corona_gain=1.0)
    return apply_round(art)


def v4_halo():
    art = vgrad((16, 17, 25), INDIGO)
    paint_radial_glow(art, C, C * 0.98, 0.52 * SIZE, (92, 106, 168), 0.85)
    paint_vignette(art, 0.42)
    paint_eclipse(art, C, C, 0.235 * SIZE, 0.085 * SIZE,
                  (34, 35, 52), DEEP, PERI, PERI_BRIGHT, corona_gain=1.25)
    return apply_round(art)


def v5_crescent():
    art = diag_grad((20, 21, 31), (74, 68, 122))
    paint_vignette(art, 0.30)
    px = art.load()
    rd = 0.255 * SIZE
    sigma = 0.070 * SIZE
    lx, ly = 0.42, 0.40
    reach = rd + sigma * 4.2
    x0, x1 = max(0, int(C - reach)), min(SIZE, int(C + reach) + 1)
    y0, y1 = max(0, int(C - reach)), min(SIZE, int(C + reach) + 1)
    for y in range(y0, y1):
        for x in range(x0, x1):
            dx, dy = x - C, y - C
            r = math.hypot(dx, dy)
            if r <= rd:
                facing = (dx * lx + dy * ly) / (rd + 1e-6)
                warm = max(0.0, facing) ** 1.5
                base = lerp((38, 39, 58), DEEP, r / rd)
                col = lerp(base, DAWN, warm * 0.8)
                px[x, y] = (int(col[0]), int(col[1]), int(col[2]), 255)
            else:
                g = gauss(r - rd, sigma)
                if g < 0.004:
                    continue
                facing = (dx * lx + dy * ly) / (r + 1e-6)
                warm = max(0.0, facing) ** 2
                cool = lerp(PERI, PERI_BRIGHT, min(1.0, g * 1.3))
                col = lerp(cool, DAWN, warm * 0.55)
                blend(px, x, y, col, min(1.0, g * 1.1))
    return apply_round(art)


def v6_starry():
    art = vgrad((19, 20, 30), (52, 53, 92))
    paint_stars(art, n=52, seed=11)
    paint_vignette(art, 0.34)
    paint_eclipse(art, C, 0.54 * SIZE, 0.245 * SIZE, 0.075 * SIZE,
                  NAVY_TOP, DEEP, PERI, PERI_BRIGHT)
    return apply_round(art)


VARIANTS = [
    ("logo-01-eclipse.png", v1_eclipse),
    ("logo-02-dawn-rise.png", v2_dawn_rise),
    ("logo-03-rings.png", v3_rings),
    ("logo-04-halo.png", v4_halo),
    ("logo-05-crescent.png", v5_crescent),
    ("logo-06-starry.png", v6_starry),
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, fn in VARIANTS:
        img = fn()
        path = os.path.join(OUT_DIR, name)
        img.save(path)
        print("wrote", path)


if __name__ == "__main__":
    main()
