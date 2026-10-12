"""Chef d'orchestre : choisit le contenu, fabrique l'image/la video, publie sur Facebook / Instagram / TikTok.

  python social_runner.py --preview 6     -> fabrique 6 posts d'essai dans apercu/ (rien n'est envoye)
  python social_runner.py --once          -> un cycle : publie SI c'est l'heure (au moins SOCIAL_GAP_MIN minutes depuis le dernier)
  python social_runner.py --once --force  -> publie tout de suite

Securite : sans la variable SOCIAL_LIVE=true, --once ne publie RIEN (il fabrique le post dans apercu/ et l'indique).
Variables : SOCIAL_GAP_MIN (170), SOCIAL_MAX_PER_DAY (6), SOCIAL_HOURS ("6-22", heures UTC), SOCIAL_VIDEO_EVERY (1 = que des videos),
SOCIAL_STATE_DIR (dossier de l'etat), SOCIAL_MEDIA_DIR + GITHUB_REPOSITORY (hebergement des fichiers pour Instagram).
"""
import argparse, base64, hashlib, json, os, random, subprocess, sys, time, datetime as dt
import requests

import social_content as sc
import social_render as sr
import social_publish as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "apercu")
SEQ = ["motivation", "conseil", "stat", "regle", "mythe", "motivation", "conseil", "question", "stat", "regle", "mythe", "conseil"]


def env(name, default):
    v = os.environ.get(name, "")
    return v.strip() if v and v.strip() else default


def log(*a):
    print(dt.datetime.utcnow().strftime("%H:%M:%S"), *a, flush=True)


# ------------------------------------------------------------------ etat
def state_path():
    return os.path.join(env("SOCIAL_STATE_DIR", HERE), "social_state.json")


def load_state():
    try:
        with open(state_path(), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"n": 0, "last": 0, "posts_today": {}, "recent": [], "history": []}


def save_state(st):
    st["history"] = st["history"][-200:]
    tmp = state_path() + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=1)
    os.replace(tmp, state_path())


def _fernet():
    k = os.environ.get("SOCIAL_STATE_KEY", "").strip()
    if not k:
        return None
    from cryptography.fernet import Fernet
    return Fernet(k.encode())


# ------------------------------------------------------------------ choix du contenu
def pick(st, rnd=None):
    rnd = rnd or random.Random()
    kind = SEQ[st["n"] % len(SEQ)]
    cta = sc.CTA_SEQ[st["n"] % len(sc.CTA_SEQ)]
    for _ in range(40):
        c = sc.make(kind, rnd)
        c["cta"] = cta
        key = hashlib.sha1((c["kind"] + c["title"] + c.get("body", "")).encode()).hexdigest()[:12]
        if key not in st["recent"]:
            st["recent"] = (st["recent"] + [key])[-150:]
            return c
    st["recent"] = st["recent"][-20:]  # bibliotheque epuisee : on repart, la mise en page change de toute facon
    c = sc.make(kind, rnd)
    c["cta"] = cta
    return c


def want_video(st):
    every = int(env("SOCIAL_VIDEO_EVERY", "1"))
    return every > 0 and st["n"] % every == every - 1


# ------------------------------------------------------------------ hebergement du fichier (Instagram veut une adresse publique)
def host(path):
    d = env("SOCIAL_MEDIA_DIR", "")
    repo = env("GITHUB_REPOSITORY", "")
    if not d or not repo:
        return None
    name = "%d_%s" % (int(time.time()), os.path.basename(path))
    dst = os.path.join(d, name)
    with open(path, "rb") as a, open(dst, "wb") as b:
        b.write(a.read())
    files = sorted(f for f in os.listdir(d) if f[:1].isdigit())
    for old in files[:-12]:
        os.remove(os.path.join(d, old))

    def git(*a):
        subprocess.run(["git", "-C", d] + list(a), check=True, capture_output=True)
    git("config", "user.name", "social-bot[bot]")
    git("config", "user.email", "social-bot@users.noreply.github.com")
    git("add", "-A")
    git("commit", "-q", "--amend", "-m", "media")
    git("push", "-q", "--force", "origin", "HEAD:media")
    url = "https://raw.githubusercontent.com/%s/media/%s" % (repo, name)
    for _ in range(30):
        try:
            if requests.head(url, timeout=15).status_code == 200:
                return url
        except Exception:
            pass
        time.sleep(4)
    raise sp.PublishError("fichier non accessible publiquement : " + url)


