"""Assistant (a lancer par TOI sur ton PC) : transforme ton jeton Meta temporaire en jeton durable pour la Page Facebook,
trouve l'identifiant Instagram, puis enregistre le tout directement dans les secrets GitHub du depot.
Les valeurs secretes ne sont jamais affichees ni ecrites dans un fichier. Usage :  python configurer_reseaux.py  DEPOT (ex: gotatrading3-cmd/social-bot)"""
import getpass, subprocess, sys
import requests

G = "https://graph.facebook.com/v23.0"


def secret(repo, name, value):
    subprocess.run(["gh", "secret", "set", name, "--repo", repo], input=value.encode(), check=True)
    print("  enregistre :", name)


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage : python configurer_reseaux.py  proprietaire/depot")
    repo = sys.argv[1]
    print("Colle les valeurs demandees (rien ne s'affiche a l'ecran, c'est normal).")
    app_id = getpass.getpass("ID de l'application Meta : ").strip()
    app_secret = getpass.getpass("Cle secrete de l'application : ").strip()
    short = getpass.getpass("Jeton temporaire (Graph API Explorer) : ").strip()
    r = requests.get(G + "/oauth/access_token", params={"grant_type": "fb_exchange_token", "client_id": app_id,
                     "client_secret": app_secret, "fb_exchange_token": short}, timeout=60).json()
    if "access_token" not in r:
        sys.exit("Echec : %s" % r.get("error", {}).get("message", r))
    pages = requests.get(G + "/me/accounts", params={"access_token": r["access_token"], "limit": 50}, timeout=60).json().get("data", [])
    if not pages:
        sys.exit("Aucune Page Facebook trouvee pour ce compte (as-tu coche ta Page dans l'autorisation ?).")
    for i, p in enumerate(pages):
        print("  %d) %s" % (i + 1, p["name"]))
    p = pages[int(input("Numero de la Page a utiliser : ")) - 1]
    secret(repo, "FB_PAGE_ID", p["id"])
    secret(repo, "FB_PAGE_TOKEN", p["access_token"])
    ig = requests.get("%s/%s" % (G, p["id"]), params={"fields": "instagram_business_account", "access_token": p["access_token"]},
                      timeout=60).json().get("instagram_business_account", {}).get("id")
    if ig:
        secret(repo, "IG_USER_ID", ig)
    else:
        print("  Instagram : aucun compte professionnel relie a cette Page (relie-le dans les parametres de la Page, puis relance).")
    print("Termine. Facebook :", "OK", "| Instagram :", "OK" if ig else "pas relie")


if __name__ == "__main__":
    main()
