"""Musique d'ambiance 100 % originale (synthese maison : aucun droit d'auteur, aucune bibliotheque externe)."""
import wave
import numpy as np

SR = 44100
PROGS = [  # suites d'accords (notes MIDI) : calme, pro, "lo-fi"
    [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)],
    [(50, 53, 57), (58, 62, 65), (53, 57, 60), (48, 52, 55)],
    [(52, 55, 59), (48, 52, 55), (45, 48, 52), (50, 54, 57)],
    [(55, 58, 62), (51, 55, 58), (53, 57, 60), (58, 62, 65)],
]


def _f(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def make_wav(path, seconds=8, variant=0):
    rnd = np.random.RandomState(variant * 7 + 3)
    prog = PROGS[variant % len(PROGS)]
    n = int(SR * seconds)
    t = np.arange(n) / SR
    out = np.zeros(n)
    seg = seconds / len(prog)
    for i, chord in enumerate(prog):
        a, b = int(i * seg * SR), int((i + 1) * seg * SR)
        tt = t[a:b] - t[a]
        env = np.minimum(1, tt / 0.6) * np.minimum(1, (seg - tt) / 0.8)
        for m in chord:
            for det, amp in ((0, 1.0), (0.004, 0.6)):
                f = _f(m) * (1 + det)
                out[a:b] += env * amp * (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt)) * 0.06
        out[a:b] += env * 0.10 * np.sin(2 * np.pi * _f(chord[0] - 12) * tt)  # basse douce
    # petit battement doux (grosse caisse tres discrete) a 80 bpm
    beat = 60 / 80
    for k in range(int(seconds / beat)):
        s = int(k * beat * SR)
        d = np.arange(int(0.22 * SR)) / SR
        kick = np.sin(2 * np.pi * (110 * np.exp(-d * 18) + 45) * d) * np.exp(-d * 14) * 0.22
        out[s:s + len(kick)] += kick[: max(0, n - s)] if s + len(kick) > n else kick
    out *= np.minimum(1, t / 0.3) * np.minimum(1, (seconds - t) / 1.2)
    out = out / max(1e-9, np.abs(out).max()) * 0.55
    data = (np.stack([out, out], axis=1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
    return path
