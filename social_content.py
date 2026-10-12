"""Bibliotheque de contenus (francais, trading uniquement). Tout est ecrit pour ce projet.
Aucune fausse statistique : les chiffres sont soit des calculs mathematiques exacts, soit des regles generales.
Chaque element : dict(kind, title, body, tag)  ->  kind in motivation | conseil | regle | mythe | stat | question
"""
import random

MOTIVATION = [
    ("La discipline bat le talent", "Un trader moyen discipliné finit devant un génie qui n'écoute que ses émotions."),
    ("Un trade ne définit pas ta carrière", "Une perte est un coût d'activité. Ce qui compte : la série de 100 trades, pas le dernier."),
    ("Patience", "Le marché te paie pour attendre le bon setup, pas pour cliquer tout le temps."),
    ("Protège ton capital", "Tu ne peux pas saisir une opportunité si ton compte est à zéro. Survivre d'abord."),
    ("Le plan avant le clic", "Entrée, stop, objectif : écrits avant d'entrer. Jamais pendant."),
    ("Les pertes font partie du jeu", "Même les meilleurs traders perdent souvent. Ils perdent petit et gagnent plus gros."),
    ("Un jour à la fois", "Pas besoin d'être riche cette semaine. Il faut être meilleur qu'hier."),
    ("Ton plus grand adversaire", "Ce n'est pas le marché. C'est l'impatience, la peur et l'envie de se refaire."),
    ("Moins de trades, plus de qualité", "Les meilleurs jours sont souvent ceux où tu as eu le courage de ne rien faire."),
    ("La régularité construit tout", "Petit risque, même méthode, des centaines de fois. C'est ça, l'avantage."),
    ("Apprendre ne s'arrête jamais", "Chaque trade, gagnant ou perdant, mérite une ligne dans ton journal."),
    ("Reste calme quand ça bouge", "Les décisions prises dans la panique coûtent plus cher que le marché lui-même."),
    ("Le journal de trading", "Ce que tu ne mesures pas, tu ne peux pas l'améliorer. Note tout."),
    ("Se lever, analyser, appliquer", "Une routine solide vaut mieux qu'une inspiration passagère."),
    ("Le succès est lent", "Les traders qui durent construisent pendant des années, pas pendant des semaines."),
    ("Accepte le risque", "Si un trade te fait trembler, la taille de position est trop grosse."),
    ("Sois ton propre risk manager", "Personne ne protégera ton compte à ta place."),
    ("Ne cours pas après le marché", "Une opportunité manquée ne coûte rien. Un trade forcé coûte cher."),
    ("Progresser > gagner", "Un trade bien exécuté qui perd vaut mieux qu'un trade mal exécuté qui gagne."),
    ("Respecte ton stop", "Déplacer son stop pour « laisser une chance » est la façon la plus rapide de vider un compte."),
    ("Éteins l'écran quand il faut", "Après une série de pertes, la meilleure décision est de fermer la plateforme."),
    ("Ta mentalité est ton edge", "Deux traders, même stratégie : celui qui reste calme gagne."),
    ("Construire en silence", "Les résultats parlent plus fort que les captures d'écran."),
    ("Commence petit", "Un petit lot appliqué avec rigueur apprend plus qu'un gros lot appliqué avec peur."),
    ("Chaque expert a débuté", "Les débuts sont des erreurs payées une fois. Apprends vite, ne les répète pas."),
    ("Pense en probabilités", "Aucun trade n'est sûr. Tu cherches un avantage répété, pas une certitude."),
    ("La constance", "La constance ennuyeuse bat l'excitation chaque semaine."),
    ("Réveille-toi, trader", "Le marché récompense ceux qui se préparent avant l'ouverture."),
    ("Le temps est ton allié", "Laisse le plan travailler. Ne le sabote pas toutes les cinq minutes."),
    ("Fais confiance au processus", "Ce n'est pas un seul trade, c'est ton processus qui te rendra rentable."),
]

