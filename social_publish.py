"""Publication Facebook (Page), Instagram (compte pro) et TikTok via leurs API officielles gratuites.
Aucun identifiant n'est ecrit dans le code : tout vient de variables d'environnement (secrets GitHub)."""
import os, time
import requests

GRAPH = "https://graph.facebook.com/" + os.environ.get("GRAPH_VERSION", "v23.0")
TIMEOUT = 120


class PublishError(Exception):
    pass


def _check(r, what):
    try:
        j = r.json()
    except Exception:
        j = {}
    if r.status_code >= 300 or "error" in j:
        err = j.get("error", {})
        msg = err.get("message") if isinstance(err, dict) else str(err)
        raise PublishError("%s : HTTP %s %s" % (what, r.status_code, (msg or r.text[:200])))
    return j


# ----------------------------------------------------------------- Facebook
class Facebook:
    name = "facebook"

    def __init__(self):
        self.page = os.environ.get("FB_PAGE_ID", "")
        self.token = os.environ.get("FB_PAGE_TOKEN", "")

    def enabled(self):
        return bool(self.page and self.token)

    def post_image(self, path, caption, url=None):
        with open(path, "rb") as f:
            r = requests.post("%s/%s/photos" % (GRAPH, self.page), data={"caption": caption, "access_token": self.token},
                              files={"source": f}, timeout=TIMEOUT)
        return _check(r, "Facebook photo").get("post_id") or "ok"

    def post_video(self, path, caption, url=None):
        with open(path, "rb") as f:
            r = requests.post("%s/%s/videos" % (GRAPH, self.page),
                              data={"description": caption, "access_token": self.token}, files={"source": f}, timeout=600)
        return _check(r, "Facebook video").get("id") or "ok"


# ----------------------------------------------------------------- Instagram
class Instagram:
    name = "instagram"

    def __init__(self):
        self.uid = os.environ.get("IG_USER_ID", "")
        self.token = os.environ.get("FB_PAGE_TOKEN", "")  # meme jeton que la Page

    def enabled(self):
        return bool(self.uid and self.token)

    def _publish(self, creation_id):
        r = requests.post("%s/%s/media_publish" % (GRAPH, self.uid),
                          data={"creation_id": creation_id, "access_token": self.token}, timeout=TIMEOUT)
        return _check(r, "Instagram publication").get("id") or "ok"

    def post_image(self, path, caption, url=None):
        if not url:
            raise PublishError("Instagram : il faut une adresse publique de l'image")
        r = requests.post("%s/%s/media" % (GRAPH, self.uid),
                          data={"image_url": url, "caption": caption, "access_token": self.token}, timeout=TIMEOUT)
        return self._publish(_check(r, "Instagram conteneur image")["id"])

    def post_video(self, path, caption, url=None):
        if not url:
            raise PublishError("Instagram : il faut une adresse publique de la video")
        r = requests.post("%s/%s/media" % (GRAPH, self.uid),
                          data={"media_type": "REELS", "video_url": url, "caption": caption, "share_to_feed": "true",
                                "access_token": self.token}, timeout=TIMEOUT)
        cid = _check(r, "Instagram conteneur reel")["id"]
        for _ in range(40):  # jusqu'a ~5 min de traitement
            time.sleep(8)
            s = requests.get("%s/%s" % (GRAPH, cid), params={"fields": "status_code,status", "access_token": self.token},
                             timeout=TIMEOUT).json()
            code = s.get("status_code")
            if code == "FINISHED":
                return self._publish(cid)
            if code in ("ERROR", "EXPIRED"):
                raise PublishError("Instagram traitement video : %s" % s.get("status", code))
        raise PublishError("Instagram : traitement video trop long")


# ----------------------------------------------------------------- TikTok
class TikTok:
    """Publie des VIDEOS. Tant que l'application TikTok n'est pas auditee par TikTok, les videos arrivent en PRIVE
    (TIKTOK_PRIVACY=SELF_ONLY) : c'est la regle de TikTok, pas une limite du bot."""
    name = "tiktok"

    def __init__(self, refresh_override=None):
        self.key = os.environ.get("TIKTOK_CLIENT_KEY", "")
        self.secret = os.environ.get("TIKTOK_CLIENT_SECRET", "")
        self.refresh = refresh_override or os.environ.get("TIKTOK_REFRESH_TOKEN", "")
        self.privacy = os.environ.get("TIKTOK_PRIVACY", "SELF_ONLY")
        self.new_refresh = None

    def enabled(self):
        return bool(self.key and self.secret and self.refresh)

    def _access(self):
        r = requests.post("https://open.tiktokapis.com/v2/oauth/token/",
                          data={"client_key": self.key, "client_secret": self.secret, "grant_type": "refresh_token",
                                "refresh_token": self.refresh},
                          headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=TIMEOUT)
        j = _check(r, "TikTok jeton")
        if "access_token" not in j:
            raise PublishError("TikTok jeton : %s" % str(j)[:200])
        if j.get("refresh_token") and j["refresh_token"] != self.refresh:
            self.new_refresh = j["refresh_token"]
            self.refresh = self.new_refresh
        return j["access_token"]

    def post_image(self, path, caption, url=None):
        return None  # TikTok : videos seulement (les photos exigent un domaine verifie)

    def post_video(self, path, caption, url=None):
        tok = self._access()
        size = os.path.getsize(path)
        body = {"post_info": {"title": caption[:2000], "privacy_level": self.privacy, "disable_duet": False,
                              "disable_comment": False, "disable_stitch": False},
                "source_info": {"source": "FILE_UPLOAD", "video_size": size, "chunk_size": size, "total_chunk_count": 1}}
        r = requests.post("https://open.tiktokapis.com/v2/post/publish/video/init/", json=body,
                          headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json; charset=UTF-8"},
                          timeout=TIMEOUT)
        j = _check(r, "TikTok init")
        if j.get("error", {}).get("code", "ok") != "ok":
            raise PublishError("TikTok init : %s" % j["error"])
        up, pid = j["data"]["upload_url"], j["data"]["publish_id"]
        with open(path, "rb") as f:
            data = f.read()
        r = requests.put(up, data=data, headers={"Content-Type": "video/mp4", "Content-Length": str(size),
                                                 "Content-Range": "bytes 0-%d/%d" % (size - 1, size)}, timeout=600)
        if r.status_code >= 300:
            raise PublishError("TikTok envoi video : HTTP %s %s" % (r.status_code, r.text[:200]))
        return pid
