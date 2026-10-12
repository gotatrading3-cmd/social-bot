"""Scenarios des videos explicatives (trading + crypto). Un probleme precis par video, ton pedagogique, aucune promesse de gain.
Chaque scene : visual (hook, chart, steps, recap, formula, compare, bigstat, anatomy) + text (voix off ET sous-titres)."""
from social_explainer import STOP_SCRIPT, series, UP, DOWN, ACC, FG

RED, GREEN = DOWN, UP

ESPERANCE = dict(
    key="esperance", topic="trading", title="Gagner souvent… et perdre quand même ?",
    summary="Un bon taux de réussite ne suffit pas : c'est le rapport entre ton gain moyen et ta perte moyenne qui décide.",
    music=0, seed=11,
    scenes=[
        dict(visual="hook", title="Tu gagnes six trades sur dix et ton compte baisse ?",
             text="Tu gagnes six trades sur dix, et pourtant ton compte baisse ? Ça arrive plus souvent qu'on ne le croit, et il y a une explication simple."),
        dict(visual="compare", label="DEUX TRADERS",
             cards=[dict(title="Trader A", color=RED, lines=["6 gagnants sur 10", "Gain 0,5 · Perte 1"], result="Bilan : -1 sur 10 trades"),
                    dict(title="Trader B", color=GREEN, lines=["4 gagnants sur 10", "Gain 2 · Perte 1"], result="Bilan : +2 sur 10 trades")],
             text="Le premier gagne six fois sur dix, mais chaque gain vaut la moitié d'une perte : sur dix trades, il perd un. Le second ne gagne que quatre fois sur dix, mais chaque gain vaut le double d'une perte : il gagne deux."),
        dict(visual="formula", label="LA FORMULE", formula=["Espérance = taux × gain moyen − (1 − taux) × perte moyenne"],
             example="Si le résultat est positif, ta méthode gagne en moyenne sur la durée. S'il est négatif, elle perd, même avec beaucoup de trades gagnants.",
             text="Pour savoir si une méthode est bonne, calcule son espérance : le taux de réussite multiplié par le gain moyen, moins le taux d'échec multiplié par la perte moyenne."),
        dict(visual="steps", label="CE QUE TU PEUX FAIRE", title="Comment corriger",
             items=["Note tes gains et tes pertes", "Calcule ton gain moyen et ta perte moyenne", "Vise un gain au moins double du risque", "Juge ta méthode sur 50 trades minimum"],
             text="Note chaque résultat, calcule ton gain moyen et ta perte moyenne, vise un gain au moins double de ton risque, et juge ta méthode sur au moins cinquante trades, pas sur trois."),
        dict(visual="recap", title="À retenir", items=["Le taux de réussite seul ne dit rien", "Le ratio gain sur risque compte autant", "Mesure ton espérance"],
             text="Retiens-le : le taux de réussite ne dit pas tout. C'est le ratio entre gain et risque, mesuré sur la durée, qui décide si tu es rentable."),
    ])

