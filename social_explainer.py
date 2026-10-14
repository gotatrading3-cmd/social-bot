"""Videos explicatives (40-60 s) : voix off francaise + schemas animes + sous-titres. Chaque video resout UN probleme precis.
Voix : Piper, voix 'siwis' (licence CC BY 4.0, Universite d'Edimbourg). Tout le reste est dessine par le programme."""
import os, random, shutil, subprocess, tempfile, wave
from PIL import Image, ImageDraw
import social_render as sr
import social_audio
from social_content import TG_HANDLE

HERE = os.path.dirname(os.path.abspath(__file__))
VOICE = os.path.join(HERE, "voix", "fr_FR-siwis-medium.onnx")
W, H = 1080, 1920
FPS = 20
THEME = sr.THEMES[0]
BG, _, ACC, FG = THEME[0], THEME[1], THEME[2], THEME[3]
UP, DOWN = (0, 214, 143), (255, 90, 100)

_voice = None


import re
# Prononciation : la voix lit "trader" comme "trade-é" ; on ecrit les mots comme ils se disent (les sous-titres gardent l'orthographe)
PRON = [
    (r"\btraders?\b", "trédeur"), (r"\btrades?\b", "tréd"), (r"\btrading\b", "trédine"), (r"\bspreads?\b", "sprède"),
    (r"\bpips\b", "pipsse"), (r"\bstop-loss\b", "stop loss"), (r"\bTelegram\b", "Télégrame"), (r"\bforex\b", "forèx"),
    (r"Ethereum", "Éthéréomme"), (r"stablecoins?", "stable coïne"), (r"Bitcoin", "Bitcoïne"), (r"blockchain", "bloc chaîne"), (r"1 000", "mille"), (r"1:2", "un pour deux"), (r"%", " pour cent"), (r"€", " euros"), (r"÷", "divisé par"),
]


def say(text):
    for pat, rep in PRON:
        text = re.sub(pat, rep, text, flags=re.I)
    return text


def tts(text, path):
    global _voice
    text = say(text)
    from piper import PiperVoice
    if _voice is None:
        _voice = PiperVoice.load(VOICE)
    with wave.open(path, "wb") as w:
        try:
            from piper import SynthesisConfig
            _voice.synthesize_wav(text, w, syn_config=SynthesisConfig(length_scale=1.08))
        except ImportError:
            _voice.synthesize_wav(text, w)
    with wave.open(path, "rb") as r:
        return r.getnframes() / r.getframerate(), r.getframerate()


# ------------------------------------------------------------------ graphique de bougies
def candles():
    closes = [48, 51, 54, 57, 60, 62, 64, 66, 65, 60, 50, 43, 46, 48, 50, 51, 52, 54, 54, 55]
    rnd = random.Random(5)
    out, prev = [], 47
    for i, c in enumerate(closes):
        o = prev
        hi = max(o, c) + rnd.uniform(1.5, 3.5)
        lo = min(o, c) - rnd.uniform(1.0, 3.0)
        if i == 11:
            lo = 40.5
        out.append((o, hi, lo, c))
        prev = c
    return out


CANDLES = candles()
PMIN, PMAX = 28, 100
CX0, CX1 = 90, W - 90
CY0, CY1 = int(H * 0.19), int(H * 0.60)


_C, _PMIN, _PMAX = CANDLES, PMIN, PMAX


def py(price):
    return CY1 - (price - _PMIN) / (_PMAX - _PMIN) * (CY1 - CY0)


def px(i):
    return CX0 + (i + 0.5) * (CX1 - CX0) / len(_C)


def series(closes, seed=5, lows=None, highs=None):
    """Fabrique des bougies (ouverture, haut, bas, cloture) a partir d'une suite de cloture."""
    rnd = random.Random(seed)
    out, prev = [], closes[0] - 2
    for i, c in enumerate(closes):
        o = prev
        hi = max(o, c) + rnd.uniform(1.0, 3.0)
        lo = min(o, c) - rnd.uniform(1.0, 3.0)
        if lows and i in lows:
            lo = lows[i]
        if highs and i in highs:
            hi = highs[i]
        out.append((o, hi, lo, c))
        prev = c
    return out


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def pill(d, x, y, text, color, size=34, alpha=255, anchor="l"):
    f = sr._font(True, size)
    tw = d.textlength(text, font=f)
    x0 = x if anchor == "l" else x - tw - 40
    d.rounded_rectangle([x0, y - size, x0 + tw + 40, y + size * 0.55], radius=18, fill=color + (alpha,))
    d.text((x0 + 20, y - size * 0.22), text, font=f, fill=(10, 12, 20, alpha), anchor="lm")


