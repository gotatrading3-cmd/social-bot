"""Deuxieme serie de videos explicatives (nouveaux sujets). Meme format que social_scripts.py."""
from social_explainer import UP, DOWN, ACC, FG

RED, GREEN = DOWN, UP

ORDRES = dict(
    key="ordres", topic="trading", title="Ordre au marché ou ordre limite ?",
    summary="Deux façons d'entrer en position, deux effets très différents sur ton prix d'entrée.",
    music=1, seed=31,
    scenes=[
        dict(visual="hook", title="Pourquoi ton prix d'entrée est parfois pire que prévu ?",
             text="Tu cliques sur acheter, et ton prix d'entrée est un peu plus mauvais que celui que tu voyais ? Ce n'est pas un bug, c'est le type d'ordre."),
        dict(visual="compare", label="DEUX ORDRES",
             cards=[dict(title="Ordre au marché", color=ACC, lines=["Exécuté tout de suite", "Au meilleur prix disponible"], result="Rapide, mais prix non garanti"),
                    dict(title="Ordre limite", color=GREEN, lines=["Tu fixes ton prix", "Exécuté seulement s'il l'atteint"], result="Prix garanti, mais pas d'exécution sûre")],
             text="Avec un ordre au marché, tu entres tout de suite, au meilleur prix disponible, mais ce prix n'est pas garanti. Avec un ordre limite, tu fixes ton prix : il est respecté, mais l'ordre n'est exécuté que si le marché l'atteint."),
        dict(visual="steps", label="QUAND UTILISER QUOI", title="Le bon choix",
             items=["Marché : quand la rapidité compte", "Limite : quand tu vises un niveau précis", "Évite le marché pendant les annonces"],
             text="Utilise l'ordre au marché quand la rapidité compte. Utilise l'ordre limite quand tu vises un niveau précis. Et évite l'ordre au marché pendant les annonces, car le prix saute et ton entrée peut être très décalée."),
        dict(visual="recap", title="À retenir", items=["Marché = vitesse", "Limite = contrôle du prix", "Pas d'ordre au marché en pleine annonce"],
             text="Retiens : le marché te donne la vitesse, la limite te donne le contrôle du prix. Choisis selon ce qui compte le plus pour ce trade."),
    ])

SESSIONS = dict(
    key="sessions", topic="trading", title="Les sessions de trading : quand le marché bouge vraiment",
    summary="Tokyo, Londres, New York : à quelles heures le marché est le plus actif.",
    music=2, seed=32,
    scenes=[
        dict(visual="hook", title="Pourquoi le marché dort parfois, puis explose ?",
             text="Tu as remarqué que le marché semble parfois endormi, puis part d'un coup ? Ce n'est pas un hasard : il dépend des horaires."),
        dict(visual="steps", label="LES TROIS SESSIONS", title="Le marché des devises ne dort jamais",
             items=["Tokyo : environ de minuit à 9 h, heure de Londres", "Londres : environ de 8 h à 17 h", "New York : environ de 13 h à 22 h"],
             text="Le marché des devises tourne presque vingt-quatre heures sur vingt-quatre, grâce à trois sessions. Tokyo, de minuit à neuf heures. Londres, de huit à dix-sept heures. New York, de treize à vingt-deux heures. Heures de Londres, approximatives."),
        dict(visual="bigstat", label="LE MOMENT FORT", value="Londres + New York",
             caption="Quand les deux sessions se chevauchent, de 13 h à 17 h environ, la liquidité et les mouvements sont les plus importants.",
             text="Le moment le plus actif, c'est quand Londres et New York sont ouvertes en même temps, de treize à dix-sept heures environ. C'est là que la liquidité est la plus forte et que les mouvements sont les plus nets."),
        dict(visual="recap", title="À retenir", items=["Chaque session a son rythme", "Le chevauchement Londres et New York est le plus actif", "Trade quand ton instrument est actif"],
             text="Retiens que chaque session a son rythme, et que le chevauchement entre Londres et New York est le plus actif. Trade quand ton instrument bouge. Horaires approximatifs, variables avec l'heure d'été."),
    ])

