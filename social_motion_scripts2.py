"""Serie 2 des videos 'motion' : 10 sujets (trading + crypto). Aucune promesse de gain, chiffres verifies (levier 100 : 1 % = toute la marge).
Syntaxe : voir social_motion.py. Les beats 'text' sont lus par la voix clonee (les mots sont reecrits comme ils se prononcent par social_explainer.say)."""
from social_motion_scripts import CTA_TEXT

PATH_STOP = [50, 54, 58, 62, 60, 55, 50, 44, 46, 50, 53, 57, 60, 63, 66]
PATH_TREND = [40, 44, 48, 52, 49, 45, 43, 47, 52, 57, 61, 58, 54, 52, 56, 62, 67, 71, 68, 64, 62, 66, 72, 77]
PATH_RANGE = [50, 56, 62, 66, 63, 58, 52, 47, 44, 48, 54, 60, 65, 67, 62, 56, 50, 46, 45, 49, 55, 61, 65, 68]
PATH_FOMO = [50, 50, 51, 52, 52, 54, 58, 64, 72, 80, 86, 84, 76, 68, 60, 54]

STOP = dict(
    key="stop-loss-placement", topic="trading", title="Où placer ton stop-loss ?",
    summary="Un stop au hasard saute souvent pour rien. Trois étapes pour le placer derrière un niveau logique.", music=1,
    beats=[
        dict(text="Ton {r|stop} saute, puis le prix repart dans ton sens ?"),
        dict(text="Ce n'est pas de la malchance. C'est un problème de {y|placement}."),
        dict(text="Erreur : un stop {r|au hasard}, à une distance fixe.", min=3.2),
        dict(text="Le marché ne connaît pas ton chiffre. Il cherche les {b|zones}.", min=3.2),
        dict(text="Première étape : repère le dernier {y|creux}."),
        dict(text="Deuxième étape : place ton stop {r|juste en dessous}."),
        dict(text="Troisième étape : vise au moins {g|deux fois} la distance.", min=3.2),
        dict(text="Alors, trois règles à retenir."),
        dict(text="Un : un {r|stop} derrière un niveau logique."),
        dict(text="Deux : une petite {y|marge} pour les mèches."),
        dict(text="Trois : la taille de position selon {b|ton stop}."),
        dict(text=CTA_TEXT, min=3.4),
    ],
    elements=[
        dict(type="levels", at=1, until=7, y=210, h=380, path=PATH_STOP, range=(34, 84), dur=3.2,
             hlines=[dict(v=47, beat=2, col="r", text="Stop au hasard"), dict(v=40, beat=5, col="r", text="Stop logique"),
                     dict(v=53, beat=6, col="w", text="Entrée", delay=0.2), dict(v=79, beat=6, col="g", text="Objectif : 2 × le risque", delay=1.4)],
             marks=[dict(i=7, beat=2, col="r", text="Stop touché", delay=1.6), dict(i=7, beat=4, col="y", text="Dernier creux", below=False)]),
        dict(type="cards", at=7, until=11, y=200,
             items=[dict(beat=8, title="Stop derrière un niveau", icon="stop", col="r"),
                    dict(beat=9, title="Marge pour les mèches", icon="shield", col="y"),
                    dict(beat=10, title="Taille selon ton stop", icon="gauge", col="b")]),
        dict(type="cta", at=11, y=190, delay=0.5),
    ])

