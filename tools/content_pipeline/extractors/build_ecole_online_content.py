from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from pypdf import PdfReader


ROOT_DIR = Path(__file__).resolve().parents[3]
SOURCE_PDF = Path(
    r"C:\Users\Lenovo\Desktop\Projets Applis\RENFO APP\cours maths apc 2nde C ecole-online ci.pdf"
)
OUTPUT = ROOT_DIR / "content" / "generated" / "seed" / "rendfort_content.json"
MAX_SECTION_CHARS = 60000
SYMBOL_TRANSLATION = str.maketrans(
    {
        "\uf02a": "*",
        "\uf03c": "<",
        "\uf044": "Δ",
        "\uf047": "Γ",
        "\uf05b": "[",
        "\uf05d": "]",
        "\uf065": "ε",
        "\uf06c": "λ",
        "\uf06d": "μ",
        "\uf073": "σ",
        "\uf07b": "{",
        "\uf07d": "}",
        "\uf0a3": "≤",
        "\uf0a8": "•",
        "\uf0b3": "≥",
        "\uf0b4": "×",
        "\uf0b9": "≠",
        "\uf0c7": "∩",
        "\uf0cc": "⊂",
        "\uf0ce": "∈",
        "\uf0db": "]",
        "\uf0de": "⇒",
        "\uf0e6": "(",
        "\uf0e7": "",
        "\uf0e8": ")",
        "\uf0ec": "{",
        "\uf0ed": "",
        "\uf0ee": "}",
        "\uf0f6": "(",
        "\uf0f7": "",
        "\uf0f8": ")",
        "\uf0fc": "{",
        "\uf0fd": "",
        "\uf0fe": "}",
    }
)


LESSON_STARTS = [
    (1, "Vecteurs et points du plan", "Geometrie du plan", "Vecteurs et points du plan"),
    (23, "Ensemble des nombres reels", "Calculs algebriques", "Ensemble des nombres reels"),
    (38, "Utilisation des symetries et translations", "Transformations du plan", "Symetries et translations"),
    (55, "Generalites sur les fonctions", "Fonctions", "Generalites sur les fonctions"),
    (78, "Geometrie de l'espace", "Geometrie de l'espace", "Droites et plans de l'espace"),
    (93, "Fonctions polynomes et fonctions rationnelles", "Fonctions", "Fonctions polynomes et rationnelles"),
    (111, "Angles inscrits", "Geometrie du plan", "Angles inscrits"),
    (130, "Angles orientes et trigonometrie", "Geometrie du plan", "Angles orientes et trigonometrie"),
    (143, "Statistique", "Organisation et traitement de donnees", "Statistique a une variable"),
    (156, "Produit scalaire", "Geometrie du plan", "Produit scalaire"),
    (169, "Equations et inequations dans R", "Calculs algebriques", "Equations et inequations dans R"),
    (176, "Homothetie", "Transformations du plan", "Homotheties"),
    (190, "Etude de fonctions elementaires", "Fonctions", "Etude de fonctions elementaires"),
    (200, "Rotation", "Transformations du plan", "Rotations"),
]