ANNONCES = dict(
    key="annonces", topic="trading", title="Les annonces économiques : comment ne pas se faire piéger",
    summary="Inflation, taux, emploi : pourquoi les annonces font bouger les prix et comment s'y préparer.",
    music=3, seed=33,
    scenes=[
        dict(visual="hook", title="Ton stop saute en une seconde pendant une annonce ?",
             text="Ton stop saute en une seconde, sans que le prix ne revienne ? Il y avait probablement une annonce économique."),
        dict(visual="steps", label="LES ANNONCES CLÉS", title="Celles qui font bouger le marché",
             items=["Les décisions de taux des banques centrales", "L'inflation", "Les chiffres de l'emploi américain"],
             text="Les annonces qui font le plus bouger les prix sont les décisions de taux des banques centrales, l'inflation, et les chiffres de l'emploi américain. À ces moments, le prix peut sauter de dizaines de pips en quelques secondes."),
        dict(visual="steps", label="LES RISQUES", title="Pendant l'annonce",
             items=["Le spread s'élargit", "Le prix peut sauter ton stop", "Les mouvements partent dans les deux sens"],
             text="Pendant l'annonce, le spread s'élargit, le prix peut sauter par-dessus ton stop, et les mouvements partent souvent dans un sens puis dans l'autre. Même un bon plan peut y subir une perte plus grande que prévue."),
        dict(visual="steps", label="TON PLAN", title="Comment t'en protéger",
             items=["Consulte le calendrier économique chaque matin", "Évite d'entrer juste avant une annonce majeure", "Attends que le marché se calme"],
             text="Consulte le calendrier économique chaque matin, évite d'ouvrir une position juste avant une annonce majeure, et attends que le marché se calme avant de reprendre."),
        dict(visual="recap", title="À retenir", items=["Calendrier économique chaque matin", "Pas d'entrée juste avant une annonce", "Patience après l'annonce"],
             text="Retiens : regarde le calendrier chaque matin, ne prends pas de position juste avant une annonce majeure, et laisse le marché se calmer."),
    ])

PAIRES = dict(
    key="paires", topic="trading", title="Une paire de devises, comment ça marche ?",
    summary="EUR/USD, GBP/USD… ce que signifie vraiment le prix d'une paire.",
    music=0, seed=34,
    scenes=[
        dict(visual="hook", title="EUR/USD à 1,10 : ça veut dire quoi, exactement ?",
             text="Tu vois écrit euro dollar à un virgule dix, mais tu ne sais pas vraiment ce que ça veut dire ? Voici la lecture simple."),
        dict(visual="bigstat", label="LA LECTURE", value="1 € = 1,10 $",
             caption="La première devise (EUR) est la devise de base. Le prix indique combien de la deuxième (USD) il faut pour l'acheter.",
             text="Le prix d'une paire indique combien il faut de la deuxième devise pour acheter une unité de la première. Si l'euro dollar est à un virgule dix, un euro vaut un dollar dix."),
        dict(visual="compare", label="ACHETER OU VENDRE",
             cards=[dict(title="Tu achètes la paire", color=GREEN, lines=["Tu achètes l'euro", "Tu vends le dollar"], result="Tu gagnes si l'euro monte"),
                    dict(title="Tu vends la paire", color=RED, lines=["Tu vends l'euro", "Tu achètes le dollar"], result="Tu gagnes si l'euro baisse")],
             text="Acheter la paire, c'est acheter l'euro et vendre le dollar : tu gagnes si l'euro monte face au dollar. La vendre, c'est l'inverse : tu gagnes si l'euro baisse."),
        dict(visual="recap", title="À retenir", items=["Première devise = devise de base", "Le prix = valeur de la base dans la seconde", "Acheter = parier sur la hausse de la base"],
             text="Retiens : la première devise est la devise de base, le prix dit combien vaut la base dans la seconde, et acheter la paire revient à parier sur la hausse de la devise de base."),
    ])