SPREAD = dict(
    key="spread", topic="trading", title="Le spread : le coût caché de chaque trade",
    summary="Dès que tu entres, tu paies déjà un coût. Voilà comment le comprendre et le réduire.",
    music=1, seed=12,
    scenes=[
        dict(visual="hook", title="Tu entres en position et tu es déjà en perte ?",
             text="Tu ouvres un trade, et à la seconde même, tu es déjà en légère perte ? Ce n'est pas un bug. C'est le spread."),
        dict(visual="steps", label="LE PRINCIPE", title="Deux prix pour un même actif",
             items=["Un prix d'achat (plus haut)", "Un prix de vente (plus bas)", "L'écart entre les deux = le spread", "C'est la rémunération du courtier"],
             text="Un actif a deux prix : un prix d'achat, un peu plus haut, et un prix de vente, un peu plus bas. L'écart entre les deux s'appelle le spread, et c'est en partie ce qui rémunère ton courtier."),
        dict(visual="bigstat", label="L'IMPACT", value="Plus tu trades, plus tu paies",
             caption="Dix trades par jour avec un spread de deux pips, c'est vingt pips de frais avant même que le marché ne bouge.",
             text="Le spread se paie à chaque trade. Dix trades par jour avec un spread de deux pips, ce sont vingt pips de frais avant même que le marché ne bouge dans ton sens."),
        dict(visual="steps", label="COMMENT LE RÉDUIRE", title="Trois réflexes",
             items=["Trade les paires très liquides", "Évite les annonces et les ouvertures", "Compare les spreads de ton courtier"],
             text="Pour le réduire : privilégie les paires très liquides, évite de trader pendant les grosses annonces ou à l'ouverture des marchés, et compare les spreads proposés par ton courtier."),
        dict(visual="recap", title="À retenir", items=["Le spread est un coût réel", "Moins de trades, plus de qualité", "Prends-le en compte dans ton ratio"],
             text="Retiens que le spread est un vrai coût. Moins de trades, mais de meilleure qualité, et pense à l'inclure dans ton calcul de risque."),
    ])

LEVIER = dict(
    key="levier", topic="trading", title="Le levier : pourquoi il détruit les débutants",
    summary="Le levier amplifie les gains, mais aussi les pertes. Un petit mouvement peut effacer toute ta mise.",
    music=3, seed=13,
    scenes=[
        dict(visual="hook", title="Le levier peut vider ton compte en quelques minutes",
             text="Le levier peut vider un compte en quelques minutes. Beaucoup de débutants l'apprennent trop tard. Voyons pourquoi."),
        dict(visual="steps", label="LE PRINCIPE", title="Ce qu'il fait vraiment",
             items=["Tu contrôles une grosse position avec peu de capital", "Les gains sont multipliés", "Les pertes aussi"],
             text="Le levier te permet de contrôler une grosse position avec peu de capital. Les gains sont multipliés, mais les pertes aussi, exactement dans les mêmes proportions."),
        dict(visual="bigstat", label="UN EXEMPLE", value="1 % = toute ta marge",
             caption="Levier 1 pour 100 : une position de 10 000 pour 100 de marge. Si le prix baisse de 1 %, tu perds 100, soit toute ta marge.",
             text="Exemple : avec un levier de cent, tu ouvres une position de dix mille avec seulement cent de marge. Si le prix baisse d'un pour cent seulement, tu perds cent. Toute ta marge."),
        dict(visual="steps", label="COMMENT L'UTILISER", title="Les bons réflexes",
             items=["Commence avec un levier faible", "Pose toujours un stop", "Risque 1 % de ton capital par trade", "Calcule ta taille de position"],
             text="Commence avec un levier faible, pose toujours un stop, ne risque qu'environ un pour cent de ton capital par trade, et calcule ta taille de position avant d'entrer."),
        dict(visual="recap", title="À retenir", items=["Le levier amplifie tout", "Le risque se règle avec le stop et la taille", "Petit levier = survie"],
             text="Le levier n'est pas un cadeau, c'est un amplificateur. C'est ton stop et la taille de ta position qui protègent ton compte."),
    ])