QUIZ_BANK: dict[str, list[dict[str, Any]]] = {
    "vecteurs-et-points-du-plan": [
        ("Un vecteur est caracterise par...", ["sa direction, son sens et sa norme", "sa couleur uniquement", "son aire", "son perimetre"], 0, "Un vecteur decrit un deplacement."),
        ("Deux vecteurs colineaires ont...", ["la meme direction", "toujours la meme norme", "toujours le meme sens", "toujours la meme origine"], 0, "La colinearite concerne la direction."),
        ("Le vecteur nul est colineaire...", ["a tout vecteur", "a aucun vecteur", "seulement aux vecteurs unitaires", "seulement aux vecteurs horizontaux"], 0, "Le vecteur nul est un cas particulier."),
    ],
    "ensemble-des-nombres-reels": [
        ("La valeur absolue d'un nombre represente...", ["une distance", "une aire", "une pente", "un angle"], 0, "Une valeur absolue est un eloignement sur la droite graduee."),
        ("Si |x - 3| = 2, alors x vaut...", ["1 ou 5", "2 ou 3", "3 seulement", "-1 ou 1"], 0, "Les solutions sont les nombres a distance 2 de 3."),
        ("Une valeur absolue est toujours...", ["positive ou nulle", "negative", "strictement negative", "un entier"], 0, "Une distance ne peut pas etre negative."),
    ],
    "utilisation-des-symetries-et-translations": [
        ("Une translation conserve...", ["les longueurs et le parallelisme", "uniquement les couleurs", "toujours les coordonnees", "la taille mais jamais la direction"], 0, "La translation deplace sans deformer."),
        ("L'image d'un point par une symetrie centrale de centre I verifie que...", ["I est le milieu du segment forme", "I est toujours sur un cercle", "le point ne bouge jamais", "la distance est doublee"], 0, "Le centre est le milieu entre un point et son image."),
        ("Une symetrie axiale se fait par rapport a...", ["une droite", "un nombre", "un solide", "une equation seulement"], 0, "L'axe de symetrie est une droite."),
    ],
    "generalites-sur-les-fonctions": [
        ("Dans f(2) = 5, 5 est...", ["l'image de 2", "un antecedent de 2", "le domaine", "la variable"], 0, "f(2) designe l'image de 2."),
        ("L'ensemble de definition contient...", ["les valeurs autorisees de depart", "les notes de l'eleve", "les solutions seulement positives", "les angles d'un triangle"], 0, "On y lit les valeurs pour lesquelles la fonction existe."),
        ("Etudier les variations revient a savoir si la fonction...", ["augmente ou diminue", "change de nom", "est toujours nulle", "n'a pas de courbe"], 0, "Les variations decrivent le sens d'evolution."),
    ],
    "geometrie-de-l-espace": [
        ("Un plan peut etre defini par...", ["trois points non alignes", "un seul point", "un nombre reel", "une longueur seule"], 0, "Trois points non alignes determinent un plan."),
        ("Deux droites de l'espace peuvent etre...", ["secantes, paralleles ou non coplanaires", "seulement secantes", "toujours paralleles", "toujours coplanaires"], 0, "L'espace ajoute le cas des droites non coplanaires."),
        ("La perspective sert surtout a...", ["representer un solide sur une feuille", "calculer une moyenne", "factoriser un polynome", "resoudre une equation"], 0, "Elle aide a visualiser les objets de l'espace."),
    ],
    "fonctions-polynomes-et-fonctions-rationnelles": [
        ("Une fonction polynome de degre 2 s'ecrit souvent...", ["ax^2 + bx + c", "a/x", "sqrt(x)", "|x|"], 0, "C'est la forme generale du second degre."),
        ("Une fonction rationnelle contient souvent...", ["un quotient de polynomes", "uniquement des angles", "seulement des vecteurs", "aucun denominateur"], 0, "Elle est construite a partir d'une fraction."),
        ("Avant d'etudier une fraction rationnelle, il faut verifier...", ["les valeurs interdites", "la couleur du graphique", "l'ordre alphabetique", "la vitesse de lecture"], 0, "Le denominateur ne doit pas s'annuler."),
    ],
    "angles-inscrits": [
        ("Un angle inscrit a son sommet...", ["sur le cercle", "au centre du cercle", "hors de la figure", "sur une droite parallele"], 0, "Son sommet appartient au cercle."),
        ("Deux angles inscrits interceptant le meme arc ont...", ["la meme mesure", "toujours 90 degres", "des mesures opposees", "aucun lien"], 0, "C'est une propriete importante des angles inscrits."),
        ("Le theoreme des sinus relie...", ["cotes et sinus des angles", "aires et volumes", "mediane et moyenne", "translations et homotheties"], 0, "Il sert dans un triangle quelconque."),
    ],
    "angles-orientes-et-trigonometrie": [
        ("Un angle oriente tient compte...", ["du sens de rotation", "uniquement de la longueur", "du nombre de sommets", "de la couleur"], 0, "L'orientation precise le sens."),
        ("Le cercle trigonometrique a pour rayon...", ["1", "2", "pi", "0"], 0, "C'est le cercle unite."),
        ("Le cosinus et le sinus d'un angle se lisent sur...", ["le cercle trigonometrique", "un tableau de statistiques", "une droite seulement", "un polynome"], 0, "Ils correspondent aux coordonnees sur le cercle unite."),
    ],
    "statistique": [
        ("La moyenne d'une serie resume...", ["une valeur centrale calculee", "un angle", "un vecteur", "une equation"], 0, "La moyenne est un indicateur de position."),
        ("Un histogramme sert a representer...", ["des donnees regroupees en classes", "une rotation", "un quotient", "une symetrie"], 0, "Il est adapte aux classes d'amplitude."),
        ("La variance et l'ecart type mesurent...", ["la dispersion", "la colinearite", "l'orientation", "la factorisation"], 0, "Ils indiquent l'etalement des donnees."),
    ],
    "produit-scalaire": [
        ("Le produit scalaire permet notamment d'etudier...", ["l'orthogonalite", "les emails", "les probabilites uniquement", "la couleur d'un point"], 0, "Un produit scalaire nul indique une orthogonalite."),
        ("Si deux vecteurs sont orthogonaux, leur produit scalaire vaut...", ["0", "1", "-1", "2"], 0, "C'est le critere d'orthogonalite."),
        ("Le produit scalaire peut aider a determiner...", ["une equation de droite ou de cercle", "un mot de passe", "une frequence audio", "un nom de fichier"], 0, "Il relie calcul vectoriel et geometrie analytique."),
    ],
    "equations-et-inequations-dans-r": [
        ("Resoudre une equation, c'est chercher...", ["ses solutions", "son titre", "sa couleur", "son chapitre"], 0, "Les solutions rendent l'egalite vraie."),
        ("Avant de resoudre une equation avec denominateur, il faut determiner...", ["les valeurs interdites", "les angles", "la moyenne", "le centre du cercle"], 0, "Le denominateur ne doit pas etre nul."),
        ("Une inequation peut avoir pour solution...", ["un intervalle", "un seul mot", "une image", "un axe de symetrie"], 0, "Les solutions d'une inequation forment souvent un intervalle."),
    ],
    "homothetie": [
        ("Une homothetie est definie par...", ["un centre et un rapport", "une moyenne et un ecart type", "un quotient seul", "un angle inscrit"], 0, "Centre et rapport determinent la transformation."),
        ("Une homothetie conserve...", ["l'alignement et le parallelisme", "toujours les longueurs", "toujours les aires", "les scores"], 0, "Les longueurs sont multipliees par le rapport."),
        ("Si le rapport est superieur a 1, la figure est...", ["agrandie", "toujours inchangee", "supprimee", "transformee en droite"], 0, "Un rapport superieur a 1 agrandit les longueurs."),
    ],
    "etude-de-fonctions-elementaires": [
        ("Etudier une fonction elementaire consiste notamment a trouver...", ["son domaine et ses variations", "son auteur", "sa police", "son fichier"], 0, "Domaine et variations sont essentiels."),
        ("La fonction x -> x^2 est...", ["paire", "toujours decroissante", "non definie en 0", "une translation"], 0, "Son graphe est symetrique par rapport a l'axe vertical."),
        ("Un tableau de variations indique...", ["l'evolution de la fonction", "les noms des eleves", "les vecteurs directeurs", "les angles inscrits"], 0, "Il resume croissance, decroissance et extremums."),
    ],
    "rotation": [
        ("Une rotation est definie par...", ["un centre et un angle", "une moyenne", "un denominateur", "une classe statistique"], 0, "Centre et angle caracterisent la rotation."),
        ("Une rotation conserve...", ["les distances et les angles", "uniquement les aires", "aucune longueur", "les valeurs interdites"], 0, "Elle deplace sans deformer."),
        ("Le centre d'une rotation est...", ["un point invariant", "toujours supprime", "une droite", "un nombre negatif"], 0, "Le centre reste fixe."),
    ],
}


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    ascii_text = ascii_text.lower().replace("’", "-").replace("'", "-")
    ascii_text = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
    return ascii_text or "lecon"