PIP_LOT = dict(
    key="pip-lot", topic="trading", title="Pip et lot : comment calculer ce que tu risques",
    summary="Ce qu'est un pip, ce qu'est un lot, et comment connaître la valeur de ton risque.",
    music=1, seed=35,
    scenes=[
        dict(visual="hook", title="Combien vaut vraiment un pip dans ton trade ?",
             text="On te parle de pips et de lots, mais tu ne sais pas combien ça représente en argent ? C'est pourtant la base du calcul du risque."),
        dict(visual="steps", label="LES DÉFINITIONS", title="Deux mots essentiels",
             items=["Un pip : le plus petit mouvement standard, 0,0001 sur la plupart des paires", "Un lot : la taille de ta position", "Un lot standard = 100 000 unités"],
             text="Un pip est le plus petit mouvement standard d'une paire, soit zéro virgule zéro zéro zéro un sur la plupart d'entre elles. Un lot est la taille de ta position, et un lot standard représente cent mille unités."),
        dict(visual="bigstat", label="LA VALEUR", value="1 lot = 10 $ par pip",
             caption="Sur une paire où le dollar est la devise de cotation, un lot standard vaut environ 10 dollars par pip. Un mini-lot, 1 dollar. Un micro-lot, 10 centimes.",
             text="Sur une paire cotée en dollars, un lot standard vaut environ dix dollars par pip. Un mini-lot, un dollar. Un micro-lot, dix centimes. Plus ton lot est petit, plus ton risque par pip est faible."),
        dict(visual="formula", label="TON CALCUL", formula=["Risque = pips de stop × valeur du pip × lots"],
             example="Exemple : un stop de 20 pips avec un micro-lot à 0,10 $ par pip, c'est 2 $ de risque. Tu peux ainsi choisir ton lot pour respecter ton 1 %.",
             text="Pour connaître ton risque, multiplie les pips de ton stop par la valeur du pip et par le nombre de lots. Par exemple, vingt pips avec un micro-lot, c'est deux dollars de risque. Tu choisis ton lot pour respecter ton pourcentage."),
        dict(visual="recap", title="À retenir", items=["Pip = unité de mouvement", "Lot = taille de position", "Risque = pips × valeur du pip × lots"],
             text="Retiens : le pip mesure le mouvement, le lot mesure ta position, et ton risque, c'est les pips de ton stop multipliés par la valeur du pip et par le nombre de lots."),
    ])

STABLECOINS = dict(
    key="stablecoins", topic="crypto", title="Les stablecoins : c'est quoi et quel risque ?",
    summary="Des cryptos conçues pour valoir un dollar. Comment ça marche, et pourquoi ce n'est pas sans risque.",
    music=3, seed=36,
    scenes=[
        dict(visual="hook", title="Une crypto qui vaut toujours un dollar, ça existe ?",
             text="Il existe des cryptos qui ne bougent presque pas : on les appelle les stablecoins. Comment font-elles, et sont-elles sans risque ?"),
        dict(visual="steps", label="LE PRINCIPE", title="Une monnaie numérique stable",
             items=["Elles visent la valeur d'une monnaie, souvent le dollar", "Un émetteur garde des réserves en échange", "Tu peux passer de crypto à stable en un clic"],
             text="Un stablecoin vise à garder la valeur d'une monnaie, souvent le dollar. Un émetteur détient des réserves censées couvrir chaque unité en circulation. Cela permet de se mettre à l'abri de la volatilité sans quitter l'univers crypto."),
        dict(visual="steps", label="LES RISQUES", title="Pas sans danger",
             items=["L'émetteur peut ne pas avoir toutes les réserves", "Le prix peut décrocher du dollar", "Des règles qui changent selon les pays"],
             text="Mais ils ne sont pas sans risque. L'émetteur peut ne pas détenir toutes ses réserves, le prix peut décrocher de un dollar, et les règles changent selon les pays. Ce n'est pas un compte bancaire garanti."),
        dict(visual="recap", title="À retenir", items=["Un stablecoin vise la valeur d'une monnaie", "Il dépend de son émetteur", "Vérifie l'émetteur avant de l'utiliser"],
             text="Retiens : un stablecoin vise la valeur d'une monnaie, mais dépend entièrement de son émetteur. Renseigne-toi sur lui avant de lui confier de l'argent."),
    ])