CONSEILS = [
    ("Risque 1 % maximum par trade", "Avec 1 % de risque, il faut dix pertes d'affilée pour perdre environ 10 %. Ton compte respire."),
    ("Un ratio gain/risque d'au moins 1:2", "Avec 1:2, tu peux perdre plus d'un trade sur deux et rester rentable."),
    ("Trade dans le sens de la tendance", "Regarde d'abord la plus grande unité de temps. Aller contre elle demande de bien meilleures raisons."),
    ("Évite les annonces à fort impact", "NFP, inflation, taux : les spreads s'élargissent et les mouvements deviennent brutaux. Attends la fin."),
    ("Place ton stop à un endroit logique", "Derrière un plus bas ou un plus haut, pas à une distance choisie au hasard."),
    ("Ne risque pas plus après une perte", "Doubler pour « se refaire » est exactement ce qui détruit les comptes."),
    ("Limite tes paires", "Mieux vaut bien connaître 3 instruments que mal en suivre 20."),
    ("Prépare ta journée la veille", "Niveaux clés, calendrier économique, scénarios : tout est noté avant l'ouverture."),
    ("Teste sur démo avant le réel", "Une stratégie non testée est une hypothèse, pas un plan."),
    ("Calcule ta taille de position", "Taille = risque en € ÷ distance du stop. Jamais au feeling."),
    ("Ne trade pas fatigué", "La fatigue réduit la patience et augmente les erreurs. Dors, puis trade."),
    ("Prends des profits partiels", "Sécuriser une partie à 1R aide à rester serein pour laisser courir le reste."),
    ("Trop de trades = trop de frais", "Spreads et commissions s'accumulent. Moins de trades de qualité gardent plus de gains."),
    ("Un seul setup à maîtriser", "Deviens excellent sur une configuration avant d'en ajouter une autre."),
    ("Zones plutôt que lignes", "Support et résistance sont des zones. Laisse de la place au prix."),
    ("Confirme avant d'entrer", "Une bougie de confirmation coûte quelques pips mais évite beaucoup de faux départs."),
    ("Fais une revue chaque dimanche", "Relis tes trades de la semaine : erreurs répétées, bons réflexes, ajustements."),
    ("Évite le levier excessif", "Le levier n'augmente pas ton avantage, seulement la vitesse à laquelle tu gagnes ou perds."),
    ("Surveille les sessions", "Londres et New York concentrent la liquidité. L'Asie est souvent plus calme."),
    ("Ne change pas de stratégie chaque semaine", "Il faut au moins 50 à 100 trades pour juger une méthode."),
    ("Aie un stop de la journée", "Deux ou trois pertes, tu arrêtes. Le marché sera là demain."),
    ("Écris pourquoi tu entres", "Si tu ne peux pas l'expliquer en une phrase, ne prends pas le trade."),
    ("Respire avant de cliquer", "Trois secondes de pause évitent beaucoup d'entrées impulsives."),
    ("Regarde le spread", "Un spread élevé mange ton ratio gain/risque avant même que le trade démarre."),
    ("Ne laisse pas un gain devenir une perte", "Avance ton stop à l'entrée quand le prix a assez progressé, selon ton plan."),
    ("Choisis ton horizon", "Scalping, day trading ou swing : mélanger les trois dans la même journée crée la confusion."),
    ("Évite le week-end non préparé", "Les écarts de réouverture peuvent dépasser ton stop. Réduis ou clôture avant."),
    ("Garde ton plan simple", "Moins d'indicateurs, plus de lecture du prix. La complexité n'est pas un avantage."),
    ("Mesure ton taux de réussite ET ton ratio", "L'un sans l'autre ne dit rien. C'est l'espérance qui compte."),
]

REGLES = [
    ("Les 5 règles d'or", ["Risque 1 % maximum", "Stop avant l'entrée", "Un plan écrit", "Jamais de revanche", "Un journal tenu"]),
    ("Checklist avant d'entrer", ["Tendance claire ?", "Zone importante ?", "Stop logique ?", "Ratio ≥ 1:2 ?", "Pas d'annonce proche ?"]),
    ("Routine du trader sérieux", ["Calendrier économique", "Niveaux du jour", "Scénarios A et B", "Taille de position", "Journal en fin de journée"]),
    ("Après une perte", ["Respire", "Ne double pas", "Relis ton plan", "Note l'erreur éventuelle", "Reprends si le setup est valide"]),
    ("Ce qui fait durer un trader", ["Capital protégé", "Régularité", "Émotions maîtrisées", "Apprentissage continu", "Patience"]),
    ("Avant de passer en réel", ["Démo rentable sur la durée", "Plan testé", "Risque défini", "Capital que tu peux perdre", "Journal en place"]),
    ("Les erreurs du débutant", ["Trop de levier", "Pas de stop", "Trop de trades", "Suivre les rumeurs", "Vouloir se refaire"]),
    ("Gérer ses émotions", ["Taille de position réduite", "Pauses régulières", "Sport et sommeil", "Pas de trade en colère", "Accepter la perte"]),
    ("Lire un graphique", ["Tendance", "Structure", "Zones clés", "Bougies de confirmation", "Volatilité"]),
    ("Bien finir sa semaine", ["Relire les trades", "Compter les erreurs", "Fixer 1 objectif", "Se reposer", "Préparer lundi"]),
]