def draw_chart(d, sc, p):
    global _C, _PMIN, _PMAX
    _C = sc.get("candles", CANDLES)
    _PMIN, _PMAX = sc.get("range", (PMIN, PMAX))
    n = len(_C)
    shown = n if not sc.get("grow") else int(n * ease(p / 0.55)) + 1
    # grille discrete
    for k in range(5):
        y = CY0 + k * (CY1 - CY0) / 4
        d.line([(CX0, y), (CX1, y)], fill=(255, 255, 255, 18), width=2)
    bw = (CX1 - CX0) / n * 0.62
    for i, (o, h, l, c) in enumerate(_C[:shown]):
        col = UP if c >= o else DOWN
        x = px(i)
        d.line([(x, py(h)), (x, py(l))], fill=col + (255,), width=5)
        d.rectangle([x - bw / 2, py(max(o, c)), x + bw / 2, py(min(o, c)) + 3], fill=col + (255,))
    for lv in sc.get("levels", []):
        a = ease((p - lv["t0"]) / 0.18)
        if a <= 0:
            continue
        y = py(lv["price"])
        x_end = CX0 + (CX1 - CX0) * (0.04 + 0.96 * a)
        dash = 26
        x = CX0
        while x < x_end:
            d.line([(x, y), (min(x + dash, x_end), y)], fill=lv["color"] + (int(255 * a),), width=6)
            x += dash * 1.7
        pill(d, CX1 - 10, y - 8, lv["label"], lv["color"], 34, int(255 * a), anchor="r")
    for m in sc.get("marks", []):
        a = ease((p - m["t0"]) / 0.15)
        if a <= 0:
            continue
        pr = m.get("price")
        if pr is None:
            pr = _C[m["idx"]][2] if m.get("at", "low") == "low" else _C[m["idx"]][1]
        x, y = px(m["idx"]), py(pr)
        r = 34 + 14 * (1 - a)
        d.ellipse([x - r, y - r, x + r, y + r], outline=m["color"] + (int(255 * a),), width=7)
        pill(d, max(CX0, min(x + 50, CX1 - 300)), y + (70 if m.get("at", "low") == "low" else -45), m["label"], m["color"], 32, int(255 * a))
    if sc.get("arrow"):
        a = ease((p - sc["arrow"]["t0"]) / 0.2)
        if a > 0:
            y0, y1 = py(sc["arrow"]["p0"]), py(sc["arrow"]["p1"])
            x = CX1 - 50
            d.line([(x, y0), (x, y0 + (y1 - y0) * a)], fill=FG + (int(220 * a),), width=8)
            d.text((x - 20, (y0 + y1) / 2), sc["arrow"]["label"], font=sr._font(True, 36), fill=FG + (int(255 * a),), anchor="rm")


OUTRO_TEXT = ("Tu veux progresser avec nous ? Rejoins notre communauté Telegram, le lien est dans la bio. "
              "On y échange en temps réel, pour avancer ensemble vers la liberté financière.")

# ------------------------------------------------------------------ scenes
def label_pill(d, text, y):
    pill(d, 80, y, text, ACC, 34)


def draw_title(d, text, y, size=0.082, maxlines=4, a=1.0):
    f, ls, s = sr._fit(d, text, True, int(W * size), int(W * 0.05), W - 160, maxlines)
    for ln in ls:
        d.text((80, y), ln, font=f, fill=FG + (int(255 * a),))
        y += int(s * 1.25)
    return y


