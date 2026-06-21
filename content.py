"""Curated scientific content extracted from the thesis."""

STUDIES = [
    {
        "chapter": "01",
        "domain": "Santé du sommeil",
        "dimension": "Relations",
        "sample": "35 808",
        "method": "Réseaux comparatifs · 39 variables · âge et sexe",
        "result": "Le sommeil non-récupérateur structure le réseau, avec la somnolence diurne excessive et l’irrégularité circadienne.",
        "clinical": "Privilégier une lecture globale de la santé du sommeil, puis l’adapter à l’âge et au sexe.",
        "accent": "#2DE2E6",
    },
    {
        "chapter": "02",
        "domain": "Addictologie",
        "dimension": "Temporalité",
        "sample": "8 260",
        "method": "211 patients · EMA · mlVAR · 14 jours",
        "result": "Le craving à T0 prédit l’usage à T1 (r = 0,10) ; l’auto-efficacité joue un rôle modérateur indépendant.",
        "clinical": "Repérer les moteurs dynamiques à court terme plutôt que lire uniquement des états moyens.",
        "accent": "#FF4FD8",
    },
    {
        "chapter": "03",
        "domain": "Catatonie",
        "dimension": "Intervention",
        "sample": "136",
        "method": "BFCRS · spinglass · comparaison · NOA",
        "result": "Trois clusters sont stables ; l’immobilité/stupeur est l’unique prédicteur direct de réponse au lorazépam.",
        "clinical": "L’effet d’un traitement peut entrer dans le réseau par un symptôme précis sans reconfigurer toute sa structure.",
        "accent": "#A8FF60",
    },
    {
        "chapter": "04",
        "domain": "Épileptologie",
        "dimension": "Explication",
        "sample": "42",
        "method": "469 crises · SEEG · réseau hybride à 32 nœuds",
        "result": "L’altération de la conscience est la variable sémiologique la plus centrale ; le cingulaire antérieur domine les régions cérébrales.",
        "clinical": "Articuler sémiologie et activité cérébrale comme un système distribué, avec prudence sur la robustesse.",
        "accent": "#9B8CFF",
    },
]

PRINCIPLES = [
    ("RELATIONS", "Les symptômes ne sont pas indépendants : leur sens clinique vient aussi de leurs connexions."),
    ("TEMPORALITÉ", "L’état clinique est une trajectoire faite de transitions, de seuils et de rétroactions."),
    ("INTERVENTION", "Le traitement agit comme une perturbation du système et peut modifier sa trajectoire."),
    ("EXPLICATION", "Les mécanismes internes doivent être reliés aux symptômes et au contexte, sans cause unique réductrice."),
]

LIMITS = [
    "Réseaux populationnels : les associations observées ne décrivent pas nécessairement un individu.",
    "Centralité : importance statistique ne signifie ni causalité directe ni cible thérapeutique automatique.",
    "Études transversales : elles ne permettent pas d’inférer les dynamiques temporelles.",
    "Réseau hybride en épileptologie : N = 42 et coefficient de stabilité d’environ 0,05.",
    "Simulation X–Y–Z : démonstration pédagogique, non ajustée aux données cliniques de la thèse.",
]