# ------------------------------------------------------------------ cycle
def due(st, force):
    now = time.time()
    if force:
        return True
    gap = int(env("SOCIAL_GAP_MIN", "170")) * 60
    if now - max(st.get("last", 0), st.get("last_try", 0) - gap + 600) < gap:
        return False
    h = dt.datetime.utcnow().hour
    a, b = [int(x) for x in env("SOCIAL_HOURS", "6-22").split("-")]
    if not (a <= h <= b):
        return False
    day = dt.datetime.utcnow().strftime("%Y-%m-%d")
    return st["posts_today"].get(day, 0) < int(env("SOCIAL_MAX_PER_DAY", "6"))


def run_once(force=False):
    st = load_state()
    if not due(st, force):
        log("pas l'heure : rien a faire")
        return 0
    live = env("SOCIAL_LIVE", "false").lower() == "true"
    if not live and os.environ.get("GITHUB_ACTIONS"):
        log("SOCIAL_LIVE n'est pas 'true' : rien a faire (mode veille)")
        return 0
    os.makedirs(OUT, exist_ok=True)
    video = want_video(st)
    c = pick(st)
    seed = random.randrange(10 ** 6)
    stamp = dt.datetime.utcnow().strftime("%Y%m%d_%H%M")
    path = os.path.join(OUT, "post_%s.%s" % (stamp, "mp4" if video else "png"))
    try:
        (sr.render_video if video else sr.render_image)(c, path, seed=seed)
    except Exception as e:
        log("ERREUR fabrication :", e)
        st["last_try"] = time.time()
        save_state(st)
        return 1
    log("fabrique : %s '%s' (%s)" % (c["kind"], c["title"], "video" if video else "image"))

    ff = None
    # TikTok : le jeton de renouvellement peut avoir tourne -> copie chiffree dans l'etat
    tt_refresh = None
    f = _fernet()
    if f and st.get("tt_refresh"):
        try:
            tt_refresh = f.decrypt(st["tt_refresh"].encode()).decode()
        except Exception:
            tt_refresh = None
    tt = sp.TikTok(tt_refresh)
    platforms = [("fb", sp.Facebook()), ("ig", sp.Instagram()), ("tt", tt)]
    if not live:
        log("MODE ESSAI (SOCIAL_LIVE n'est pas 'true') : rien n'est publie. Fichier : " + path)
        for k, p in platforms:
            log("  %s %s : %s" % (p.name, "pret" if p.enabled() else "pas configure", "oui" if (video or k != "tt") else "(video seulement)"))
        return 0

    url = None
    ok = 0
    results = {}
    for k, p in platforms:
        if not p.enabled():
            continue
        if k == "tt" and not video:
            continue
        try:
            if k == "ig" and url is None:
                url = host(path)
            cap = sc.caption(c, k)
            res = (p.post_video if video else p.post_image)(path, cap, url)
            results[p.name] = "ok"
            ok += 1
            log("publie sur", p.name, res)
        except Exception as e:
            results[p.name] = "erreur"
            log("ECHEC", p.name, ":", str(e)[:300])
    if tt.new_refresh and f:
        st["tt_refresh"] = f.encrypt(tt.new_refresh.encode()).decode()
    now = time.time()
    if ok:
        day = dt.datetime.utcnow().strftime("%Y-%m-%d")
        st["posts_today"] = {day: st["posts_today"].get(day, 0) + 1}
        st["last"] = now
        st["n"] += 1
        st["history"].append({"t": int(now), "kind": c["kind"], "title": c["title"], "video": video, "res": results})
    else:
        st["last_try"] = now  # echec partout : on reessaie dans ~10 min, pas en boucle
    save_state(st)
    try:
        os.remove(path)
    except OSError:
        pass
    return 0 if ok or not any(p.enabled() for _, p in platforms) else 1


def preview(n):
    os.makedirs(OUT, exist_ok=True)
    st = {"n": 0, "recent": []}
    for i in range(n):
        st["n"] = i
        video = want_video(st)
        c = pick(st)
        p = os.path.join(OUT, "essai_%02d_%s.%s" % (i + 1, c["kind"], "mp4" if video else "png"))
        (sr.render_video if video else sr.render_image)(c, p, seed=i * 7 + 1)
        log(p)
        print("   Facebook :", sc.caption(c, "fb").replace("\n", " | ")[:160])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--preview", type=int, default=0)
    a = ap.parse_args()
    if a.preview:
        preview(a.preview)
    elif a.once:
        sys.exit(run_once(a.force))
    else:
        ap.print_help()