LEVIER = dict(
    key="levier-danger", topic="trading", title="Le levier peut vider ton compte en une bougie",
    summary="Le levier amplifie les gains comme les pertes. Un exemple chiffré et trois règles pour l'utiliser sans te brûler.", music=3,
    beats=[
        dict(text="Le {r|levier} peut vider ton compte en quelques minutes."),
        dict(text="Il {y|amplifie} tout : les gains, mais aussi les pertes."),
        dict(text="Exemple : un levier de {y|100}, et {b|100 dollars} de marge.", min=3.4),
        dict(text="Tu contrôles une position de {b|10 000 dollars}.", min=3.0),
        dict(text="Le prix baisse d'{r|1 %}. Ça fait {r|100 dollars} de perte.", min=3.6),
        dict(text="Toute ta marge a disparu. En {r|une seule} bougie.", min=3.2),
        dict(text="Pour l'utiliser sans te brûler, trois règles."),
        dict(text="Un : un levier {g|faible} au départ."),
        dict(text="Deux : un {r|stop} toujours posé."),
        dict(text="Trois : risque {y|1 %} de ton capital, pas plus."),
        dict(text="Le levier n'est pas un cadeau. C'est un {r|amplificateur}.", min=3.4),
        dict(text=CTA_TEXT, min=3.4),
    ],
    elements=[
        dict(type="stat", at=2, until=6, x=190, y=300, label="MARGE", text="100 $", col="b", size=64),
        dict(type="stat", at=3, until=6, x=530, y=300, label="POSITION", text="10 000 $", col="b", size=56),
        dict(type="stat", at=4, until=6, x=190, y=480, label="BAISSE DU PRIX", text="-1 %", col="r", size=64),
        dict(type="stat", at=4, until=6, x=530, y=480, label="PERTE", text="-100 $", col="r", size=64, delay=1.4),
        dict(type="big", at=5, until=6, y=660, lines=["MARGE : 0 $"], cols=["r"], size=58),
        dict(type="cards", at=6, until=10, y=200,
             items=[dict(beat=7, title="Levier faible", icon="gauge", col="g"),
                    dict(beat=8, title="Stop toujours posé", icon="stop", col="r"),
                    dict(beat=9, title="1 % de risque", icon="target", col="y")]),
        dict(type="big", at=10, until=11, y=330, lines=["LE LEVIER", "AMPLIFIE TOUT"], cols=["w", "r"], size=66, lh=100),
        dict(type="cta", at=11, y=190, delay=0.5),
    ])

SPREAD = dict(
    key="spread-cout-cache", topic="trading", title="Le spread : le coût caché de chaque trade",
    summary="Tu paies un coût dès l'ouverture. Comment le comprendre et le réduire.", music=2,
    beats=[
        dict(text="Tu ouvres un trade et tu es déjà en {r|perte} ?"),
        dict(text="Ce n'est pas un bug. C'est le {y|spread}."),
        dict(text="Il y a un prix d'{g|achat} et un prix de {r|vente}.", min=3.2),
        dict(text="L'écart entre les deux, c'est le {y|spread}."),
        dict(text="Et tu le paies à {r|chaque} trade."),
        dict(text="Dix trades par jour, deux pips d'écart : {r|vingt pips} de frais.", min=3.8),
        dict(text="Comment le réduire ? Trois réflexes."),
        dict(text="Un : trade les paires {g|liquides}."),
        dict(text="Deux : évite les {r|annonces}."),
        dict(text="Trois : moins de trades, plus de {b|qualité}."),
        dict(text=CTA_TEXT, min=3.4),
    ],
    elements=[
        dict(type="stat", at=2, until=6, x=190, y=300, label="PRIX D'ACHAT", text="1,1002", col="g", size=54),
        dict(type="stat", at=2, until=6, x=530, y=300, label="PRIX DE VENTE", text="1,1000", col="r", size=54, delay=1.2),
        dict(type="chip", at=3, until=6, y=420, text="écart = spread = 2 pips", col="y"),
        dict(type="stat", at=5, until=6, x=360, y=620, label="10 TRADES × 2 PIPS", text="20 pips", col="r", size=78),
        dict(type="cards", at=6, until=10, y=200,
             items=[dict(beat=7, title="Paires liquides", icon="chart", col="g"),
                    dict(beat=8, title="Pas d'annonces", icon="clock", col="r"),
                    dict(beat=9, title="Moins de trades", icon="check", col="b")]),
        dict(type="cta", at=10, y=190, delay=0.5),
    ])

