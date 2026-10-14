import sys, social_motion as M, social_motion_scripts2 as MS2
if __name__ == "__main__":
    keys = sys.argv[1:]
    for s in MS2.MOTION2:
        if s["key"] in keys:
            s["voice_dir"] = None   # voix de secours locale : controle visuel seulement
            print(s["key"], round(M.render_motion(s, "test_visuel/%s.mp4" % s["key"])), "s", flush=True)