BOUGIE = dict(
    key="bougie", topic="trading", title="Lire une bougie japonaise en 1 minute",
    summary="Quatre prix, deux couleurs : tout ce qu'il faut savoir pour lire une bougie.",
    music=2, seed=14,
    scenes=[
        dict(visual="hook", title="Tu regardes des bougies sans savoir les lire ?",
             text="Tu regardes des bougies sur ton écran, mais tu ne sais pas vraiment ce qu'elles racontent ? Voici l'essentiel en une minute."),
        dict(visual="anatomy", bull=True, names=["Plus haut", "Clôture", "Ouverture", "Plus bas"], label="BOUGIE HAUSSIÈRE",
             text="Une bougie résume quatre prix sur une période : l'ouverture, la clôture, le plus haut et le plus bas. Quand la clôture est au-dessus de l'ouverture, la bougie est haussière, souvent en vert."),
        dict(visual="anatomy", bull=False, names=["Plus haut", "Clôture", "Ouverture", "Plus bas"], label="BOUGIE BAISSIÈRE",
             text="Quand la clôture est en dessous de l'ouverture, la bougie est baissière, souvent en rouge. Le rectangle s'appelle le corps, et les traits fins sont les mèches."),
        dict(visual="steps", label="COMMENT LIRE", title="Ce que ça te dit",
             items=["Grand corps : acheteurs ou vendeurs décidés", "Longue mèche : le prix a été rejeté", "Petit corps : hésitation du marché"],
             text="Un grand corps montre des acheteurs ou des vendeurs décidés. Une longue mèche montre que le prix a été rejeté à ce niveau. Un petit corps montre une hésitation."),
        dict(visual="recap", title="À retenir", items=["4 prix par bougie", "Corps = ouverture à clôture", "Mèches = extrêmes rejetés"],
             text="Retiens quatre prix par bougie, un corps entre l'ouverture et la clôture, et des mèches qui montrent les extrêmes. Une bougie seule ne suffit pas : lis-la toujours dans son contexte."),
    ])

_TREND = series([40, 44, 48, 52, 49, 45, 43, 47, 52, 57, 61, 58, 54, 52, 56, 62, 67, 71, 68, 64, 62, 66, 72, 77], seed=3,
                lows={6: 40.5, 13: 49.5, 20: 59.5}, highs={3: 54.5, 10: 63, 17: 73.5})
TENDANCE = dict(
    key="tendance", topic="trading", title="Comment reconnaître une tendance",
    summary="Sommets et creux de plus en plus hauts : voilà le secret d'une tendance haussière.",
    music=0, seed=15,
    scenes=[
        dict(visual="hook", title="Tu trades contre le marché sans le savoir ?",
             text="Beaucoup de traders perdent parce qu'ils vont contre la tendance sans s'en rendre compte. Voici comment la reconnaître."),
        dict(visual="chart", grow=True, candles=_TREND, range=(30, 90), label="LA TENDANCE", text="Regarde ce graphique. Le prix ne monte pas en ligne droite : il monte, recule un peu, puis repart plus haut."),
        dict(visual="chart", candles=_TREND, range=(30, 90), label="HAUSSIÈRE",
             marks=[dict(idx=6, at="low", label="Creux", color=ACC, t0=0.1), dict(idx=13, at="low", label="Creux plus haut", color=ACC, t0=0.35),
                    dict(idx=20, at="low", label="Encore plus haut", color=ACC, t0=0.6)],
             text="Une tendance haussière, c'est une suite de creux de plus en plus hauts, et de sommets de plus en plus hauts. Chaque recul est acheté plus haut que le précédent."),
        dict(visual="steps", label="À L'INVERSE", title="Une tendance baissière",
             items=["Des sommets de plus en plus bas", "Des creux de plus en plus bas", "Chaque rebond est vendu plus bas"],
             text="Dans une tendance baissière, c'est l'inverse : des sommets et des creux de plus en plus bas. Chaque rebond est vendu plus bas que le précédent."),
        dict(visual="recap", title="À retenir", items=["Sommets et creux plus hauts = hausse", "Sommets et creux plus bas = baisse", "Trade dans le sens de la tendance"],
             text="Retiens-le : des sommets et des creux plus hauts signalent la hausse, plus bas signalent la baisse. Et la plupart du temps, il vaut mieux trader dans le sens de la tendance."),
    ])

_RANGE = series([50, 56, 62, 66, 63, 58, 52, 47, 44, 48, 54, 60, 65, 67, 62, 56, 50, 46, 45, 49, 55, 61, 65, 68], seed=8,
                lows={8: 42, 18: 42.5}, highs={3: 69, 13: 69.5, 23: 70})