EMOTIONS = dict(
    key="trois-pertes", topic="trading", title="Trois pertes de suite : que faire ?",
    summary="Le moment le plus dangereux de ta journée. Deux réactions possibles et un plan anti-revanche.", music=0,
    beats=[
        dict(text="Trois pertes de suite. Tu sens l'envie de te {r|refaire}."),
        dict(text="C'est le moment le plus {r|dangereux} de ta journée."),
        dict(text="Première réaction : tu {r|augmentes} ta taille.", min=3.0),
        dict(text="Résultat : la perte {r|grossit}."),
        dict(text="Deuxième réaction : tu {g|t'arrêtes}.", min=3.0),
        dict(text="Le compte {g|respire}. Ton esprit aussi."),
        dict(text="Ton plan anti-revanche, en trois règles."),
        dict(text="Un : une {y|limite} de pertes par jour."),
        dict(text="Deux : tu {r|fermes} la plateforme."),
        dict(text="Trois : tu {b|notes} ce qui s'est passé."),
        dict(text="Le marché sera là {g|demain}. Ton compte aussi."),
        dict(text=CTA_TEXT, min=3.4),
    ],
    elements=[
        dict(type="side", at=2, until=6, x=46, y=230, w=300, h=330, col="r", title="SOUS L'ÉMOTION", lines=["Taille doublée", "Entrée sans plan"], big="PERTE ×2", ),
        dict(type="side", at=4, until=6, x=374, y=230, w=300, h=330, col="g", title="AVEC UNE RÈGLE", lines=["Tu arrêtes la journée", "Même taille demain"], big="ÇA RESPIRE"),
        dict(type="cards", at=6, until=10, y=200,
             items=[dict(beat=7, title="Limite de pertes", icon="lock", col="y"),
                    dict(beat=8, title="Ferme la plateforme", icon="stop", col="r"),
                    dict(beat=9, title="Note ce qui s'est passé", icon="book", col="b")]),
        dict(type="big", at=10, until=11, y=330, lines=["DEMAIN,", "NOUVEAU JOUR"], cols=["g", "w"], size=70, lh=100),
        dict(type="cta", at=11, y=190, delay=0.5),
    ])

TENDANCE = dict(
    key="reconnaitre-tendance", topic="trading", title="Comment reconnaître une tendance",
    summary="Creux et sommets de plus en plus hauts : le repère simple d'une tendance haussière.", music=0,
    beats=[
        dict(text="Tu trades {r|contre} le marché sans le savoir ?"),
        dict(text="Voici comment reconnaître une {b|tendance}."),
        dict(text="Le prix ne monte pas en ligne droite.", min=3.0),
        dict(text="Il monte, recule un peu, puis repart {g|plus haut}.", min=3.2),
        dict(text="Des {y|creux} de plus en plus hauts.", min=3.4),
        dict(text="Des {y|sommets} de plus en plus hauts.", min=3.4),
        dict(text="C'est une tendance {g|haussière}."),
        dict(text="À l'inverse, des sommets et des creux de plus en plus {r|bas}, c'est une baisse.", min=3.8),
        dict(text="Alors, trois règles simples."),
        dict(text="Un : repère les {y|creux} et les {y|sommets}."),
        dict(text="Deux : trade dans le {g|sens} de la tendance."),
        dict(text="Trois : vérifie sur une {b|plus grande} échelle de temps."),
        dict(text=CTA_TEXT, min=3.4),
    ],
    elements=[
        dict(type="levels", at=2, until=8, y=230, h=380, path=PATH_TREND, range=(34, 84), dur=3.4, col="b",
             marks=[dict(i=6, beat=4, col="y", text="Creux", delay=0.1), dict(i=13, beat=4, col="y", text="Creux plus haut", delay=1.2),
                    dict(i=20, beat=4, col="y", text="Encore plus haut", delay=2.3),
                    dict(i=3, beat=5, col="g", text="Sommet", below=False, delay=0.1), dict(i=10, beat=5, col="g", text="Sommet plus haut", below=False, delay=1.2),
                    dict(i=17, beat=5, col="g", text="Encore plus haut", below=False, delay=2.3)]),
        dict(type="chip", at=6, until=8, y=190, text="TENDANCE HAUSSIÈRE", col="g"),
        dict(type="cards", at=8, until=12, y=200,
             items=[dict(beat=9, title="Creux et sommets", icon="chart", col="y"),
                    dict(beat=10, title="Dans le sens", icon="target", col="g"),
                    dict(beat=11, title="Grande échelle", icon="clock", col="b")]),
        dict(type="cta", at=12, y=190, delay=0.5),
    ])

