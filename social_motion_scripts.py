"""Scenarios 'motion design'. Voir social_motion.py pour la syntaxe. Chiffres verifies : 0,99^10 = 90,4 % ; 0,9^10 = 34,9 % ;
revenir de -65,1 % demande +186,8 % ; semaine : -1 +2 -1 -1 +2 = +1 (taux de reussite 40 %)."""

CTA_TEXT = "Pour progresser avec nous, {y|rejoins la communauté Telegram}. Le lien est dans la bio."

RISQUE = dict(
    key="risque-1-pourcent", topic="trading", title="Dix pertes de suite : combien te reste-t-il ?",
    summary="Avec 1 % de risque, tu survis à une mauvaise série. Avec 10 %, il ne reste presque rien. Les 3 règles pour rester dans le jeu.",
    music=3,
    beats=[
        dict(text="{y|Dix pertes} de suite. Ça arrive à tous les traders."),
        dict(text="Alors, combien te reste-t-il ?", min=2.0),
        dict(text="Avec {g|1 %} de risque, il te reste {g|90 %}.", min=3.6),
        dict(text="Avec {r|10 %} de risque, il te reste {r|35 %}.", min=3.6),
        dict(text="Même série de pertes. {b|Deux destins} différents."),
        dict(text="Pour revenir au point de départ après {r|-65 %}, il faut gagner {b|+187 %}.",
             say="Pour revenir au point de départ après une perte de 65 %, il faut gagner 187 %.", min=3.8),
        dict(text="Pour rester dans le jeu, {b|trois règles}."),
        dict(text="Un : {y|1 %} de risque, pas plus."),
        dict(text="Deux : un {r|stop} posé avant d'entrer."),
        dict(text="Trois : une {g|limite} de pertes par jour."),
        dict(text="{g|Survivre} d'abord. Progresser ensuite."),
        dict(text=CTA_TEXT, min=3.4),
    ],
    elements=[
        dict(type="candles", at=0, until=2, y=200),
        dict(type="chip", at=1, until=2, y=170, text="10 pertes de suite", col="r"),
        dict(type="bars", at=2, until=5, x=46, y=190, w=628, h=240, title="RISQUE 1 % PAR TRADE", tcol="g",
             values=[0.99 ** k for k in range(1, 11)], c0="g", c1="g", final="90,4 %", fcol="g"),
        dict(type="bars", at=3, until=5, x=46, y=455, w=628, h=240, title="RISQUE 10 % PAR TRADE", tcol="r",
             values=[0.9 ** k for k in range(1, 11)], c0="y", c1="r", final="34,9 %", fcol="r"),
        dict(type="big", at=4, until=5, y=770, lines=["MÊME SÉRIE", "DEUX DESTINS"], cols=["m", "b"], size=40, lh=58),
        dict(type="stat", at=5, until=6, x=190, y=420, label="PERTE", text="-65 %", col="r", size=72, delay=0.4),
        dict(type="stat", at=5, until=6, x=520, y=420, label="GAIN NÉCESSAIRE", text="+187 %", col="b", size=72, delay=2.0),
        dict(type="cards", at=6, until=10, y=200,
             items=[dict(beat=7, title="1 % de risque", icon="gauge", col="y"),
                    dict(beat=8, title="Stop posé avant", icon="stop", col="r"),
                    dict(beat=9, title="Limite par jour", icon="lock", col="g")]),
        dict(type="big", at=10, until=11, y=330, lines=["SURVIVRE", "D'ABORD"], cols=["g", "w"], size=84, lh=110),
        dict(type="cta", at=11, y=190, delay=0.5),
    ])

SEMAINE = dict(
    key="ratio-semaine", topic="trading", title="Trois pertes sur cinq, et pourtant gagnant",
    summary="Une semaine de trades montre pourquoi le rapport gain sur risque compte plus que le taux de réussite.",
    music=0,
    beats=[
        dict(text="Cette semaine, tu prends {y|cinq trades}."),
        dict(text="Lundi : une {r|perte}. Tu perds ce que tu risquais.", min=3.0),
        dict(text="Mardi : un {g|gain}, deux fois ce que tu risquais.", min=3.2),
        dict(text="Mercredi, jeudi : deux {r|pertes}.", min=3.0),
        dict(text="Vendredi : un {g|gain}, encore deux fois le risque.", min=3.2),
        dict(text="Trois pertes, deux gains. Tu n'as eu raison que {b|40 %} du temps.", min=3.6),
        dict(text="Et pourtant, le bilan est {g|positif}. Plus une fois ton risque.",
             say="Et pourtant, le bilan est positif : plus une fois ton risque.", min=3.4),
        dict(text="Le secret : ce n'est pas d'avoir raison souvent. C'est de {b|gagner plus} quand tu as raison.", min=4.4),
        dict(text="Alors, trois choses à faire.", min=2.2),
        dict(text="Un : note chaque trade en {b|multiple} de ton risque.", min=3.2),
        dict(text="Deux : vise au moins {y|deux fois} ton risque.", min=3.0),
        dict(text="Trois : juge ta méthode sur {b|50 trades}, pas sur cinq.", min=3.2),
        dict(text=CTA_TEXT, min=3.4),
    ],
    elements=[
        dict(type="chip", at=0, until=8, y=185, text="1R = ce que tu risques par trade", col="b"),
        dict(type="week", at=0, until=8, y=360, days=["LUN", "MAR", "MER", "JEU", "VEN"],
             trades=[dict(day=0, beat=1, text="-1R", col="r"), dict(day=1, beat=2, text="+2R", col="g"),
                     dict(day=2, beat=3, text="-1R", col="r", delay=0.25), dict(day=3, beat=3, text="-1R", col="r", delay=1.5),
                     dict(day=4, beat=4, text="+2R", col="g")]),
        dict(type="stat", at=5, until=8, x=190, y=620, label="TAUX DE RÉUSSITE", text="40 %", col="b", size=64),
        dict(type="stat", at=6, until=8, x=530, y=620, label="BILAN DE LA SEMAINE", text="+1R", col="g", size=64),
        dict(type="big", at=7, until=8, y=760, lines=["GAIN MOYEN : 2R", "PERTE MOYENNE : 1R"], cols=["g", "r"], size=34, lh=56),
        dict(type="cards", at=8, until=12, y=200,
             items=[dict(beat=9, title="Note en multiple de R", icon="book", col="b"),
                    dict(beat=10, title="Gain ≥ 2 × le risque", icon="target", col="y"),
                    dict(beat=11, title="Juge sur 50 trades", icon="count", col="g")]),
        dict(type="cta", at=12, y=190, delay=0.5),
    ])

MOTION = [RISQUE, SEMAINE]