HALVING = dict(
    key="halving", topic="crypto", title="Le Bitcoin divise sa création par deux tous les 4 ans",
    summary="Le mécanisme qui réduit la création de nouveaux bitcoins, environ tous les quatre ans.",
    music=0, seed=37,
    scenes=[
        dict(visual="hook", title="Pourquoi on parle du Bitcoin tous les quatre ans ?",
             text="Environ tous les quatre ans, le monde de la crypto parle d'un événement précis du Bitcoin. Voici ce qu'il se passe."),
        dict(visual="steps", label="LE MÉCANISME", title="Une règle écrite dans le code",
             items=["De nouveaux bitcoins récompensent les mineurs", "Cette récompense est divisée par deux tous les 210 000 blocs", "Soit environ tous les 4 ans"],
             text="De nouveaux bitcoins sont créés pour récompenser les mineurs, ceux qui font fonctionner le réseau. Cette récompense est divisée par deux tous les deux cent dix mille blocs, soit environ tous les quatre ans."),
        dict(visual="bigstat", label="DERNIÈRE RÉDUCTION", value="3,125 BTC",
             caption="C'est la récompense par bloc depuis avril 2024. Elle était de 6,25 avant, et de 50 au tout début.",
             text="Depuis avril deux mille vingt-quatre, la récompense est de trois virgule cent vingt-cinq bitcoins par bloc. Elle était de six virgule vingt-cinq avant, et de cinquante au tout début."),
        dict(visual="steps", label="À SAVOIR", title="Ce que ça ne garantit pas",
             items=["La création ralentit, donc la rareté augmente", "Le prix n'est pas garanti de monter", "D'autres facteurs pèsent bien plus"],
             text="Moins de nouveaux bitcoins, cela signifie une rareté qui augmente. Mais cela ne garantit pas que le prix monte : la demande, l'actualité et l'économie pèsent aussi beaucoup. Personne ne peut prédire le prix."),
        dict(visual="recap", title="À retenir", items=["Récompense divisée par deux environ tous les 4 ans", "Rareté croissante", "Aucune garantie sur le prix"],
             text="Retiens : la récompense des mineurs est divisée par deux environ tous les quatre ans, la rareté augmente, mais le prix n'est jamais garanti."),
    ])

ETHEREUM = dict(
    key="ethereum", topic="crypto", title="Ethereum : à quoi ça sert, en dehors du prix ?",
    summary="Contrats intelligents, applications décentralisées : ce que fait réellement Ethereum.",
    music=2, seed=38,
    scenes=[
        dict(visual="hook", title="Ethereum, c'est juste « un autre Bitcoin » ?",
             text="On te dit qu'Ethereum, c'est juste un autre Bitcoin. Pas exactement : les deux n'ont pas le même objectif."),
        dict(visual="compare", label="DEUX OBJECTIFS",
             cards=[dict(title="Bitcoin", color=ACC, lines=["Une monnaie numérique", "Rare et simple"], result="Réserve de valeur et paiements"),
                    dict(title="Ethereum", color=GREEN, lines=["Une plateforme programmable", "Applications et contrats intelligents"], result="Une infrastructure pour développeurs")],
             text="Bitcoin est avant tout une monnaie numérique. Ethereum est une plateforme programmable : on y crée des applications et des contrats intelligents, des programmes qui s'exécutent seuls selon des règles fixées d'avance."),
        dict(visual="steps", label="EN PRATIQUE", title="Ce qu'on y trouve",
             items=["Des applications sans intermédiaire", "Des échanges de cryptos directement entre utilisateurs", "Des frais de réseau à payer à chaque opération"],
             text="Sur Ethereum, on trouve des applications sans intermédiaire, des échanges directs entre utilisateurs, et des frais de réseau à chaque opération, qui varient selon l'affluence."),
        dict(visual="recap", title="À retenir", items=["Bitcoin : une monnaie rare", "Ethereum : une plateforme programmable", "Chaque projet a ses risques"],
             text="Retiens : Bitcoin est une monnaie rare, Ethereum est une plateforme programmable. Ce sont deux projets différents, avec chacun leurs risques."),
    ])

PEUR_RATER = dict(
    key="peur-de-rater", topic="trading", title="La peur de rater le mouvement : le piège du débutant",
    summary="Pourquoi on entre trop tard, et comment retrouver du sang-froid face à un marché qui s'envole.",
    music=1, seed=39,
    scenes=[
        dict(visual="hook", title="Tu achètes juste quand le prix s'envole ?",
             text="Tu vois un prix s'envoler, tu te dis que tu vas rater l'occasion, et tu achètes en haut ? C'est la peur de rater le mouvement."),
        dict(visual="steps", label="LE PIÈGE", title="Ce qui se passe",
             items=["Le prix a déjà beaucoup monté", "Tu entres tard, avec un stop lointain", "Le prix revient, et tu perds"],
             text="Le prix a déjà beaucoup monté, tu entres tard, avec un stop forcément lointain, et le prix revient vers sa zone d'équilibre. Tu prends alors une perte plus grosse que prévu."),
        dict(visual="steps", label="LE RÉFLEXE", title="Ce qu'il faut te dire",
             items=["Il y aura toujours une autre occasion", "Sans plan, ne rentre pas", "Attends un retour vers une zone logique"],
             text="Dis-toi qu'il y aura toujours une autre occasion. Si ton plan ne te donne pas d'entrée, tu n'entres pas. Et attends un retour du prix vers une zone logique plutôt que de courir derrière lui."),
        dict(visual="recap", title="À retenir", items=["Une occasion manquée ne coûte rien", "Un trade forcé coûte cher", "Ton plan décide, pas l'émotion"],
             text="Retiens : une occasion manquée ne coûte rien, un trade forcé coûte cher, et c'est ton plan qui décide, pas l'émotion du moment."),
    ])