SUPPORT = dict(
    key="support-resistance", topic="trading", title="Support et résistance : les zones que le prix respecte",
    summary="Pourquoi le prix rebondit aux mêmes endroits, et comment t'en servir pour placer stop et objectif.", music=1,
    beats=[
        dict(text="Pourquoi le prix rebondit toujours {y|au même endroit} ?"),
        dict(text="Ce n'est pas un hasard. Ce sont des {b|zones}.", min=3.2),
        dict(text="En haut, le prix {r|bute} : c'est une résistance.", min=3.4),
        dict(text="En bas, il {g|rebondit} : c'est un support.", min=3.4),
        dict(text="Plus un niveau est touché, plus il est {y|regardé}.", min=3.2),
        dict(text="Attention : trace des {b|zones}, pas des lignes exactes.", min=3.2),
        dict(text="Trois façons de les utiliser."),
        dict(text="Un : ton stop {r|derrière} la zone."),
        dict(text="Deux : ton objectif {g|avant} la zone opposée."),
        dict(text="Trois : attends une {b|confirmation}."),
        dict(text=CTA_TEXT, min=3.4),
    ],
    elements=[
        dict(type="levels", at=1, until=6, y=230, h=380, path=PATH_RANGE, range=(36, 76), dur=3.4, col="b",
             hlines=[dict(v=67, beat=2, col="r", text="Résistance"), dict(v=44, beat=3, col="g", text="Support")]),
        dict(type="cards", at=6, until=10, y=200,
             items=[dict(beat=7, title="Stop derrière la zone", icon="stop", col="r"),
                    dict(beat=8, title="Objectif avant l'autre", icon="target", col="g"),
                    dict(beat=9, title="Attends confirmation", icon="check", col="b")]),
        dict(type="cta", at=10, y=190, delay=0.5),
    ])

PLAN = dict(
    key="plan-6-lignes", topic="trading", title="Ton plan de trading en 6 lignes",
    summary="Ce que contient un plan de trading écrit, pour ne plus décider à l'instinct.", music=2,
    beats=[
        dict(text="Tu trades à l'{r|instinct} ? Un plan écrit change tout."),
        dict(text="Il tient en {y|six lignes}."),
        dict(text="Trois premières lignes : le {b|cadre}."),
        dict(text="{y|Quoi} : un ou deux instruments, pas vingt.", min=3.0),
        dict(text="{y|Quand} : des horaires fixes.", min=2.6),
        dict(text="{y|Comment} : entrée, stop et objectif, écrits avant.", min=3.2),
        dict(text="Trois dernières lignes : la {r|protection}."),
        dict(text="{y|Combien} : 1 % de risque par trade.", min=2.8),
        dict(text="{y|Limite} : un plafond de pertes par jour.", min=3.0),
        dict(text="{y|Règle} : tu le suis, ou tu n'entres pas.", min=3.0),
        dict(text="Relis-le avant {b|chaque} session.", min=3.0),
        dict(text=CTA_TEXT, min=3.4),
    ],
    elements=[
        dict(type="cards", at=2, until=6, y=200,
             items=[dict(beat=3, title="Quoi : 1 ou 2 instruments", icon="chart", col="y"),
                    dict(beat=4, title="Quand : horaires fixes", icon="clock", col="y"),
                    dict(beat=5, title="Comment : entrée et stop", icon="target", col="y")]),
        dict(type="cards", at=6, until=10, y=200,
             items=[dict(beat=7, title="Combien : 1 %", icon="gauge", col="r"),
                    dict(beat=8, title="Limite par jour", icon="lock", col="r"),
                    dict(beat=9, title="Tu le suis", icon="check", col="r")]),
        dict(type="big", at=10, until=11, y=330, lines=["RELIS-LE", "CHAQUE JOUR"], cols=["b", "w"], size=74, lh=104),
        dict(type="cta", at=11, y=190, delay=0.5),
    ])