SUPPORT = dict(
    key="support", topic="trading", title="Support et résistance : les zones que le prix respecte",
    summary="Le prix rebondit souvent aux mêmes endroits. Apprends à repérer ces zones.",
    music=1, seed=16,
    scenes=[
        dict(visual="hook", title="Pourquoi le prix rebondit toujours au même endroit ?",
             text="Tu as remarqué que le prix rebondit souvent aux mêmes endroits ? Ce n'est pas un hasard. On appelle ça des supports et des résistances."),
        dict(visual="chart", grow=True, candles=_RANGE, range=(30, 85), label="LE CONSTAT",
             levels=[dict(price=70, label="Résistance", color=RED, t0=0.6), dict(price=42.5, label="Support", color=GREEN, t0=0.8)],
             text="Ici, le prix butte plusieurs fois vers le haut, sur une résistance, et rebondit plusieurs fois vers le bas, sur un support. Plus un niveau est touché, plus il est regardé par les autres traders."),
        dict(visual="steps", label="EN PRATIQUE", title="Comment les tracer",
             items=["Repère les rebonds répétés", "Trace une zone, pas une ligne exacte", "Ignore les niveaux touchés une seule fois"],
             text="Pour les repérer, cherche les endroits où le prix a rebondi plusieurs fois. Trace une zone plutôt qu'une ligne exacte, car le prix dépasse souvent un peu, et ignore les niveaux touchés une seule fois."),
        dict(visual="steps", label="COMMENT EN PROFITER", title="Trois usages",
             items=["Placer ton stop derrière la zone", "Fixer ton objectif avant la zone opposée", "Attendre une confirmation avant d'entrer"],
             text="Utilise-les pour placer ton stop juste derrière la zone, fixer ton objectif avant la zone opposée, et attendre une bougie de confirmation avant d'entrer."),
        dict(visual="recap", title="À retenir", items=["Support : le prix rebondit vers le haut", "Résistance : le prix bute vers le bas", "Des zones, pas des lignes"],
             text="Retiens : un support fait rebondir le prix vers le haut, une résistance le fait buter vers le bas. Pense en zones, pas en lignes exactes."),
    ])

BITCOIN = dict(
    key="bitcoin", topic="crypto", title="Bitcoin : c'est quoi, concrètement ?",
    summary="Un réseau sans banque centrale, un nombre limité d'unités et un registre public. L'essentiel à comprendre.",
    music=3, seed=17,
    scenes=[
        dict(visual="hook", title="Bitcoin : tout le monde en parle, peu l'expliquent",
             text="Tout le monde parle de Bitcoin, mais peu de gens savent l'expliquer simplement. Voici l'essentiel."),
        dict(visual="steps", label="LES BASES", title="Ce que c'est",
             items=["Une monnaie numérique créée en 2009", "Sans banque centrale", "Un réseau d'ordinateurs partout dans le monde"],
             text="Bitcoin est une monnaie numérique créée en deux mille neuf par un auteur anonyme, Satoshi Nakamoto. Aucune banque centrale ne la contrôle : c'est un réseau d'ordinateurs dans le monde entier."),
        dict(visual="bigstat", label="LA RARETÉ", value="21 millions",
             caption="C'est le nombre maximum de bitcoins qui existeront un jour. Cette limite est écrite dans le code.",
             text="Il n'existera jamais plus de vingt et un millions de bitcoins. Cette limite est écrite dans le code, et c'est l'une des raisons pour lesquelles on le compare souvent à un or numérique."),
        dict(visual="steps", label="LA BLOCKCHAIN", title="Un registre public",
             items=["Chaque transaction est enregistrée", "Le registre est visible par tous", "Impossible de le modifier après coup"],
             text="Toutes les transactions sont enregistrées dans un registre public, la blockchain. Il est visible par tous, et il est pratiquement impossible de le modifier après coup."),
        dict(visual="recap", title="À retenir", items=["Créé en 2009", "Limité à 21 millions", "Registre public, sans banque centrale", "Très volatil : le prix varie beaucoup"],
             text="Retiens : créé en deux mille neuf, limité à vingt et un millions, un registre public sans banque centrale. Et son prix est très volatil : n'investis jamais ce que tu ne peux pas te permettre de perdre."),
    ])