CORRELATION = dict(
    key="correlation", topic="trading", title="Deux trades, un seul risque : la corrélation",
    summary="Pourquoi acheter deux paires proches revient souvent à prendre le même pari deux fois.",
    music=3, seed=40,
    scenes=[
        dict(visual="hook", title="Tu as deux trades ouverts mais un seul pari ?",
             text="Tu as ouvert deux trades différents, mais ils perdent en même temps ? Tu as peut-être pris le même pari deux fois."),
        dict(visual="compare", label="UN EXEMPLE",
             cards=[dict(title="Deux achats corrélés", color=RED, lines=["Euro dollar et livre dollar", "Les deux dépendent du dollar"], result="Si le dollar monte, tu perds deux fois"),
                    dict(title="Deux trades indépendants", color=GREEN, lines=["Des instruments différents", "Des moteurs différents"], result="Le risque est mieux réparti")],
             text="Si tu achètes l'euro dollar et la livre dollar, les deux dépendent beaucoup du dollar : s'il monte, tu perds sur les deux. Deux trades indépendants, avec des moteurs différents, répartissent mieux le risque."),
        dict(visual="steps", label="COMMENT FAIRE", title="Garder un risque maîtrisé",
             items=["Compte les trades corrélés comme un seul", "Divise ton risque entre eux", "Vérifie les devises en commun"],
             text="Compte les trades corrélés comme un seul, et divise ton risque entre eux. Avant d'ouvrir une deuxième position, vérifie si elle partage une devise ou un moteur avec la première."),
        dict(visual="recap", title="À retenir", items=["Trades corrélés = un seul pari", "Le risque total compte", "Vérifie les devises communes"],
             text="Retiens : des trades corrélés forment un seul pari, c'est le risque total qui compte, et vérifie toujours les devises communes avant d'ouvrir une deuxième position."),
    ])

PLAN = dict(
    key="plan-de-trading", topic="trading", title="Ton plan de trading en 6 lignes",
    summary="Ce qu'un plan de trading doit contenir pour éviter les décisions sur un coup de tête.",
    music=2, seed=41,
    scenes=[
        dict(visual="hook", title="Tu décides tes trades sur un coup de tête ?",
             text="Tu prends tes décisions à l'instinct, selon l'humeur du jour ? Un plan écrit change tout, et il tient en six lignes."),
        dict(visual="steps", label="LE PLAN", title="Six lignes à écrire",
             items=["Les instruments que tu trades", "Les heures auxquelles tu trades", "Ta condition d'entrée", "Ton stop et ton objectif", "Ton risque maximal par trade", "Ta limite de pertes par jour"],
             text="Écris les instruments que tu trades, les heures auxquelles tu trades, ta condition d'entrée, ton stop et ton objectif, ton risque maximal par trade, et ta limite de pertes par jour."),
        dict(visual="steps", label="MODE D'EMPLOI", title="Comment l'utiliser",
             items=["Relis-le avant chaque session", "Si une ligne n'est pas respectée, ne rentre pas", "Corrige-le une fois par semaine, pas pendant un trade"],
             text="Relis-le avant chaque session. Si une ligne n'est pas respectée, tu n'entres pas. Et si tu veux le modifier, fais-le une fois par semaine à tête reposée, jamais en plein trade."),
        dict(visual="recap", title="À retenir", items=["Un plan écrit, pas dans ta tête", "Tu le suis ou tu n'entres pas", "Tu l'améliores calmement"],
             text="Retiens : un plan écrit, pas seulement dans ta tête, que tu suis ou pour lequel tu n'entres pas, et que tu améliores calmement, semaine après semaine."),
    ])

SCRIPTS2 = [ORDRES, SESSIONS, ANNONCES, PAIRES, PIP_LOT, STABLECOINS, HALVING, ETHEREUM, PEUR_RATER, CORRELATION, PLAN]