FOMO = dict(
    key="peur-de-rater", topic="trading", title="La peur de rater le mouvement",
    summary="Pourquoi on achète en haut, et les trois réflexes pour garder du sang-froid.", music=3,
    beats=[
        dict(text="Le prix s'envole. Tu te dis : je vais {r|rater} l'occasion.", min=3.4),
        dict(text="Alors tu achètes. Tout {r|en haut}."),
        dict(text="Regarde : le prix a déjà beaucoup {y|monté}.", min=3.2),
        dict(text="Tu entres {r|tard}, avec un stop très lointain.", min=3.4),
        dict(text="Le prix revient. Et tu {r|perds}.", min=3.2),
        dict(text="C'est la peur de rater le {y|mouvement}."),
        dict(text="Ce qu'il faut te dire, en trois points."),
        dict(text="Un : il y aura toujours une autre {g|occasion}."),
        dict(text="Deux : sans plan, tu n'{r|entres} pas."),
        dict(text="Trois : attends un {b|retour} vers une zone logique."),
        dict(text="Une occasion manquée ne coûte {g|rien}. Un trade forcé coûte cher.", min=4.0),
        dict(text=CTA_TEXT, min=3.4),
    ],
    elements=[
        dict(type="levels", at=2, until=6, y=230, h=380, path=PATH_FOMO, range=(44, 92), dur=3.4, col="b",
             marks=[dict(i=10, beat=3, col="r", text="Tu entres ici", below=False, delay=0.4)]),
        dict(type="chip", at=5, until=6, y=190, text="LA PEUR DE RATER", col="r"),
        dict(type="cards", at=6, until=10, y=200,
             items=[dict(beat=7, title="Une autre occasion", icon="clock", col="g"),
                    dict(beat=8, title="Sans plan, pas d'entrée", icon="stop", col="r"),
                    dict(beat=9, title="Attends un retour", icon="chart", col="b")]),
        dict(type="big", at=10, until=11, y=330, lines=["MANQUÉ :", "ÇA NE COÛTE RIEN"], cols=["g", "w"], size=52, lh=84),
        dict(type="cta", at=11, y=190, delay=0.5),
    ])

