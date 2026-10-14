"""Fabrique les videos motion : python rendre_motion.py [cle ...]  ->  lot_explicatifs/ (numeros a partir de 26)"""
import os, sys, time
import social_motion as M, social_motion_scripts as MS, social_motion_scripts2 as MS2, social_content as sc

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    d = os.path.join(here, "lot_explicatifs")
    keys = sys.argv[1:]
    nl = chr(10)
    sep = nl + "=" * 40 + nl
    for i, s in enumerate(MS.MOTION + MS2.MOTION2):
        if keys and s["key"] not in keys:
            continue
        c = dict(kind="explicatif", title=s["title"], body=s["summary"], topic=s["topic"], cta="tg")
        base = os.path.join(d, "%02d_%s" % (26 + i, s["key"]))
        vd = os.path.join(here, "voix_clonee")
        if os.path.isdir(vd) and not os.environ.get("SOCIAL_VOIX_PIPER"):
            s["voice_dir"] = vd   # voix clonee du proprietaire si disponible
        t0 = time.time()
        dur = M.render_motion(s, base + ".mp4")
        with open(base + ".txt", "w", encoding="utf-8") as f:
            f.write("FACEBOOK" + sep + sc.caption(c, "fb") + nl + nl)
            f.write("INSTAGRAM" + sep + sc.caption(c, "ig") + nl + nl)
            f.write("TIKTOK" + sep + sc.caption(c, "tt") + nl)
        print("pret %s : %.0f s de video en %.0f s de calcul" % (base, dur, time.time() - t0), flush=True)