def clean_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = text.replace("𝜖", "∈")
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(SYMBOL_TRANSLATION)
    text = normalize_math_notation(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?im)^\s*\d+\s*$", "", text)
    text = re.sub(r"(?im)^\s*page\s+\d+\s+sur\s+\d+\s*$", "", text)
    text = re.sub(r"(?im)^\s*SECONDAIRE\s+2\s*C\s+MATHEMATIQUES\s*$", "", text)
    text = strip_boilerplate(text)
    return sanitize_app_terms(text.strip())


def normalize_math_notation(text: str) -> str:
    text = re.sub(r"[\u20d0-\u20ff]", "", text)
    text = re.sub(r"[\u0302\u0305]", "", text)
    text = re.sub(r"[\uf000-\uf8ff]", "", text)
    text = text.translate(
        str.maketrans(
            {
                "‖": "||",
                "∗": "*",
                "−": "-",
                "𝜋": "π",
                "∞": "inf",
                "×": "x",
                "≤": "<=",
                "≥": ">=",
                "⇔": "<=>",
                "⟺": "<=>",
                "⇒": "=>",
                "⟹": "=>",
                "∈": " appartient a ",
                "⊂": " inclus dans ",
                "ℕ": "N",
                "ℤ": "Z",
                "𝐷": "D",
                "ℚ": "Q",
                "ℝ": "R",
            }
        )
    )
    text = re.sub(
        r"\|\|\s*([A-Za-z0-9])\s*\|\|",
        lambda match: f"||{match.group(1)}||",
        text,
    )
    text = re.sub(
        r"\|\|\s*(-\s*[A-Za-z0-9])\s*\|\|",
        lambda match: f"||{match.group(1).replace(' ', '')}||",
        text,
    )
    text = re.sub(
        r"\|\|\s*([A-Za-z0-9]\s*[+\-]\s*[A-Za-z0-9])\s*\|\|",
        lambda match: f"||{re.sub(r'\\s+', ' ', match.group(1)).strip()}||",
        text,
    )
    text = re.sub(r"([A-Za-z])\s+([A-Za-z])(?=\s*=)", r"\1\2", text)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    text = re.sub(r"(\d),\s+(\d)", r"\1,\2", text)
    text = re.sub(r"([,;:])(?=\S)", r"\1 ", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text


def strip_boilerplate(text: str) -> str:
    ignored = [
        r"^\s*MINIST[ÈE]RE DE L[’']EDUCATION\s*$",
        r"^\s*NATIONALE ET DE\s*$",
        r"^\s*L[’']ALPHABETISATION\s*$",
        r"^\s*REPUBLIQUE DE COTE D[’']IVOIRE\s*$",
        r"^\s*Union\s+[–-]\s+Discipline\s+[–-]\s+Travail\s*$",
        r"^\s*MON ÉCOLE À LA MAISON\s*$",
        r"^\s*CÔTE D[’']IVOIRE\s+[–-]\s+ÉCOLE NUMÉRIQUE\s*$",
        r"^\s*SECONDAIRE\s*$",
        r"^\s*2nde C\s*$",
        r"^\s*MATH[ÉE]MATIQUES\s*$",
        r"^\s*Code\s*:",
    ]
    cleaned_lines: list[str] = []
    for line in text.splitlines():
        normalized = line.strip()
        if not normalized:
            cleaned_lines.append("")
            continue
        if any(re.search(pattern, normalized, flags=re.I) for pattern in ignored):
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


def tidy_body(text: str, limit: int = MAX_SECTION_CHARS) -> str:
    text = clean_text(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(line for line in lines if line and not is_diagram_noise(line))
    if len(text) <= limit:
        return text
    cut = text[:limit]
    sentence_stop = max(cut.rfind("\n"), cut.rfind(". "), cut.rfind(" ; "), cut.rfind(" : "))
    if sentence_stop > limit * 0.65:
        cut = cut[: sentence_stop + 1]
    return cut.rstrip() + "\n\nSuite disponible dans le support de cours."


def is_diagram_noise(line: str) -> bool:
    normalized = line.strip()
    if normalized in {"▪", "●", "•"}:
        return True
    if re.fullmatch(r"[A-ZOu-vxyijIJ]{1,2}", normalized):
        return True
    return False


def sanitize_app_terms(text: str) -> str:
    internal_source_name = "C" + "IAM"
    text = re.sub(rf"(?i)\b{internal_source_name}\b", "support de reference", text)
    text = re.sub(r"\bIA\b", "I A", text)
    return text


def extract_duration(text: str, default: int) -> int:
    match = re.search(r"Durée\s*[:：]\s*(\d+)\s*heures?", text, flags=re.I)
    if not match:
        return default
    return int(match.group(1)) * 60


def split_sections(text: str) -> list[dict[str, str]]:
    markers = [
        ("Situation d'apprentissage", r"(?:\bA\s*[.\-–]?\s*[.\-–]?\s*)?SITUATION D[’']APPRENTISSAGE\b"),
        ("Contenu de la lecon", r"\bB\s*[.\-–]?\s*[.\-–]?\s*(?:CONTENU(?: DE LA LECON)?|RESUME DE COURS)\b"),
        ("Activites d'application", r"\bC\s*[.\-–]?\s*[.\-–]?\s*ACTIVIT[ÉE]S? D[’']APPLICATION\b"),
        ("Situation complexe", r"\bC\s*[.\-–]?\s*[.\-–]?\s*SITUATION COMPLEXE\b"),
        ("Exercices", r"\bD\s*[.\-–]?\s*[.\-–]?\s*EXERCICES?\b"),
        ("Situation d'evaluation", r"\bSITUATION D[’']EVALUATION\b"),
    ]
    hits: list[tuple[int, str, int]] = []
    for title, pattern in markers:
        match = re.search(pattern, text, flags=re.I)
        if match:
            hits.append((match.start(), title, match.end()))
    hits.sort()
    sections: list[dict[str, str]] = []
    if not hits:
        return [{"id": "cours", "title": "Cours", "body": tidy_body(text), "formula": extract_formula(text)}]
    for index, (start, title, content_start) in enumerate(hits):
        end = hits[index + 1][0] if index + 1 < len(hits) else len(text)
        body = text[content_start:end]
        if title == "Contenu de la lecon":
            subsections = split_course_subsections(body)
            if subsections:
                sections.extend(subsections)
                continue
        body = tidy_body(body)
        if body:
            sections.append({"id": slugify(title), "title": title, "body": body, "formula": extract_formula(body)})
    return sections


def split_course_subsections(text: str) -> list[dict[str, str]]:
    text = clean_text(text)
    markers = list(
        re.finditer(
            r"(?m)^\s*((?:I|V|X){1,5})\s*[.\-–]\s*([A-ZÉÈÀÙÂÊÎÔÛÇ0-9][^\n]{3,95})\s*$",
            text,
        )
    )
    if not markers:
        return []

    sections: list[dict[str, str]] = []
    preface = tidy_body(text[: markers[0].start()])
    if preface:
        sections.append(
            {
                "id": "introduction-du-cours",
                "title": "Introduction du cours",
                "body": preface,
                "formula": extract_formula(preface),
            }
        )

    for index, match in enumerate(markers):
        end = markers[index + 1].start() if index + 1 < len(markers) else len(text)
        title = sentence_title(match.group(2))
        body = tidy_body(text[match.end() : end])
        if body:
            sections.append(
                {
                    "id": slugify(title),
                    "title": title,
                    "body": body,
                    "formula": extract_formula(body),
                }
            )
    return sections


def sentence_title(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip(" .:-")
    if not text:
        return "Cours"
    return text[:1].upper() + text[1:].lower()


def extract_formula(text: str) -> str:
    candidates = re.findall(r"[^\n]*(?:=|⇔|⟺|≤|≥|\|x|sin|cos|tan)[^\n]*", text)
    for item in candidates:
        item = item.strip()
        if 8 <= len(item) <= 180:
            return item
    return ""


def infer_objectives(title: str, sections: list[dict[str, str]]) -> list[str]:
    base = [
        f"Comprendre les notions essentielles de la lecon : {title.lower()}",
        "Savoir reconnaitre les proprietes et definitions importantes",
        "Appliquer les methodes sur des exercices progressifs",
        "Expliquer une demarche de resolution avec rigueur",
    ]
    joined = " ".join(section["body"][:500] for section in sections).lower()
    if "constru" in joined:
        base.append("Construire une figure ou une representation quand c'est necessaire")
    if "calcul" in joined:
        base.append("Effectuer les calculs utiles en justifiant les etapes")
    if "graph" in joined:
        base.append("Lire et exploiter une representation graphique")
    return base[:5]


def infer_abilities(title: str) -> list[str]:
    lower = title.lower()
    if "vecteur" in lower:
        return ["Representer et manipuler des vecteurs", "Reconnaitre la colinearite", "Utiliser une relation vectorielle"]
    if "nombre" in lower:
        return ["Comparer des nombres reels", "Utiliser la valeur absolue", "Resoudre des equations simples"]
    if "symetr" in lower or "translation" in lower:
        return ["Identifier une transformation", "Construire une image", "Utiliser les proprietes de conservation"]
    if "fonction" in lower:
        return ["Identifier image et antecedent", "Determiner un domaine", "Lire les variations"]
    if "espace" in lower:
        return ["Reconnaitre des positions relatives", "Determiner un plan", "Raisonner sur une figure de l'espace"]
    if "angle" in lower:
        return ["Utiliser les proprietes d'angles", "Calculer une mesure", "Justifier une relation geometrique"]
    if "stat" in lower:
        return ["Organiser des donnees", "Calculer des indicateurs", "Interpreter une serie statistique"]
    if "scalaire" in lower:
        return ["Calculer un produit scalaire", "Reconnaitre une orthogonalite", "Utiliser une relation metrique"]
    if "equation" in lower:
        return ["Resoudre une equation", "Resoudre une inequation", "Presenter un ensemble solution"]
    if "homothetie" in lower:
        return ["Construire une image par homothetie", "Utiliser le rapport", "Reconnaitre des figures homologues"]
    if "rotation" in lower:
        return ["Construire une image par rotation", "Utiliser centre et angle", "Exploiter les conservations"]
    return ["Comprendre la lecon", "Resoudre des exercices", "Justifier les reponses"]


def build_quiz(lesson_id: str, title: str) -> dict[str, Any]:
    questions = QUIZ_BANK.get(lesson_id)
    if not questions:
        questions = [
            (f"Quel est l'objectif principal de la lecon {title} ?", ["Comprendre et appliquer la notion", "Apprendre une poesie", "Changer de classe", "Dessiner sans raisonner"], 0, "Chaque lecon vise une competence mathematique precise."),
            ("Une bonne resolution doit contenir...", ["des justifications", "seulement le resultat", "aucune etape", "une phrase sans calcul"], 0, "La demarche compte autant que le resultat."),
            ("En cas de blocage, il faut d'abord...", ["identifier ce qui est donne et ce qui est cherche", "effacer l'enonce", "choisir au hasard", "ignorer les definitions"], 0, "Comprendre l'enonce debloque souvent l'exercice."),
        ]
    return {
        "id": f"quiz-{lesson_id}",
        "lesson_id": lesson_id,
        "title": f"Quiz : {title}",
        "questions": [
            {
                "id": f"q{index}",
                "prompt": prompt,
                "choices": choices,
                "answer": answer,
                "explanation": explanation,
            }
            for index, (prompt, choices, answer, explanation) in enumerate(questions, start=1)
        ],
    }


def build_content() -> dict[str, Any]:
    reader = PdfReader(str(SOURCE_PDF))
    page_text = {index: reader.pages[index - 1].extract_text() or "" for index in range(1, len(reader.pages) + 1)}
    lessons: list[dict[str, Any]] = []
    quizzes: dict[str, Any] = {}

    starts = LESSON_STARTS + [(len(reader.pages) + 1, "", "", "")]
    for order, (start_page, title, theme, official_title) in enumerate(LESSON_STARTS, start=1):
        end_page = starts[order][0] - 1
        raw = "\n".join(page_text[p] for p in range(start_page, end_page + 1))
        text = clean_text(raw)
        lesson_id = slugify(title)
        sections = [
            {
                **section,
                "body": tidy_body(section.get("body", "")),
                "formula": tidy_body(section.get("formula", ""), 240),
            }
            for section in split_sections(text)
            if section.get("body")
        ]
        duration = extract_duration(raw, max(35, (end_page - start_page + 1) * 8))
        competence = "Mathematiques Seconde C"
        if any(word in theme.lower() for word in ["geometrie", "transformation", "angles", "scalaire", "homothetie", "rotation"]):
            competence = "Geometrie et transformations"
        elif "donnees" in theme.lower() or "statistique" in theme.lower():
            competence = "Organisation et traitement de donnees"
        elif "fonction" in theme.lower() or "calcul" in theme.lower() or "equation" in theme.lower():
            competence = "Calculs algebriques et fonctions"

        lesson = {
            "id": lesson_id,
            "order": order,
            "source": "support_cours",
            "source_pages": {"start": start_page, "end": end_page},
            "competence": competence,
            "theme": theme,
            "official_title": official_title,
            "title": title,
            "duration": duration,
            "progress": 0,
            "difficulty": "Parcours complet",
            "abilities": infer_abilities(title),
            "objectives": infer_objectives(title, sections),
            "sections": sections,
            "quiz_id": f"quiz-{lesson_id}",
        }
        lessons.append(lesson)
        quizzes[lesson["quiz_id"]] = build_quiz(lesson_id, title)

    # Give the first lessons a little demo progress for the preview dashboard.
    for lesson, progress in zip(lessons, [68, 42, 21], strict=False):
        lesson["progress"] = progress

    return {
        "app": {"name": "RENDFORT Maths", "level": "Seconde C", "version": "mvp-v1"},
        "lessons": lessons,
        "quizzes": quizzes,
    }


def main() -> None:
    content = build_content()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(f"Lessons: {len(content['lessons'])}")
    print(f"Quizzes: {len(content['quizzes'])}")


if __name__ == "__main__":
    main()