def visual(sc, p, lay):
    d = ImageDraw.Draw(lay)
    kind = sc["visual"]
    if kind == "hook":
        label_pill(d, sc.get("label", "LE PROBLÈME"), int(H * 0.2))
        y = draw_title(d, sc["title"], int(H * 0.25), 0.092, 5, ease(p / 0.2))
        d.rectangle([80, y + 20, 80 + int(W * 0.2 * ease(p / 0.5)), y + 28], fill=ACC + (255,))
        q = ease(p / 0.4)
        d.text((W // 2, int(H * 0.54)), "?", font=sr._font(True, int(300 + 30 * q)), fill=ACC + (int(70 * q),), anchor="mm")
    elif kind == "chart":
        label_pill(d, sc.get("label", "EXEMPLE"), int(H * 0.145))
        draw_chart(d, sc, p)
    elif kind in ("steps", "recap"):
        label_pill(d, sc.get("label", "À RETENIR" if kind == "recap" else "LES ÉTAPES"), int(H * 0.16))
        y = draw_title(d, sc["title"], int(H * 0.2), 0.07, 2)
        y += 40
        for i, it in enumerate(sc["items"]):
            a = ease((p - 0.15 - i * 0.14) / 0.14)
            dy = int((1 - a) * 30)
            d.ellipse([80, y + dy, 80 + 62, y + dy + 62], fill=ACC + (int(255 * a),))
            d.text((111, y + dy + 33), str(i + 1) if kind == "steps" else "✓", font=sr._font(True, 38), fill=(10, 12, 20, int(255 * a)), anchor="mm")
            f, ls, s = sr._fit(d, it, False, int(W * 0.052), int(W * 0.04), W - 270, 2)
            for j, ln in enumerate(ls):
                d.text((172, y + dy + 6 + j * int(s * 1.2)), ln, font=f, fill=FG + (int(255 * a),))
            y += 105 + (len(ls) - 1) * int(s * 1.2)
    elif kind == "formula":
        label_pill(d, sc.get("label", "LA FORMULE"), int(H * 0.2))
        a = ease(p / 0.25)
        d.rounded_rectangle([80, int(H * 0.27), W - 80, int(H * 0.27) + 330], radius=36, fill=(255, 255, 255, int(28 * a)),
                            outline=ACC + (int(255 * a),), width=5)
        y = int(H * 0.27) + 60
        for ln in sc["formula"]:
            f, ls, s = sr._fit(d, ln, True, int(W * 0.066), int(W * 0.04), W - 200, 2)
            for l2 in ls:
                d.text((W // 2, y), l2, font=f, fill=FG + (int(255 * a),), anchor="mm")
                y += int(s * 1.3)
        a2 = ease((p - 0.35) / 0.25)
        f, ls, s = sr._fit(d, sc["example"], False, int(W * 0.048), int(W * 0.038), W - 160, 4)
        yy = int(H * 0.27) + 400
        for ln in ls:
            d.text((80, yy), ln, font=f, fill=FG + (int(230 * a2),))
            yy += int(s * 1.4)
    elif kind == "anatomy":
        label_pill(d, sc.get("label", "LA BOUGIE"), int(H * 0.16))
        bull = sc.get("bull", True)
        col = UP if bull else DOWN
        cx = int(W * 0.30)
        top, bot = int(H * 0.27), int(H * 0.62)
        hi_y, lo_y = top, bot
        b1, b2 = int(H * 0.37), int(H * 0.52)  # corps
        grow = ease(p / 0.25)
        d.line([(cx, hi_y), (cx, lo_y)], fill=col + (int(255 * grow),), width=10)
        d.rectangle([cx - 70, b1, cx + 70, b2], fill=col + (int(255 * grow),))
        names = sc["names"]  # [haut, cloture, ouverture, bas] ou inverse selon sens
        ys = [hi_y, b1 if bull else b2, b2 if bull else b1, lo_y]
        # si bougie baissiere : ouverture en haut du corps, cloture en bas
        for i, (nm, yy) in enumerate(zip(names, ys)):
            a = ease((p - 0.2 - i * 0.14) / 0.12)
            if a <= 0:
                continue
            d.line([(cx + (10 if i in (0, 3) else 70), yy), (int(W * 0.52), yy)], fill=FG + (int(180 * a),), width=4)
            pill(d, int(W * 0.53), yy + 12, nm, ACC, 38, int(255 * a))
    elif kind == "compare":
        label_pill(d, sc.get("label", "COMPARAISON"), int(H * 0.15))
        y0 = int(H * 0.19)
        for k, card in enumerate(sc["cards"]):
            a = ease((p - 0.1 - k * 0.35) / 0.18)
            dy = int((1 - a) * 40)
            hgt = int(H * 0.255)
            yy = y0 + k * (hgt + 30) + dy
            d.rounded_rectangle([80, yy, W - 80, yy + hgt], radius=32, fill=(255, 255, 255, int(24 * a)), outline=card["color"] + (int(255 * a),), width=5)
            pill(d, 110, yy + 62, card["title"], card["color"], 38, int(255 * a))
            ty = yy + 100
            for ln in card["lines"]:
                d.text((112, ty), ln, font=sr._font(False, int(W * 0.042)), fill=FG + (int(240 * a),))
                ty += int(W * 0.062)
            d.text((112, yy + hgt - 88), card["result"], font=sr._font(True, int(W * 0.046)), fill=card["color"] + (int(255 * a),))
    elif kind == "bigstat":
        label_pill(d, sc.get("label", "LE CHIFFRE"), int(H * 0.2))
        a = ease(p / 0.3)
        f, ls, sz = sr._fit(d, sc["value"], True, int(W * 0.17), int(W * 0.08), W - 160, 2)
        y = int(H * 0.30)
        for ln in ls:
            d.text((W // 2, y), ln, font=f, fill=ACC + (int(255 * a),), anchor="ma")
            y += int(sz * 1.2)
        a2 = ease((p - 0.3) / 0.3)
        f2, l2, s2 = sr._fit(d, sc["caption"], False, int(W * 0.052), int(W * 0.038), W - 200, 5)
        y += 50
        for ln in l2:
            d.text((W // 2, y), ln, font=f2, fill=FG + (int(240 * a2),), anchor="ma")
            y += int(s2 * 1.4)
    elif kind == "outro":
        a = ease(p / 0.3)
        logo = Image.open(os.path.join(sr.ASSETS, "logo.png")).convert("RGBA")
        lw = int(W * 0.30)
        logo = logo.resize((lw, int(lw * logo.height / logo.width)))
        lay.alpha_composite(logo, (W // 2 - lw // 2, int(H * 0.22)))
        y = int(H * 0.22) + logo.height + 60
        d.text((W // 2, y), sr.BRAND, font=sr._font(True, 64), fill=ACC + (int(255 * a),), anchor="mm")
        a2 = ease((p - 0.2) / 0.25)
        d.rounded_rectangle([80, y + 90, W - 80, y + 290], radius=40, fill=ACC + (int(255 * a2),))
        d.text((W // 2, y + 150), "Rejoins notre communauté Telegram", font=sr._font(True, 40), fill=(10, 12, 20, int(255 * a2)), anchor="mm")
        d.text((W // 2, y + 225), "Lien dans la bio  ·  " + TG_HANDLE, font=sr._font(False, 42), fill=(10, 12, 20, int(255 * a2)), anchor="mm")


def subtitle(d, text, a):
    f, ls, s = sr._fit(d, text, True, int(W * 0.048), int(W * 0.03), W - 200, 6)
    h = len(ls) * int(s * 1.35) + 50
    y0 = int(H * 0.735)
    d.rounded_rectangle([60, y0, W - 60, y0 + h], radius=28, fill=(5, 8, 16, int(185 * a)))
    y = y0 + 25
    for ln in ls:
        d.text((W // 2, y), ln, font=f, fill=(255, 255, 255, int(255 * a)), anchor="ma")
        y += int(s * 1.35)


def frame(base, sc, p, t, dur, idx, total_t, total_dur):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    visual(sc, p, lay)
    fade = ease(t / 0.35) * (1 - ease((t - (dur - 0.25)) / 0.25) * 0.0)
    if fade < 1:
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * fade)))
    fr = base.copy()
    fr.alpha_composite(lay)
    d = ImageDraw.Draw(fr)
    if True:
        lay2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        subtitle(ImageDraw.Draw(lay2), sc["text"], fade)
        fr.alpha_composite(lay2)
    d.rectangle([0, 0, int(W * total_t / total_dur), 10], fill=ACC + (255,))
    return fr.convert("RGB")


def still(sc, p, path):
    base = sr._background(W, H, THEME, 7)
    frame(base, sc, p, 5.0, 8.0, 0, 3.0, 10.0).save(path)


def render_explainer(script, path, fps=FPS):
    ff = shutil.which("ffmpeg")
    if not ff:
        raise RuntimeError("ffmpeg introuvable")
    tmp = tempfile.mkdtemp(prefix="socexp_")
    try:
        scenes = list(script["scenes"]) + [dict(visual="outro", text=OUTRO_TEXT)]
        durs, wavs, sr_ = [], [], 22050
        for i, sc in enumerate(scenes):
            if sc.get("fixed"):
                durs.append(sc["fixed"])
                wavs.append(None)
                continue
            wp = os.path.join(tmp, "v%02d.wav" % i)
            ad, sr_ = tts(sc["text"], wp)
            wavs.append(wp)
            durs.append(max(3.2, ad + 0.55))
        # piste voix : chaque voix est posee au debut de sa scene, silence ensuite
        import numpy as np
        voice = np.zeros(int(sum(durs) * sr_ + sr_), dtype="<i2")
        pos = 0
        for wp, dur in zip(wavs, durs):
            if wp:
                with wave.open(wp, "rb") as r:
                    a = np.frombuffer(r.readframes(r.getnframes()), dtype="<i2")
                voice[pos + int(0.15 * sr_): pos + int(0.15 * sr_) + len(a)] = a
            pos += int(dur * sr_)
        vpath = os.path.join(tmp, "voix.wav")
        with wave.open(vpath, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr_); w.writeframes(voice.tobytes())
        total = sum(durs)
        music = social_audio.make_wav(os.path.join(tmp, "musique.wav"), int(total) + 2, script.get("music", 0))
        base = sr._background(W, H, THEME, script.get("seed", 7))
        k, elapsed = 0, 0.0
        for i, (sc, dur) in enumerate(zip(scenes, durs)):
            nfr = int(dur * fps)
            for j in range(nfr):
                t = j / fps
                frame(base, sc, t / dur, t, dur, i, elapsed + t, total).save(os.path.join(tmp, "f%05d.jpg" % k), quality=88)
                k += 1
            elapsed += dur
        cmd = [ff, "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(tmp, "f%05d.jpg"),
               "-i", vpath, "-i", music, "-filter_complex",
               "[1:a]volume=1.6,aresample=44100[v];[2:a]volume=0.13,aresample=44100[m];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
               "-map", "0:v", "-map", "[a]", "-t", "%.2f" % total, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
               "-movflags", "+faststart", "-c:a", "aac", "-b:a", "128k", path]
        subprocess.run(cmd, check=True)
        return total
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------------ scenario de test
RED, GREEN = DOWN, UP
STOP_SCRIPT = dict(
    key="stop-loss",
    title="Où placer son stop-loss ?",
    music=2, seed=7,
    scenes=[
        dict(visual="hook", title="Ton stop saute, puis le prix repart dans ton sens ?",
             text="Ton stop-loss saute, puis le prix repart exactement dans ton sens ? Ce n'est pas de la malchance. C'est presque toujours un problème de placement."),
        dict(visual="chart", grow=True, label="L'ERREUR",
             levels=[dict(price=47, label="Stop au hasard", color=RED, t0=0.55)],
             marks=[dict(idx=11, price=40.5, label="Stop touché", color=RED, t0=0.8)],
             text="Beaucoup de traders placent leur stop à une distance choisie au hasard, vingt pips par exemple. Mais le marché ne connaît pas ce chiffre : il va chercher les zones où il y a des ordres."),
        dict(visual="chart", label="ÉTAPE 1",
             marks=[dict(idx=11, price=40.5, label="Dernier creux", color=ACC, t0=0.25)],
             text="Première étape : repère le dernier creux logique, l'endroit où les acheteurs sont déjà intervenus."),
        dict(visual="chart", label="ÉTAPE 2",
             marks=[dict(idx=11, price=40.5, label="Dernier creux", color=ACC, t0=0.0)],
             levels=[dict(price=35.5, label="Stop logique", color=RED, t0=0.3)],
             text="Deuxième étape : place ton stop juste en dessous, avec une petite marge pour le spread et les mèches. Si ce niveau casse, ton idée de départ n'est plus valable."),
        dict(visual="chart", label="ÉTAPE 3",
             levels=[dict(price=35.5, label="Stop", color=RED, t0=0.0), dict(price=55, label="Entrée", color=FG, t0=0.0),
                     dict(price=94, label="Objectif 1:2", color=GREEN, t0=0.35)],
             arrow=dict(p0=55, p1=35.5, label="1", t0=0.2),
             text="Troisième étape : fixe ton objectif. Vise au moins deux fois la distance de ton stop. Ainsi, tu peux avoir tort une fois sur deux et rester gagnant."),
        dict(visual="formula", label="ÉTAPE 4", formula=["Taille = risque en € ÷ distance du stop"],
             example="Avec un compte de 1 000 et un risque de 1 %, tu risques 10 sur ce trade. Plus ton stop est loin, plus ta position doit être petite.",
             text="Dernière étape : adapte la taille de ta position à la distance du stop, jamais l'inverse. C'est elle qui garde ton risque fixe, trade après trade."),
        dict(visual="recap", title="Pour résumer", label="À RETENIR",
             items=["Stop derrière un niveau logique", "Une petite marge pour les mèches", "Objectif d'au moins 2 fois le risque", "Taille de position calculée"],
             text="En résumé : un stop derrière un niveau logique, une petite marge, un objectif au moins double, et une taille de position calculée."),
    ])

SCRIPTS = [STOP_SCRIPT]

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "apercu", "explicatif_test.mp4")
    print("duree %.1f s" % render_explainer(STOP_SCRIPT, out))