WALLET = dict(
    key="securite-crypto", topic="crypto", title="Comment sécuriser tes cryptos",
    summary="Phrase de récupération, double authentification, adresses vérifiées : les bases pour ne rien perdre.",
    music=2, seed=18,
    scenes=[
        dict(visual="hook", title="Des cryptos volées en quelques secondes ?",
             text="Chaque semaine, des gens perdent leurs cryptos en quelques secondes, souvent par une simple erreur. Voici comment l'éviter."),
        dict(visual="steps", label="LA PHRASE SECRÈTE", title="Ta phrase de récupération",
             items=["Elle donne accès à tout ton portefeuille", "Ne la partage jamais, à personne", "Note-la sur papier, hors ligne", "Aucun support sérieux ne te la demandera"],
             text="Quand tu crées un portefeuille, on te donne une phrase de récupération. Elle donne accès à tout. Ne la partage jamais, note-la sur papier, hors ligne, et sache qu'aucun support sérieux ne te la demandera."),
        dict(visual="steps", label="AU QUOTIDIEN", title="Les bons réflexes",
             items=["Active la double authentification", "Vérifie l'adresse avant chaque envoi", "Méfie-toi des liens et des messages privés", "Teste avec un petit montant d'abord"],
             text="Active la double authentification sur tes comptes, vérifie l'adresse avant chaque envoi, méfie-toi des liens et des messages privés, et teste toujours avec un petit montant avant un gros transfert."),
        dict(visual="bigstat", label="LA RÈGLE D'OR", value="Pas tes clés, pas tes cryptos",
             caption="Sur une plateforme, c'est elle qui détient les clés. Dans ton portefeuille personnel, c'est toi.",
             text="Un dicton résume tout : pas tes clés, pas tes cryptos. Sur une plateforme, ce sont ses clés. Dans un portefeuille personnel, ce sont les tiennes, avec la responsabilité qui va avec."),
        dict(visual="recap", title="À retenir", items=["Phrase secrète : jamais partagée", "Double authentification partout", "Adresse vérifiée à chaque envoi"],
             text="Retiens trois choses : ta phrase secrète n'est jamais partagée, la double authentification est activée partout, et chaque adresse est vérifiée avant l'envoi."),
    ])

ARNAQUES = dict(
    key="arnaques", topic="crypto", title="5 signes d'une arnaque en trading ou en crypto",
    summary="Gains garantis, pression, inconnu qui te contacte : les signaux d'alerte à connaître.",
    music=1, seed=19,
    scenes=[
        dict(visual="hook", title="Comment savoir si une offre de trading est une arnaque ?",
             text="Comment savoir si une offre de trading ou de crypto est une arnaque ? Voici cinq signaux d'alerte à connaître absolument."),
        dict(visual="steps", label="LES ALERTES", title="Fuis si tu vois ça",
             items=["Des gains garantis", "Une pression pour agir vite", "Un dépôt sur le compte d'un inconnu", "Des captures d'écran sans preuve", "Un inconnu qui te contacte en privé"],
             text="Un : des gains garantis. Deux : une pression pour agir vite. Trois : un dépôt sur le compte d'un inconnu. Quatre : des captures d'écran sans preuve. Cinq : un inconnu qui te contacte en privé."),
        dict(visual="steps", label="LES RÉFLEXES", title="Avant de donner un euro",
             items=["Vérifie que la société est régulée", "Cherche des avis indépendants", "Prends ton temps, rien n'est urgent"],
             text="Avant de donner un seul euro, vérifie que la société est régulée, cherche des avis indépendants, et prends ton temps : une vraie opportunité ne disparaît pas en dix minutes."),
        dict(visual="recap", title="À retenir", items=["Aucun gain n'est garanti", "L'urgence est un piège", "Ne confie jamais ton argent à un inconnu"],
             text="Retiens que personne ne peut te garantir des gains, que l'urgence est un piège, et que tu ne dois jamais confier ton argent à un inconnu, même sympathique."),
    ])