MYTHES = [
    ("Il faut gagner presque tout le temps", "Une méthode à 40 % de réussite et un ratio 1:2 est déjà rentable. Le ratio compte autant que le taux."),
    ("Plus on trade, plus on gagne", "Plus on trade, plus on paie de frais et plus on fait d'erreurs. La qualité prime."),
    ("Il existe un indicateur magique", "Aucun indicateur ne prédit l'avenir. La gestion du risque pèse plus que l'outil."),
    ("Le trading est de l'argent facile", "C'est un métier de patience et de discipline. Les gains rapides sont rares, les pertes rapides sont courantes."),
    ("Un stop-loss est un signe de faiblesse", "Un stop est une assurance. Sans lui, un seul trade peut effacer des mois de travail."),
    ("Le levier rend riche", "Le levier amplifie les gains ET les pertes. Mal utilisé, il accélère la ruine."),
    ("Les pros ne perdent jamais", "Tous les pros perdent régulièrement. Ils limitent chaque perte et suivent leur plan."),
    ("Il faut un gros capital pour commencer", "Il faut surtout apprendre la gestion du risque. Un petit compte sert à s'entraîner sans se mettre en danger."),
    ("Se refaire vite après une perte", "La revanche mène à des positions trop grosses. Ralentis, ne double pas."),
    ("Suivre les signaux sans comprendre", "Un signal sans compréhension ni gestion du risque reste un pari. Apprends pourquoi le trade existe."),
]

QUESTIONS = [
    "Quelle est ta plus grande erreur en trading cette semaine ? Dis-le en commentaire, on apprend ensemble.",
    "Tu trades plutôt le matin, l'après-midi ou le soir ? Réponds en commentaire.",
    "Ta paire ou ton actif préféré ? Écris-le ci-dessous.",
    "Stop-loss toujours posé ou parfois oublié ? Sois honnête, personne ne te juge.",
    "Quelle règle de trading t'a le plus aidé ? Partage-la avec la communauté.",
    "Combien de trades prends-tu en moyenne par jour ? Dis-nous en commentaire.",
    "Tu tiens un journal de trading ? Oui ou non ?",
    "Ton plus gros défi : la patience, la peur ou la discipline ?",
    "Day trading, swing ou scalping : ton style ?",
    "Quelle est la première chose que tu regardes sur un graphique ?",
    "Qu'est-ce qui te motive à continuer à apprendre le trading ?",
    "Un conseil que tu donnerais à un débutant ? Écris-le.",
]


def fr(x, d=0):
    """Nombre au format francais : 10 000 / 0,5"""
    s = ("%." + str(d) + "f") % x
    if "." in s:
        a, b = s.split(".")
        b = b.rstrip("0")
    else:
        a, b = s, ""
    a = "{:,}".format(int(a)).replace(",", " ")
    return a + ("," + b if b else "")


def _pct_recovery():
    loss = random.choice([10, 20, 25, 30, 40, 50, 60, 75])
    need = loss / (100 - loss) * 100
    return ("Perdre %d %%, c'est devoir regagner %s %%" % (loss, fr(need)),
            "Après une baisse de %d %%, il faut +%s %% pour revenir à zéro. Les grosses pertes sont très difficiles à rattraper." % (loss, fr(need, 1)))


def _streak():
    r = random.choice([1, 2, 3, 5])
    n = random.choice([5, 10, 15, 20])
    left = 100 * (1 - r / 100) ** n
    return ("%d pertes de suite à %s %% de risque" % (n, fr(r, 1)),
            "Il te reste %s %% de ton capital. Avec un petit risque, une mauvaise série ne détruit pas ton compte." % fr(left, 1))