BITCOIN = dict(
    key="bitcoin-1-minute", topic="crypto", title="Bitcoin en une minute",
    summary="Ce qu'est Bitcoin, pourquoi il est limité à 21 millions, et trois réflexes avant d'acheter.", music=3,
    beats=[
        dict(text="Bitcoin : tout le monde en parle, peu l'{y|expliquent}."),
        dict(text="Une monnaie numérique, créée en {b|2009}.", min=3.0),
        dict(text="Sans banque centrale. Un {y|réseau} d'ordinateurs dans le monde entier.", min=3.6),
        dict(text="Il n'en existera jamais plus de {y|21 millions}.", min=3.2),
        dict(text="Cette limite est écrite dans le {b|code}.", min=3.0),
        dict(text="Toutes les transactions sont dans un registre {y|public}.", min=3.4),
        dict(text="On l'appelle la {b|blockchain}."),
        dict(text="Mais attention : son prix est très {r|volatil}.", min=3.2),
        dict(text="Trois réflexes avant d'acheter."),
        dict(text="Un : n'investis que ce que tu peux {r|perdre}."),
        dict(text="Deux : ne partage {r|jamais} ta phrase secrète."),
        dict(text="Trois : méfie-toi des {r|gains garantis}."),
        dict(text=CTA_TEXT, min=3.4),
    ],
    elements=[
        dict(type="stat", at=1, until=3, x=360, y=330, label="CRÉÉ EN", text="2009", col="b", size=90),
        dict(type="chip", at=2, until=3, y=440, text="sans banque centrale", col="y"),
        dict(type="stat", at=3, until=5, x=360, y=330, label="MAXIMUM", text="21 millions", col="y", size=64),
        dict(type="big", at=5, until=7, y=330, lines=["REGISTRE PUBLIC"], cols=["y"], size=48),
        dict(type="chip", at=6, until=7, y=440, text="blockchain", col="b"),
        dict(type="big", at=7, until=8, y=330, lines=["TRÈS VOLATIL"], cols=["r"], size=64),
        dict(type="cards", at=8, until=12, y=200,
             items=[dict(beat=9, title="Ce que tu peux perdre", icon="shield", col="r"),
                    dict(beat=10, title="Phrase secrète privée", icon="lock", col="r"),
                    dict(beat=11, title="Pas de gains garantis", icon="warn", col="r")]),
        dict(type="cta", at=12, y=190, delay=0.5),
    ])

ARNAQUES = dict(
    key="arnaques-5-signes", topic="crypto", title="5 signes d'une arnaque en trading ou en crypto",
    summary="Gains garantis, pression, inconnu qui te contacte : les signaux d'alerte à connaître avant de donner un euro.", music=1,
    beats=[
        dict(text="Comment repérer une {r|arnaque} en trading ou en crypto ?", min=3.2),
        dict(text="Cinq signaux d'{r|alerte}.", min=2.4),
        dict(text="Un : des gains {r|garantis}.", min=2.6),
        dict(text="Deux : une {r|pression} pour agir vite.", min=3.0),
        dict(text="Trois : un dépôt chez un {r|inconnu}.", min=3.0),
        dict(text="Quatre : des captures d'écran {r|sans preuve}.", min=3.2),
        dict(text="Cinq : un inconnu qui te {r|contacte} en privé.", min=3.2),
        dict(text="Avant de donner un euro, vérifie que la société est {g|régulée}.", min=3.6),
        dict(text="Cherche des avis {b|indépendants}."),
        dict(text="Et prends ton {y|temps}. Une vraie occasion ne disparaît pas en dix minutes.", min=4.2),
        dict(text=CTA_TEXT, min=3.4),
    ],
    elements=[
        dict(type="cards", at=1, until=7, y=190,
             items=[dict(beat=2, title="Gains garantis", icon="warn", col="r"),
                    dict(beat=3, title="Pression : agis vite", icon="clock", col="r"),
                    dict(beat=4, title="Dépôt chez un inconnu", icon="coin", col="r"),
                    dict(beat=5, title="Captures sans preuve", icon="chart", col="r"),
                    dict(beat=6, title="Inconnu en privé", icon="warn", col="r")]),
        dict(type="big", at=7, until=10, y=300, lines=["RÉGULÉE ?", "AVIS INDÉPENDANTS ?", "DU TEMPS ?"], cols=["g", "b", "y"], size=44, lh=84),
        dict(type="cta", at=10, y=190, delay=0.5),
    ])

MOTION2 = [STOP, LEVIER, SPREAD, EMOTIONS, TENDANCE, SUPPORT, PLAN, FOMO, BITCOIN, ARNAQUES]

# Jamais d'ecran vide au debut : un graphique de bougies s'anime tant que le premier schema n'est pas la
for _i, _s in enumerate(MOTION2):
    _first = min(e["at"] for e in _s["elements"])
    if _first > 0:
        _s["elements"].insert(0, dict(type="candles", at=0, until=_first, y=210, seed=11 + _i))