EMOTIONS = dict(
    key="emotions", topic="trading", title="Après trois pertes de suite, que faire ?",
    summary="La série de pertes est le moment le plus dangereux. Voici le réflexe qui protège ton compte.",
    music=0, seed=20,
    scenes=[
        dict(visual="hook", title="Trois pertes de suite et tu veux te refaire ?",
             text="Tu viens de perdre trois trades d'affilée, et tu sens l'envie de te refaire tout de suite ? C'est le moment le plus dangereux pour ton compte."),
        dict(visual="compare", label="DEUX RÉACTIONS",
             cards=[dict(title="Sous le coup de l'émotion", color=RED, lines=["Tu augmentes ta taille", "Tu entres sans plan"], result="Résultat : la perte grossit"),
                    dict(title="Avec une règle", color=GREEN, lines=["Tu t'arrêtes pour la journée", "Tu reviens demain, même taille"], result="Résultat : le compte respire")],
             text="Sous le coup de l'émotion, on augmente sa taille et on entre sans plan : la perte grossit. Avec une règle claire, on s'arrête pour la journée et on revient demain avec la même taille."),
        dict(visual="steps", label="TA RÈGLE", title="Ton plan anti-revanche",
             items=["Fixe une limite de pertes par jour", "Ferme la plateforme une fois atteinte", "Note ce qui s'est passé", "Reviens le lendemain avec la même taille"],
             text="Fixe une limite de pertes par jour, par exemple trois trades ou deux pour cent. Une fois atteinte, ferme la plateforme, note ce qui s'est passé, et reviens le lendemain avec la même taille."),
        dict(visual="recap", title="À retenir", items=["Une limite par jour", "Jamais de revanche", "Le marché sera là demain"],
             text="Retiens : une limite de pertes par jour, jamais de revanche, et rappelle-toi que le marché sera encore là demain."),
    ])

PETIT_CAPITAL = dict(
    key="petit-capital", topic="trading", title="Trader avec un petit capital : ce qu'il faut savoir",
    summary="Avec un petit compte, l'objectif n'est pas de gagner vite mais d'apprendre à ne pas perdre.",
    music=2, seed=21,
    scenes=[
        dict(visual="hook", title="Tu veux commencer le trading avec peu d'argent ?",
             text="Tu veux commencer le trading avec un petit capital ? C'est possible, mais il faut bien comprendre ce que ça implique."),
        dict(visual="bigstat", label="LE RISQUE", value="1 % de 100 € = 1 €",
             caption="C'est ton risque maximum par trade. Petit compte, petits montants : c'est normal.",
             text="Avec cent euros, risquer un pour cent, c'est risquer un euro par trade. C'est peu, et c'est normal. Les petits comptes ne donnent pas de gros gains, mais ils permettent d'apprendre sans se mettre en danger."),
        dict(visual="steps", label="L'OBJECTIF", title="Au début, vise l'apprentissage",
             items=["Apprends à ne pas perdre avant de gagner", "Mesure tes résultats sur 50 trades", "Teste ta méthode en démo d'abord", "Augmente ton capital plus tard, pas ta prise de risque"],
             text="Au début, apprends à ne pas perdre avant de chercher à gagner. Mesure tes résultats sur cinquante trades, teste ta méthode en démonstration d'abord, et fais grandir ton capital plus tard, sans augmenter ta prise de risque."),
        dict(visual="recap", title="À retenir", items=["Risque 1 % par trade", "Apprendre avant de gagner", "Pas de levier excessif"],
             text="Retiens : un pour cent de risque par trade, apprendre avant de gagner, et pas de levier excessif. Un petit compte bien géré vaut mieux qu'un gros compte détruit."),
    ])

