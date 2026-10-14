"""Fabrique la 2e serie de videos explicatives dans lot_explicatifs/ (numeros a partir de 15) : python lot_nouveau.py"""
import os, sys, social_scripts2, social_content as sc, social_runner as r

HERE = os.path.dirname(os.path.abspath(__file__))
d = os.path.join(HERE, "lot_explicatifs")
start = int(sys.argv[1]) if len(sys.argv) > 1 else 15
nl = chr(10)
sep = nl + "=" * 40 + nl
for i, script in enumerate(social_scripts2.SCRIPTS2):
    c = dict(kind="explicatif", title=script["title"], body=script["summary"], topic=script["topic"], cta="tg")
    base = os.path.join(d, "%02d_%s" % (start + i, script["key"]))
    if os.path.exists(base + ".mp4"):
        continue
    r.render_video_post({}, base + ".mp4", c, script)
    with open(base + ".txt", "w", encoding="utf-8") as f:
        f.write("FACEBOOK" + sep + sc.caption(c, "fb") + nl + nl)
        f.write("INSTAGRAM" + sep + sc.caption(c, "ig") + nl + nl)
        f.write("TIKTOK" + sep + sc.caption(c, "tt") + nl)
    r.log("pret :", base + ".mp4")
