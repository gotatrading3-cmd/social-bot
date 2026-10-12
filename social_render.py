"""Rendu des visuels (image 4:5 pour Facebook/Instagram, video 9:16 pour Reels/TikTok). Pillow + ffmpeg, 100 % gratuit."""
import os, random, shutil, subprocess, tempfile
from social_content import CTA_BAR
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
BRAND = "GOTA TRADING"

THEMES = [  # fond haut, fond bas, accent, texte
    ((8, 12, 24), (14, 30, 52), (240, 185, 11), (245, 247, 250)),
    ((10, 10, 14), (30, 24, 40), (0, 214, 143), (245, 245, 245)),
    ((6, 20, 30), (8, 52, 70), (255, 196, 0), (240, 248, 252)),
    ((20, 8, 20), (52, 16, 44), (255, 120, 90), (252, 244, 246)),
    ((6, 14, 12), (10, 44, 36), (240, 185, 11), (240, 250, 246)),
]


def _font(bold, size):
    return ImageFont.truetype(os.path.join(ASSETS, "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)


def _wrap(draw, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _fit(draw, text, bold, start, minsize, maxw, maxlines):
    s = start
    while s >= minsize:
        f = _font(bold, s)
        ls = _wrap(draw, text, f, maxw)
        if len(ls) <= maxlines:
            return f, ls, s
        s -= 4
    f = _font(bold, minsize)
    return f, _wrap(draw, text, f, maxw)[:maxlines], minsize


def _background(w, h, theme, seed):
    top, bot, acc, _ = theme
    img = Image.new("RGB", (w, h))
    px = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        px.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    # bougies japonaises en filigrane (decor aleatoire, purement visuel)
    rnd = random.Random(seed)
    deco = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(deco)
    n = 17
    step = w / n
    price = h * 0.72
    for i in range(n):
        o = price
        price += rnd.uniform(-90, 80)
        price = max(h * 0.45, min(h * 0.92, price))
        c = price
        hi = min(o, c) - rnd.uniform(15, 70)
        lo = max(o, c) + rnd.uniform(15, 70)
        col = (0, 214, 143, 40) if c < o else (255, 80, 90, 40)
        x = i * step + step / 2
        d.line([(x, hi), (x, lo)], fill=col, width=4)
        d.rectangle([x - step * 0.28, min(o, c), x + step * 0.28, max(o, c)], fill=col)
    img = Image.alpha_composite(img.convert("RGBA"), deco.filter(ImageFilter.GaussianBlur(1.2)))
    # halo d'accent
    halo = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([w * 0.55, -h * 0.12, w * 1.3, h * 0.28], fill=acc + (38,))
    img = Image.alpha_composite(img, halo.filter(ImageFilter.GaussianBlur(120)))
    # logo + marque
    logo = Image.open(os.path.join(ASSETS, "logo.png")).convert("RGBA")
    lw = int(w * 0.13)
    logo = logo.resize((lw, int(lw * logo.height / logo.width)))
    img.alpha_composite(logo, (int(w * 0.07), int(h * 0.045)))
    dd = ImageDraw.Draw(img)
    dd.text((int(w * 0.07) + lw + 22, int(h * 0.045) + logo.height // 2), BRAND, font=_font(True, int(w * 0.036)),
            fill=acc, anchor="lm")
    return img


def _text_layer(c, w, h, theme, p=1.0):
    """Calque de texte. p in [0,1] : progression de l'apparition (video)."""
    _, _, acc, fg = theme
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    mx = int(w * 0.08)
    maxw = w - 2 * mx

    def A(a):
        return max(0, min(1, a))

    def slide(t0, t1):
        a = A((p - t0) / (t1 - t0))
        return a, int((1 - a) * 40)

    # etiquette
    a, dy = slide(0.0, 0.2)
    lf = _font(True, int(w * 0.034))
    tw = d.textlength(c["label"], font=lf)
    ly = int(h * 0.2) + dy
    d.rounded_rectangle([mx, ly, mx + tw + 56, ly + int(w * 0.075)], radius=int(w * 0.04), fill=acc + (int(255 * a),))
    d.text((mx + 28, ly + int(w * 0.0375)), c["label"], font=lf, fill=(10, 12, 20, int(255 * a)), anchor="lm")

    # titre
    a, dy = slide(0.12, 0.45)
    tf, tl, ts = _fit(d, c["title"], True, int(w * (0.07 if c["kind"] == "regle" else 0.088)), int(w * 0.05), maxw, 3 if c["kind"] == "regle" else 4)
    y = int(h * 0.285) + dy
    for ln in tl:
        d.text((mx, y), ln, font=tf, fill=fg + (int(255 * a),))
        y += int(ts * 1.25)
    y += int(h * 0.025)
    d.rectangle([mx, y, mx + int(w * 0.18), y + 8], fill=acc + (int(255 * a),))
    y += int(h * 0.04)

    # corps
    if c["kind"] == "regle":
        bf = _font(False, int(w * 0.05))
        for i, it in enumerate(c["items"]):
            a, dy = slide(0.4 + i * 0.1, 0.55 + i * 0.1)
            d.ellipse([mx, y + dy + 6, mx + 46, y + dy + 52], fill=acc + (int(255 * a),))
            d.text((mx + 23, y + dy + 29), str(i + 1), font=_font(True, int(w * 0.04)), fill=(10, 12, 20, int(255 * a)), anchor="mm")
            d.text((mx + 74, y + dy + 29), it, font=bf, fill=fg + (int(255 * a),), anchor="lm")
            y += int(w * 0.092)
    else:
        a, dy = slide(0.45, 0.8)
        bf, bl, bs = _fit(d, c["body"], False, int(w * 0.052), int(w * 0.034), maxw, 9)
        y += dy
        for ln in bl:
            d.text((mx, y), ln, font=bf, fill=fg + (int(235 * a),))
            y += int(bs * 1.42)

    # pied
    a, _ = slide(0.8, 1.0)
    bar = CTA_BAR.get(c.get("cta"))
    bar_y = int(h * (0.77 if h / w > 1.6 else 0.905))  # video : au-dessus de la zone cachee par l'interface
    if bar:
        d.rounded_rectangle([mx, bar_y, w - mx, bar_y + int(w * 0.11)], radius=int(w * 0.03), fill=acc + (int(255 * a),))
        d.text((w // 2, bar_y + int(w * 0.0275)), bar[0], font=_font(True, int(w * 0.031)),
               fill=(10, 12, 20, int(255 * a)), anchor="mm")
        d.text((w // 2, bar_y + int(w * 0.078)), bar[1], font=_font(False, int(w * 0.032)),
               fill=(10, 12, 20, int(255 * a)), anchor="mm")
    else:
        d.text((mx, bar_y + int(w * 0.07)), "Un conseil de trading chaque jour", font=_font(False, int(w * 0.03)),
               fill=fg + (int(170 * a),), anchor="ls")
    return lay


def render_image(c, path, seed=None, size=(1080, 1350)):
    seed = random.randrange(10 ** 6) if seed is None else seed
    theme = THEMES[seed % len(THEMES)]
    w, h = size
    img = _background(w, h, theme, seed)
    img.alpha_composite(_text_layer(c, w, h, theme, 1.0))
    img.convert("RGB").save(path, quality=92)
    return path


def render_video(c, path, seed=None, seconds=8, fps=20, size=(1080, 1920)):
    ff = shutil.which("ffmpeg")
    if not ff:
        raise RuntimeError("ffmpeg introuvable")
    seed = random.randrange(10 ** 6) if seed is None else seed
    theme = THEMES[seed % len(THEMES)]
    w, h = size
    base = _background(w, h, theme, seed)
    tmp = tempfile.mkdtemp(prefix="socvid_")
    try:
        n = seconds * fps
        reveal = int(n * 0.6)  # texte complet apres 60 % puis maintien
        for i in range(n):
            p = min(1.0, i / reveal)
            fr = base.copy()
            # leger zoom lent du fond pour donner du mouvement
            z = 1 + 0.04 * i / n
            cw, ch = int(w / z), int(h / z)
            fr = fr.crop(((w - cw) // 2, (h - ch) // 2, (w + cw) // 2, (h + ch) // 2)).resize((w, h))
            fr.alpha_composite(_text_layer(c, w, h, theme, p))
            fr.convert("RGB").save(os.path.join(tmp, "f%04d.jpg" % i), quality=90)
        cmd = [ff, "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(tmp, "f%04d.jpg"),
               "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
               "-c:a", "aac", "-b:a", "96k", path]
        subprocess.run(cmd, check=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return path