def _rr():
    ratio = random.choice([1.5, 2, 3])
    be = 100 / (1 + ratio)
    return ("Ratio 1:%s : il suffit de gagner %s %%" % (fr(ratio, 1), fr(be)),
            "Avec un gain moyen de %s fois ta perte moyenne, tu n'as besoin de gagner que %s %% de tes trades pour ne pas perdre (hors frais)." % (fr(ratio, 1), fr(be)))


def _compound():
    pct = random.choice([1, 2, 3, 5])
    m = random.choice([6, 12, 24])
    v = 100 * (1 + pct / 100) ** m
    return ("+%d %% par mois pendant %d mois" % (pct, m),
            "100 deviennent %s en théorie. Mais la régularité est difficile : vise d'abord ne pas perdre, ensuite construire." % fr(v))


def _risk_unit():
    cap = random.choice([500, 1000, 2000, 5000, 10000])
    r = random.choice([0.5, 1, 2])
    return ("Risquer %s %% d'un compte de %s" % (fr(r, 1), fr(cap)),
            "C'est %s par trade au maximum. C'est cette limite, pas l'objectif de gain, qui garde ton compte en vie." % fr(cap * r / 100, 1))


STATS = [_pct_recovery, _streak, _rr, _compound, _risk_unit]

# Hashtags
TAGS_FB = "#trading #forex #bourse #tradingtips #discipline"
TAGS_IG = ("#trading #forex #trader #tradingfrancais #bourse #motivation #investissement #bitcoin #crypto "
           "#tradingforex #gestiondurisque #mindsettrader #apprendreletrading #tradingdebutant")
TAGS_TT = "#trading #forex #trader #tradingtips #motivation #bourse #fyp"

KINDS = ["motivation", "conseil", "stat", "regle", "mythe", "question"]


def make(kind, rng=None):
    """Retourne un dict de contenu; rng = random.Random pour reproductibilite (apercu)."""
    rnd = rng or random
    if kind == "motivation":
        t, b = rnd.choice(MOTIVATION)
        return dict(kind=kind, title=t, body=b, label="MOTIVATION")
    if kind == "conseil":
        t, b = rnd.choice(CONSEILS)
        return dict(kind=kind, title=t, body=b, label="CONSEIL TRADING")
    if kind == "stat":
        state = random.getstate()
        if rng:
            random.setstate(rng.getstate())
        t, b = rnd.choice(STATS)()
        if rng:
            rng.setstate(random.getstate())
        random.setstate(state)
        return dict(kind=kind, title=t, body=b, label="LE CHIFFRE")
    if kind == "regle":
        t, items = rnd.choice(REGLES)
        return dict(kind=kind, title=t, items=items, body=" · ".join(items), label="CHECKLIST")
    if kind == "mythe":
        t, b = rnd.choice(MYTHES)
        return dict(kind=kind, title="Mythe : " + t, body=b, label="MYTHE OU RÉALITÉ")
    q = rnd.choice(QUESTIONS)
    return dict(kind="question", title="À toi la parole", body=q, label="COMMUNAUTÉ")


import os

TG_LINK = os.environ.get("SOCIAL_CTA_LINK", "https://t.me/Gotatrade")
TG_HANDLE = os.environ.get("SOCIAL_CTA_HANDLE", "@Gotatrade")


def cta(platform):
    if platform == "fb":
        return "📲 Pour apprendre plus de compétences en trading, rejoins-nous gratuitement sur Telegram : " + TG_LINK
    return "📲 Pour apprendre plus en trading, rejoins-nous gratuitement sur Telegram : lien dans la bio (%s)" % TG_HANDLE


def caption(c, platform):
    tags = {"fb": TAGS_FB, "ig": TAGS_IG, "tt": TAGS_TT}[platform]
    if c["kind"] == "regle":
        core = c["title"] + " :\n" + "\n".join("✅ " + i for i in c["items"])
    else:
        core = c["title"] + "\n\n" + c["body"]
    if platform == "tt":
        core = c["title"] + " — " + c["body"] if c["kind"] != "regle" else core
    return core.strip() + "\n\n" + tags