OFFRE_DEMANDE = dict(
    key="prix-crypto", topic="crypto", title="Pourquoi le prix du Bitcoin bouge autant ?",
    summary="Offre et demande, actualité, liquidité : les raisons des grands mouvements.",
    music=3, seed=22,
    scenes=[
        dict(visual="hook", title="Pourquoi le Bitcoin peut bouger de 10 % en un jour ?",
             text="Pourquoi le Bitcoin peut-il bouger de dix pour cent en une seule journée ? Il y a trois raisons principales."),
        dict(visual="steps", label="LES MOTEURS", title="Trois raisons",
             items=["L'offre et la demande", "L'actualité et les annonces", "Une liquidité plus faible que les grands marchés"],
             text="Un : l'offre et la demande. Plus d'acheteurs que de vendeurs, et le prix monte. Deux : l'actualité, comme une décision d'un régulateur. Trois : une liquidité plus faible que sur les grands marchés, donc des mouvements plus brusques."),
        dict(visual="compare", label="CE QUE ÇA CHANGE",
             cards=[dict(title="Opportunité", color=GREEN, lines=["De grands mouvements", "Des tendances nettes"], result="Plus de potentiel"),
                    dict(title="Danger", color=RED, lines=["Des chutes rapides", "Des pertes amplifiées avec le levier"], result="Plus de risque")],
             text="Cette volatilité crée des opportunités, avec de grands mouvements et des tendances nettes, mais elle crée aussi des dangers : des chutes rapides, et des pertes amplifiées si tu utilises le levier."),
        dict(visual="recap", title="À retenir", items=["Offre et demande", "L'actualité déplace le prix", "Volatilité = risque aussi"],
             text="Retiens : l'offre et la demande, l'actualité qui déplace le prix, et une volatilité qui est à la fois une chance et un risque. Prends toujours un stop, surtout en crypto."),
    ])

JOURNAL = dict(
    key="journal", topic="trading", title="Le journal de trading : quoi noter pour progresser",
    summary="Six lignes à noter après chaque trade pour apprendre vite de tes erreurs.",
    music=1, seed=23,
    scenes=[
        dict(visual="hook", title="Tu refais les mêmes erreurs sans comprendre pourquoi ?",
             text="Tu refais les mêmes erreurs sans comprendre pourquoi ? Il existe un outil simple, gratuit, que presque tous les traders sérieux utilisent : le journal."),
        dict(visual="steps", label="À NOTER", title="Après chaque trade",
             items=["La date et l'actif", "Pourquoi tu es entré", "Ton stop et ton objectif", "Le résultat, en multiple du risque", "Ce que tu ressentais", "Ce que tu referais autrement"],
             text="Après chaque trade, note la date et l'actif, la raison de ton entrée, ton stop et ton objectif, le résultat en multiple de ton risque, ce que tu ressentais, et ce que tu ferais autrement."),
        dict(visual="steps", label="LA REVUE", title="Chaque dimanche",
             items=["Relis tes trades de la semaine", "Repère l'erreur qui revient", "Choisis une seule règle à corriger"],
             text="Chaque dimanche, relis tes trades de la semaine, repère l'erreur qui revient le plus souvent, et choisis une seule règle à corriger la semaine suivante."),
        dict(visual="recap", title="À retenir", items=["Note chaque trade", "Mesure en multiple du risque", "Corrige une chose à la fois"],
             text="Retiens : note chaque trade, mesure en multiple de ton risque, et corrige une seule chose à la fois. Ce qui ne se mesure pas ne s'améliore pas."),
    ])

SCRIPTS = [STOP_SCRIPT, BITCOIN, ESPERANCE, BOUGIE, WALLET, LEVIER, TENDANCE, ARNAQUES, SPREAD, SUPPORT, EMOTIONS, OFFRE_DEMANDE, PETIT_CAPITAL, JOURNAL]
for _s in SCRIPTS:
    _s.setdefault("topic", "trading")
    _s.setdefault("summary", _s["title"])
