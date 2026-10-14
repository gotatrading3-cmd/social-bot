"""Videos 'motion design' (style TikTok pedagogique) : fond sombre, phrases courtes avec mot cle colore, schemas qui se construisent
au rythme de la voix, transitions fluides, 30 images par seconde. Moteur 100 % maison (Pillow + ffmpeg), voix Piper (voir social_explainer).

Un scenario = une suite de 'beats' (une phrase = un beat) + des 'elements' graphiques qui apparaissent a un beat donne et y restent
(ou jusqu'a un autre beat). Texte des beats : {r|mot} colore le mot (r rouge, b bleu, y jaune, g vert, w blanc)."""
import math, os, random, re, shutil, subprocess, tempfile, wave
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
W, H, S, FPS = 720, 1280, 2, 30           # unites de conception 720x1280, dessin en 2x puis reduction (bords lisses)
COL = dict(w=(245, 247, 250), r=(255, 90, 100), b=(76, 141, 255), y=(240, 185, 11), g=(25, 195, 125), m=(140, 155, 182))
BG_TOP, BG_BOT = (7, 10, 20), (14, 22, 42)
CAP_Y = 905            # haut de la zone de sous-titres (au-dessus de l'interface des reseaux)

_fonts = {}


def font(bold, size):
    k = (bold, size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(os.path.join(ASSETS, "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), int(size * S))
    return _fonts[k]


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def eo(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def eio(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def eb(x):  # pop avec leger depassement
    x = clamp(x)
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _c(color, a=1.0):
    return None if color is None else (color[0], color[1], color[2], int(255 * clamp(a)))


class Cv:
    """Dessin en unites de conception, sur une image 2x, avec transparence."""

    def __init__(self, im):
        self.im, self.d = im, ImageDraw.Draw(im, "RGBA")

    def rr(self, x0, y0, x1, y1, r, fill=None, outline=None, width=2, a=1.0):
        self.d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, fill=_c(fill, a), outline=_c(outline, a), width=max(1, int(width * S)))

    def circ(self, cx, cy, r, fill=None, outline=None, width=2, a=1.0):
        self.d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=_c(fill, a), outline=_c(outline, a), width=max(1, int(width * S)))

    def line(self, pts, color, width=3, a=1.0):
        self.d.line([(x * S, y * S) for x, y in pts], fill=_c(color, a), width=max(1, int(width * S)), joint="curve")

    def arc(self, cx, cy, r, a0, a1, color, width=6, a=1.0):
        self.d.arc([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], a0, a1, fill=_c(color, a), width=max(1, int(width * S)))

    def text(self, x, y, s, size, color, bold=True, anchor="mm", a=1.0):
        self.d.text((x * S, y * S), s, font=font(bold, size), fill=_c(color, a), anchor=anchor)

    def tw(self, s, size, bold=True):
        return font(bold, size).getlength(s) / S


# ------------------------------------------------------------------ fond
def make_bg():
    im = Image.new("RGB", (W * S, H * S))
    d = ImageDraw.Draw(im)
    for y in range(H * S):
        t = y / (H * S)
        d.line([(0, y), (W * S, y)], fill=mix(BG_TOP, BG_BOT, t))
    glow = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([W * S * 0.25, -H * S * 0.1, W * S * 1.2, H * S * 0.3], fill=(60, 110, 255, 34))
    im = Image.alpha_composite(im.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(160 * S / 2)))
    ov = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    g = ImageDraw.Draw(ov)
    for x in range(0, W, 60):  # grille tres discrete
        g.line([(x * S, 0), (x * S, H * S)], fill=(255, 255, 255, 9), width=S)
    for y in range(0, H, 60):
        g.line([(0, y * S), (W * S, y * S)], fill=(255, 255, 255, 9), width=S)
    im = Image.alpha_composite(im, ov)
    g = ImageDraw.Draw(im)
    logo = Image.open(os.path.join(ASSETS, "logo.png")).convert("RGBA")
    lw = 62 * S
    logo = logo.resize((lw, int(lw * logo.height / logo.width)))
    im.alpha_composite(logo, (34 * S, 34 * S))
    g.text((34 * S + lw + 12 * S, 34 * S + logo.height // 2), "GOTA TRADING", font=font(True, 19), fill=(240, 185, 11, 255), anchor="lm")
    return im.convert("RGB")


# ------------------------------------------------------------------ elements
def _alpha(el, t, T):
    """Opacite : apparition douce, disparition au debut du beat 'until'."""
    loc = t - T["start"][el["at"]] - el.get("delay", 0)
    a = eo(loc / 0.4)
    if el.get("until") is not None and el["until"] < len(T["start"]):
        a *= 1 - eo((t - T["start"][el["until"]]) / 0.35)
    return a, loc


def draw_candles(cv, el, t, T):
    a, loc = _alpha(el, t, T)
    if a <= 0:
        return
    rnd = random.Random(el.get("seed", 3))
    n, price = 26, 100.0
    x0, x1, y0, y1 = 50, 670, el.get("y", 190), el.get("y", 190) + 330
    series = []
    for i in range(n):
        o = price
        price += rnd.uniform(-12, 12)
        c = price
        series.append((o, max(o, c) + rnd.uniform(2, 9), min(o, c) - rnd.uniform(2, 9), c))
    lo, hi = min(s[2] for s in series), max(s[1] for s in series)
    sc = lambda p: y1 - (p - lo) / (hi - lo) * (y1 - y0)
    shown = int(n * eio(loc / 2.6)) + 1
    for i, (o, h, l, c) in enumerate(series[:shown]):
        x = x0 + (i + 0.5) * (x1 - x0) / n
        col = COL["g"] if c >= o else COL["r"]
        cv.line([(x, sc(h)), (x, sc(l))], col, 2.2, 0.8 * a)
        cv.rr(x - 6, sc(max(o, c)), x + 6, sc(min(o, c)) + 1, 2, fill=col, a=0.8 * a)
    for k, (i, txt, col) in enumerate(el.get("tags", [(8, "ACHAT", "g"), (15, "VENTE", "r"), (21, "ACHAT", "g")])):
        if i < shown and loc > 1.0 + k * 0.5:
            x = x0 + (i + 0.5) * (x1 - x0) / n
            y = sc(series[i][1]) - 26
            cv.rr(x - 30, y - 12, x + 30, y + 12, 5, fill=COL[col], a=0.25 * a, outline=COL[col], width=1.4)
            cv.text(x, y, txt, 11, COL[col], a=a)


def draw_bars(cv, el, t, T):
    a, loc = _alpha(el, t, T)
    if a <= 0:
        return
    x, y, w, h = el["x"], el["y"], el["w"], el["h"]
    pop = eb(loc / 0.45)
    cv.rr(x, y + (1 - pop) * 14, x + w, y + h + (1 - pop) * 14, 22, fill=(255, 255, 255), a=0.045 * a, outline=(255, 255, 255), width=1.4)
    cv.text(x + 22, y + 28, el["title"], 17, COL[el.get("tcol", "m")], anchor="lm", a=a)
    vals, n = el["values"], len(el["values"])
    bx0, bx1, base, top = x + 22, x + w - 150, y + h - 22, y + 56
    bw = (bx1 - bx0) / n
    c0, c1 = COL[el["c0"]], COL[el["c1"]]
    for i, v in enumerate(vals):
        p = eb((loc - 0.35 - i * 0.2) / 0.4)
        if p <= 0:
            continue
        hh = (base - top) * v * clamp(p, 0, 1.08)
        cv.rr(bx0 + i * bw + 3, base - hh, bx0 + (i + 1) * bw - 3, base, 4, fill=mix(c0, c1, i / max(1, n - 1)), a=a)
    fl = 0.35 + n * 0.2 + 0.25
    if loc > fl:
        pf = eb((loc - fl) / 0.5)
        col = COL[el["fcol"]]
        cv.text(x + w - 78, y + h / 2 - 8, el["final"], int(34 * clamp(pf, 0, 1.1)) or 1, col, a=a)
        cv.text(x + w - 78, y + h / 2 + 24, el.get("sub", "il reste"), 14, COL["m"], bold=False, a=a * clamp(pf))


def draw_week(cv, el, t, T):
    a, loc = _alpha(el, t, T)
    if a <= 0:
        return
    y, days = el["y"], el["days"]
    x0, x1 = 70, 650
    step = (x1 - x0) / (len(days) - 1)
    cv.line([(x0 - 30, y), (x1 + 30, y)], (255, 255, 255), 2, 0.25 * a)
    for i, d in enumerate(days):
        x = x0 + i * step
        cv.text(x, y - 74, d, 15, COL["m"], bold=False, a=a)
        cv.line([(x, y - 56), (x, y - 44)], (255, 255, 255), 2, 0.2 * a)
        cv.circ(x, y, 14, outline=COL["m"], width=1.6, a=0.45 * a)
    run = 0.0
    for tr in el["trades"]:
        tl = t - T["start"][tr["beat"]] - tr.get("delay", 0.25)
        if tl <= 0:
            continue
        x = x0 + tr["day"] * step
        p = eb(tl / 0.45)
        col = COL[tr["col"]]
        r = 34 * clamp(p, 0, 1.12)
        cv.circ(x, y, r + 8, fill=col, a=0.16 * a)
        cv.circ(x, y, r, fill=col, a=0.95 * a)
        cv.text(x, y, tr["text"], int(20 * clamp(p, 0.01, 1.1)), (255, 255, 255), a=a)


def draw_stat(cv, el, t, T):
    a, loc = _alpha(el, t, T)
    if a <= 0:
        return
    x, y = el["x"], el["y"]
    p = eb(loc / 0.5)
    cv.text(x, y - 46, el["label"], 15, COL["m"], a=a)
    sz = int(el.get("size", 58) * clamp(p, 0.01, 1.12))
    cv.text(x, y, el["text"], max(sz, 1), COL[el["col"]], a=a)


def draw_chip(cv, el, t, T):
    a, loc = _alpha(el, t, T)
    if a <= 0:
        return
    s = el["text"]
    w = cv.tw(s, 17) + 44
    x, y = W / 2, el["y"] + (1 - eo(loc / 0.4)) * 14
    cv.rr(x - w / 2, y - 22, x + w / 2, y + 22, 22, fill=COL[el.get("col", "b")], a=0.16 * a, outline=COL[el.get("col", "b")], width=1.6)
    cv.text(x, y, s, 17, COL[el.get("col", "b")], a=a)


def draw_big(cv, el, t, T):
    a, loc = _alpha(el, t, T)
    if a <= 0:
        return
    for k, ln in enumerate(el["lines"]):
        p = eo((loc - k * 0.18) / 0.5)
        cv.text(W / 2, el["y"] + k * el.get("lh", 80) + (1 - p) * 24, ln, el.get("size", 60), COL[el["cols"][k]], a=a * p)


def icon(cv, kind, cx, cy, a, p):
    if kind == "gauge":
        cv.arc(cx, cy + 6, 26, 180, 360, COL["m"], 5, a)
        cv.arc(cx, cy + 6, 26, 180, 180 + 60 * p, COL["y"], 5, a)
        ang = math.radians(180 + 60 * p)
        cv.line([(cx, cy + 6), (cx + 22 * math.cos(ang), cy + 6 + 22 * math.sin(ang))], COL["w"], 3, a)
        cv.circ(cx, cy + 6, 4, fill=COL["w"], a=a)
    elif kind == "stop":
        cv.line([(cx - 28, cy), (cx + 28, cy)], COL["r"], 4, a)
        cv.line([(cx - 8, cy - 22), (cx + 8, cy - 6)], COL["r"], 4, a * p)
        cv.line([(cx + 8, cy - 22), (cx - 8, cy - 6)], COL["r"], 4, a * p)
    elif kind == "lock":
        cv.arc(cx, cy - 6, 13, 180, 360, COL["g"], 5, a)
        cv.rr(cx - 20, cy - 6, cx + 20, cy + 24, 6, fill=COL["g"], a=a * (0.35 + 0.65 * p))
    elif kind == "book":
        cv.rr(cx - 22, cy - 26, cx + 22, cy + 26, 6, outline=COL["b"], width=3, a=a)
        for k in range(3):
            cv.line([(cx - 12, cy - 12 + k * 14), (cx - 12 + 24 * clamp(p * 3 - k), cy - 12 + k * 14)], COL["b"], 3, a)
    elif kind == "target":
        for r, al in ((26, 0.5), (17, 0.7), (8, 1)):
            cv.circ(cx, cy, r, outline=COL["y"], width=3, a=a * al)
        cv.line([(cx + 30 * (1 - p) + 2, cy - 30 * (1 - p) - 2), (cx, cy)], COL["w"], 3, a)
    elif kind == "count":
        cv.circ(cx, cy, 26, outline=COL["b"], width=3, a=a)
        cv.text(cx, cy, str(int(50 * p)), 20, COL["b"], a=a)


def draw_cards(cv, el, t, T):
    a, loc = _alpha(el, t, T)
    if a <= 0:
        return
    items = el["items"]
    y0 = el["y"]
    last = -1
    for i, it in enumerate(items):
        if t >= T["start"][it["beat"]]:
            last = i
    for i, it in enumerate(items):
        y = y0 + i * 118
        pin = eb((loc - 0.15 * i) / 0.5)
        revealed = t >= T["start"][it["beat"]] + 0.05
        rl = t - T["start"][it["beat"]]
        active = i == last
        col = COL[it["col"]]
        dx = (1 - clamp(pin)) * 60
        cv.rr(46 + dx, y, 674 + dx, y + 96, 18, fill=(255, 255, 255), a=(0.07 if active else 0.04) * a,
              outline=col if (active and revealed) else (255, 255, 255), width=2.4 if active else 1.2)
        cv.circ(86 + dx, y + 48, 20, outline=col if revealed else COL["m"], width=2.2, a=a)
        cv.text(86 + dx, y + 48, str(i + 1), 19, col if revealed else COL["m"], a=a)
        if revealed:
            pr = eo(rl / 0.5)
            cv.text(126 + dx, y + 48 + (1 - pr) * 10, it["title"], 22, COL["w"], anchor="lm", a=a * pr)
            icon(cv, it["icon"], 608 + dx, y + 48, a * pr, eo(rl / 0.9))
        else:
            cv.text(126 + dx, y + 48, "?", 26, COL["m"], anchor="lm", a=a * 0.7)


def draw_cta(cv, el, t, T):
    a, loc = _alpha(el, t, T)
    if a <= 0:
        return
    p = eb(loc / 0.6)
    y = el["y"]
    logo = Image.open(os.path.join(ASSETS, "logo.png")).convert("RGBA")
    lw = int(190 * S * clamp(p, 0.01, 1.05))
    logo = logo.resize((max(1, lw), max(1, int(lw * logo.height / logo.width))))
    if a < 1:
        logo.putalpha(logo.getchannel("A").point(lambda v: int(v * a)))
    cv.im.paste(logo, (int(W / 2 * S - lw / 2), int(y * S)), logo)
    cv.text(W / 2, y + 205, "GOTA TRADING", 34, COL["y"], a=a)
    q = eo((loc - 0.25) / 0.5)
    cv.rr(60, y + 250, W - 60, y + 360, 30, fill=COL["y"], a=a * q)
    cv.text(W / 2, y + 288, "Rejoins la communauté Telegram", 24, (10, 12, 20), a=a * q)
    cv.text(W / 2, y + 328, "Lien dans la bio  ·  @Gotatrade", 20, (10, 12, 20), bold=False, a=a * q)


DRAW = dict(candles=draw_candles, bars=draw_bars, week=draw_week, stat=draw_stat, chip=draw_chip, big=draw_big, cards=draw_cards, cta=draw_cta)


# ------------------------------------------------------------------ sous-titres
TAG = re.compile(r"\{(\w)\|([^}]*)\}")


def parse(text):
    """'Un {r|stop} posé' -> [('Un','w'),('stop','r'),('posé','w')]"""
    text = text.replace(" %", chr(160) + "%")
    out, pos = [], 0
    for m in TAG.finditer(text):
        out += [(w, "w") for w in text[pos:m.start()].split(" ") if w]
        out += [(w, m.group(1)) for w in m.group(2).split(" ") if w]
        pos = m.end()
    out += [(w, "w") for w in text[pos:].split(" ") if w]
    merged = []
    for w, c in out:  # la ponctuation reste collee au mot qui la precede
        if merged and all(ch in ".,;:?!" for ch in w):
            merged[-1] = (merged[-1][0] + w, merged[-1][1])
        else:
            merged.append((w, c))
    return merged


def layout(words, size=33, maxw=620):
    lines, cur, cw = [], [], 0
    sp = font(True, size).getlength(" ") / S
    for w, c in words:
        ww = font(True, size).getlength(w) / S
        if cur and cw + sp + ww > maxw:
            lines.append(cur)
            cur, cw = [], 0
        cur.append((w, c, ww))
        cw += (sp if len(cur) > 1 else 0) + ww
    if cur:
        lines.append(cur)
    out = []
    for li, ln in enumerate(lines):
        tot = sum(x[2] for x in ln) + sp * (len(ln) - 1)
        x = W / 2 - tot / 2
        for w, c, ww in ln:
            out.append((w, c, x + ww / 2, CAP_Y + 26 + li * 46))
            x += ww + sp
    return out


def draw_caption(cv, beat, t, T, i):
    tl = t - T["start"][i]
    if tl < 0:
        return
    words = beat["_layout"]
    span = max(0.5, beat["_audio"] * 0.9)
    tot = sum(len(w) + 1 for w, *_ in words)
    acc = 0
    fade = 1 - eo((tl - (T["dur"][i] - 0.2)) / 0.2) if tl > T["dur"][i] - 0.2 else 1
    for w, c, x, y in words:
        tw = 0.18 + acc / tot * span
        acc += len(w) + 1
        p = eo((tl - tw) / 0.14)
        if p <= 0:
            continue
        cv.text(x, y + (1 - p) * 8, w, 33, COL[c], a=p * fade)


# ------------------------------------------------------------------ rendu
def frame_job(args):
    scenario, T, frames, tmp = args
    bg = make_bg()
    n = len(T["start"])
    for k in frames:
        t = k / FPS
        im = bg.copy()
        cv = Cv(im)
        for el in scenario["elements"]:
            if t >= T["start"][el["at"]] + el.get("delay", 0):
                DRAW[el["type"]](cv, el, t, T)
        bi = max([i for i in range(n) if T["start"][i] <= t] or [0])
        draw_caption(cv, scenario["beats"][bi], t, T, bi)
        cv.rr(0, 0, W * t / T["total"], 5, 0, fill=COL["y"])
        im.resize((W, H), Image.LANCZOS).save(os.path.join(tmp, "f%05d.jpg" % k), quality=88)
    return len(frames)


def load_voice(src, dst, thr=0.012):
    """Lit un wav (n'importe quelle frequence), enleve les silences de debut et de fin, ecrit en 24000 Hz mono 16 bits."""
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-ac", "1", "-ar", "24000", "-sample_fmt", "s16", dst + ".tmp.wav"], check=True)
    with wave.open(dst + ".tmp.wav", "rb") as r:
        a = np.frombuffer(r.readframes(r.getnframes()), dtype="<i2")
    os.remove(dst + ".tmp.wav")
    env = np.abs(a.astype(float)) / 32768.0
    idx = np.where(env > thr)[0]
    if len(idx):
        a = a[max(0, idx[0] - 1200): idx[-1] + 2400]
    with wave.open(dst, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(a.tobytes())
    return len(a) / 24000, 24000


def render_motion(scenario, path, workers=6):
    import social_explainer as E
    import social_audio
    ff = shutil.which("ffmpeg")
    tmp = tempfile.mkdtemp(prefix="socmot_")
    try:
        beats = scenario["beats"]
        wavs, T = [], dict(start=[], dur=[])
        t = 0.45
        sr_ = 22050
        for i, b in enumerate(beats):
            wp = os.path.join(tmp, "v%02d.wav" % i)
            spoken = b.get("say") or TAG.sub(lambda m: m.group(2), b["text"])
            ext = os.path.join(scenario["voice_dir"], "%s_%02d.wav" % (scenario["key"], i)) if scenario.get("voice_dir") else None
            if ext and os.path.exists(ext):
                ad, sr_ = load_voice(ext, wp)   # voix clonee (fabriquee chez GitHub)
            else:
                ad, sr_ = E.tts(spoken, wp)
            b["_audio"] = ad
            b["_layout"] = layout(parse(b["text"]))
            wavs.append(wp)
            d = max(b.get("min", 2.4), ad + 0.4)
            T["start"].append(t)
            T["dur"].append(d)
            t += d
        T["total"] = t + 0.5
        voice = np.zeros(int(T["total"] * sr_ + sr_), dtype="<i2")
        for wp, st in zip(wavs, T["start"]):
            with wave.open(wp, "rb") as r:
                a = np.frombuffer(r.readframes(r.getnframes()), dtype="<i2")
            o = int((st + 0.08) * sr_)
            voice[o:o + len(a)] = a
        vpath = os.path.join(tmp, "voix.wav")
        with wave.open(vpath, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr_); w.writeframes(voice.tobytes())
        music = social_audio.make_wav(os.path.join(tmp, "musique.wav"), int(T["total"]) + 2, scenario.get("music", 0))
        total_frames = int(T["total"] * FPS)
        chunks = [list(range(i, total_frames, workers)) for i in range(workers)]
        with ProcessPoolExecutor(max_workers=workers) as ex:
            list(ex.map(frame_job, [(scenario, T, c, tmp) for c in chunks]))
        cmd = [ff, "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%05d.jpg"), "-i", vpath, "-i", music,
               "-filter_complex", "[1:a]volume=1.6,aresample=44100[v];[2:a]volume=0.12,aresample=44100[m];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
               "-map", "0:v", "-map", "[a]", "-t", "%.2f" % T["total"], "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
               "-movflags", "+faststart", "-c:a", "aac", "-b:a", "128k", path]
        subprocess.run(cmd, check=True)
        return T["total"]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
