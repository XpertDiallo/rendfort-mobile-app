from __future__ import annotations

import argparse
import json
import os
import secrets
import time
import urllib.error
import urllib.request
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


ROOT_DIR = Path(__file__).resolve().parents[3]
WEB_DIR = ROOT_DIR / "apps" / "mobile" / "web"
CONTENT_FILE = ROOT_DIR / "content" / "generated" / "seed" / "rendfort_content.json"
APP_CONFIG = {"name": "RENDFORT Maths", "level": "Seconde C", "version": "mvp-v1"}


LESSONS: list[dict[str, Any]] = [
    {
        "id": "nombres-reels",
        "order": 1,
        "competence": "Calculs algebriques et fonctions",
        "theme": "Calculs algebriques",
        "title": "Ensemble des nombres reels",
        "duration": 18,
        "progress": 68,
        "difficulty": "Base solide",
        "abilities": [
            "Comparer deux nombres reels",
            "Interpreter une valeur absolue comme une distance",
            "Resoudre une equation simple avec valeur absolue",
        ],
        "objectives": [
            "Reconnaitre les sous-ensembles de nombres",
            "Utiliser l'ordre dans R",
            "Manipuler la valeur absolue",
            "Encadrer et arrondir un nombre reel",
        ],
        "sections": [
            {
                "id": "situation",
                "title": "Situation d'apprentissage",
                "body": "Sur une droite graduee, deux eleves mesurent l'ecart entre leurs resultats : l'un est a 12,5 et l'autre a 8,75. La notion de distance entre deux nombres permet de decrire cet ecart sans se preoccuper du sens.",
                "formula": "|x - a| represente la distance entre x et a",
            },
            {
                "id": "valeur-absolue",
                "title": "Valeur absolue",
                "body": "La valeur absolue d'un nombre mesure son eloignement par rapport a zero. Elle est toujours positive ou nulle. Pour resoudre |x - a| = r, on cherche les nombres situes a une distance r du nombre a.",
                "formula": "|x - a| = r equivaut a x = a - r ou x = a + r, avec r >= 0",
            },
            {
                "id": "application",
                "title": "Cas concret",
                "body": "Si un controle vise une note de 14 et qu'un eleve obtient x, l'ecart avec l'objectif est |x - 14|. Une note de 12 et une note de 16 sont toutes les deux a 2 points de l'objectif.",
                "formula": "|12 - 14| = |16 - 14| = 2",
            },
        ],
        "quiz_id": "quiz-nombres-reels",
    },
    {
        "id": "polynomes-fractions",
        "order": 2,
        "competence": "Calculs algebriques et fonctions",
        "theme": "Calculs algebriques",
        "title": "Polynomes et fractions rationnelles",
        "duration": 22,
        "progress": 35,
        "difficulty": "Technique",
        "abilities": [
            "Identifier le degre d'un polynome",
            "Factoriser une expression simple",
            "Simplifier une fraction rationnelle dans son domaine",
        ],
        "objectives": [
            "Comprendre degre, coefficient et zero",
            "Factoriser par x - a",
            "Etudier le signe d'une fraction rationnelle simple",
        ],
        "sections": [
            {
                "id": "definition",
                "title": "Polynome",
                "body": "Un polynome est une somme de termes formes avec des puissances entieres positives de x. Son degre est la plus grande puissance de x presente avec un coefficient non nul.",
                "formula": "P(x) = ax^2 + bx + c",
            },
            {
                "id": "factorisation",
                "title": "Factoriser",
                "body": "Factoriser revient a transformer une somme en produit. C'est utile pour resoudre une equation ou etudier un signe.",
                "formula": "x^2 - 9 = (x - 3)(x + 3)",
            },
        ],
        "quiz_id": "quiz-polynomes",
    },
    {
        "id": "equations-inequations-r",
        "order": 3,
        "competence": "Calculs algebriques et fonctions",
        "theme": "Calculs algebriques",
        "title": "Equations et inequations dans R",
        "duration": 25,
        "progress": 18,
        "difficulty": "Progressif",
        "abilities": [
            "Determiner un ensemble de validite",
            "Resoudre une equation se ramenant au premier degre",
            "Utiliser un tableau de signes simple",
        ],
        "objectives": [
            "Transformer une equation sans changer ses solutions",
            "Resoudre des inequations simples",
            "Lire une solution sous forme d'intervalle",
        ],
        "sections": [
            {
                "id": "equivalence",
                "title": "Equations equivalentes",
                "body": "Deux equations sont equivalentes lorsqu'elles ont exactement les memes solutions. Les transformations autorisees doivent conserver cet ensemble de solutions.",
                "formula": "2x + 3 = 7 equivaut a 2x = 4",
            }
        ],
        "quiz_id": "quiz-equations",
    },
    {
        "id": "fonctions-generalites",
        "order": 4,
        "competence": "Calculs algebriques et fonctions",
        "theme": "Fonctions",
        "title": "Generalites sur les fonctions",
        "duration": 20,
        "progress": 0,
        "difficulty": "Visualisation",
        "abilities": [
            "Identifier image et antecedent",
            "Lire une information sur une courbe",
            "Determiner un ensemble de definition simple",
        ],
        "objectives": [
            "Comprendre la notion de fonction",
            "Passer d'un tableau a un graphique",
            "Interpreter les variations",
        ],
        "sections": [
            {
                "id": "notion",
                "title": "Une machine a associer",
                "body": "Une fonction associe a chaque valeur de depart au plus une valeur d'arrivee. On peut la voir comme une machine qui transforme une entree en sortie.",
                "formula": "f : x -> f(x)",
            }
        ],
        "quiz_id": "quiz-fonctions",
    },
    {
        "id": "vecteurs-plan",
        "order": 5,
        "competence": "Geometrie du plan",
        "theme": "Vecteurs et points du plan",
        "title": "Vecteurs et points du plan",
        "duration": 24,
        "progress": 0,
        "difficulty": "Geometrie",
        "abilities": [
            "Representer un vecteur",
            "Reconnaitre deux vecteurs colineaires",
            "Utiliser une base du plan",
        ],
        "objectives": [
            "Relier vecteur et deplacement",
            "Calculer avec des vecteurs",
            "Caracteriser une colinearite",
        ],
        "sections": [
            {
                "id": "deplacement",
                "title": "Vecteur comme deplacement",
                "body": "Un vecteur decrit un deplacement : direction, sens et longueur. Deux deplacements identiques representent le meme vecteur, meme s'ils ne commencent pas au meme point.",
                "formula": "AB = CD lorsque les deux deplacements sont identiques",
            }
        ],
        "quiz_id": "quiz-vecteurs",
    },
]


QUIZZES: dict[str, dict[str, Any]] = {
    "quiz-nombres-reels": {
        "id": "quiz-nombres-reels",
        "lesson_id": "nombres-reels",
        "title": "Quiz : nombres reels",
        "questions": [
            {
                "id": "q1",
                "prompt": "Que represente |x - a| sur une droite graduee ?",
                "choices": ["Une distance", "Une aire", "Une pente", "Un angle"],
                "answer": 0,
                "explanation": "La valeur absolue donne l'ecart entre x et a, donc une distance.",
            },
            {
                "id": "q2",
                "prompt": "Si |x - 5| = 2, quelles sont les solutions ?",
                "choices": ["3 et 7", "2 et 5", "-3 et 7", "5 seulement"],
                "answer": 0,
                "explanation": "Les nombres a distance 2 de 5 sont 5 - 2 et 5 + 2.",
            },
            {
                "id": "q3",
                "prompt": "Une valeur absolue est toujours...",
                "choices": ["negative", "positive ou nulle", "strictement positive", "nulle"],
                "answer": 1,
                "explanation": "Une distance ne peut pas etre negative.",
            },
        ],
    },
    "quiz-polynomes": {
        "id": "quiz-polynomes",
        "lesson_id": "polynomes-fractions",
        "title": "Quiz : polynomes",
        "questions": [
            {
                "id": "q1",
                "prompt": "Quel est le degre de P(x) = 4x^3 - 2x + 1 ?",
                "choices": ["1", "2", "3", "4"],
                "answer": 2,
                "explanation": "La plus grande puissance de x est 3.",
            },
            {
                "id": "q2",
                "prompt": "Quelle factorisation est correcte ?",
                "choices": ["x^2 - 4 = (x - 2)(x + 2)", "x^2 - 4 = (x - 4)(x + 4)", "x^2 - 4 = x(x - 4)", "x^2 - 4 = (x - 2)^2"],
                "answer": 0,
                "explanation": "C'est l'identite remarquable a^2 - b^2.",
            },
        ],
    },
    "quiz-equations": {
        "id": "quiz-equations",
        "lesson_id": "equations-inequations-r",
        "title": "Quiz : equations",
        "questions": [
            {
                "id": "q1",
                "prompt": "Quelle est la solution de 2x + 3 = 7 ?",
                "choices": ["1", "2", "3", "4"],
                "answer": 1,
                "explanation": "2x = 4, donc x = 2.",
            }
        ],
    },
    "quiz-fonctions": {
        "id": "quiz-fonctions",
        "lesson_id": "fonctions-generalites",
        "title": "Quiz : fonctions",
        "questions": [
            {
                "id": "q1",
                "prompt": "Dans f(3) = 7, le nombre 7 est...",
                "choices": ["un antecedent", "une image", "un domaine", "une variable"],
                "answer": 1,
                "explanation": "7 est l'image de 3 par la fonction f.",
            }
        ],
    },
    "quiz-vecteurs": {
        "id": "quiz-vecteurs",
        "lesson_id": "vecteurs-plan",
        "title": "Quiz : vecteurs",
        "questions": [
            {
                "id": "q1",
                "prompt": "Un vecteur decrit principalement...",
                "choices": ["une couleur", "un deplacement", "une note", "un volume"],
                "answer": 1,
                "explanation": "Un vecteur porte direction, sens et longueur.",
            }
        ],
    },
}


def load_seed_content() -> None:
    global APP_CONFIG, LESSONS, QUIZZES
    if not CONTENT_FILE.exists():
        return
    try:
        data = json.loads(CONTENT_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    lessons = data.get("lessons")
    quizzes = data.get("quizzes")
    if isinstance(lessons, list) and isinstance(quizzes, dict) and lessons:
        APP_CONFIG = data.get("app", APP_CONFIG)
        LESSONS = lessons
        QUIZZES = quizzes


load_seed_content()


DEMO_USER = {
    "id": "demo-user",
    "first_name": "Kouadio",
    "last_name": "Eleve",
    "email": "demo@rendfort.local",
    "level": "Seconde C",
    "objective": "Renforcer mes bases",
}

SESSIONS: dict[str, dict[str, Any]] = {}
QUIZ_ATTEMPTS: list[dict[str, Any]] = [
    {
        "quiz_id": LESSONS[0]["quiz_id"],
        "lesson_id": LESSONS[0]["id"],
        "title": LESSONS[0]["title"],
        "score": 16,
        "created_at": "Aujourd'hui",
    },
    {
        "quiz_id": LESSONS[1]["quiz_id"],
        "lesson_id": LESSONS[1]["id"],
        "title": LESSONS[1]["title"],
        "score": 12,
        "created_at": "Hier",
    },
]


def json_response(handler: SimpleHTTPRequestHandler, payload: Any, status: int = 200) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.end_headers()
    handler.wfile.write(body)


def read_json(handler: SimpleHTTPRequestHandler) -> dict[str, Any]:
    length = int(handler.headers.get("Content-Length", "0"))
    if length == 0:
        return {}
    raw = handler.rfile.read(length)
    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


def public_lesson(lesson: dict[str, Any], include_sections: bool = False) -> dict[str, Any]:
    result = {k: v for k, v in lesson.items() if k != "sections"}
    if include_sections:
        result["sections"] = lesson["sections"]
    return result


def dashboard_payload() -> dict[str, Any]:
    completed = sum(1 for lesson in LESSONS if lesson["progress"] >= 80)
    in_progress = sum(1 for lesson in LESSONS if 0 < lesson["progress"] < 80)
    avg_score = round(sum(item["score"] for item in QUIZ_ATTEMPTS) / max(len(QUIZ_ATTEMPTS), 1))
    abilities: list[str] = []
    for lesson in LESSONS:
        if lesson["progress"] > 0:
            abilities.extend(lesson["abilities"][:2])
    return {
        "app": APP_CONFIG,
        "user": DEMO_USER,
        "stats": {
            "study_time": "2h15",
            "mastery": 54,
            "questions": 12,
            "average_score": avg_score,
            "completed_lessons": completed,
            "in_progress_lessons": in_progress,
        },
        "resume_lesson": public_lesson(LESSONS[0]),
        "abilities": abilities[:5],
        "recent_quizzes": QUIZ_ATTEMPTS[-4:][::-1],
        "weak_points": [
            {"title": "Factorisation", "lesson_id": "polynomes-fractions", "hint": "Revoir les produits remarquables."},
            {"title": "Valeur absolue", "lesson_id": "nombres-reels", "hint": "Relier chaque calcul a une distance."},
        ],
    }


def fallback_tutor_answer(question: str, lesson_id: str | None) -> dict[str, Any]:
    lesson = next((item for item in LESSONS if item["id"] == lesson_id), LESSONS[0])
    q = question.lower()
    if "valeur absolue" in q or "distance" in q:
        answer = "Imagine une droite graduee. La valeur absolue mesure seulement l'ecart entre deux points. Elle oublie le sens, donc le resultat reste positif ou nul."
        detected = "valeur_absolue_comme_distance"
    elif "factor" in q or "polynome" in q:
        answer = "Pour factoriser, cherche d'abord un facteur commun ou une identite remarquable. Le but est de remplacer une somme par un produit plus facile a etudier."
        detected = "factorisation"
    elif "fonction" in q:
        answer = "Une fonction associe une valeur de sortie a une valeur d'entree. Quand tu lis f(3), tu demandes quelle sortie correspond a l'entree 3."
        detected = "image_et_antecedent"
    else:
        answer = f"Dans la lecon « {lesson['title']} », reprenons simplement : identifie d'abord ce qu'on te donne, puis ce qu'on cherche. Je peux aussi te donner un exemple proche."
        detected = "besoin_de_reformulation"
    return {
        "answer": answer,
        "suggested_action": "continue_lesson",
        "detected_gap": detected,
        "next_prompt": "Veux-tu un exemple guide avant de continuer ?",
        "source": "local",
    }


def groq_tutor_answer(question: str, lesson_id: str | None, section_id: str | None) -> dict[str, Any] | None:
    api_key = os.environ.get("TUTOR_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    base_url = os.environ.get("TUTOR_BASE_URL", "https://api.groq.com/openai/v1").rstrip("/")
    model = os.environ.get("TUTOR_MODEL", "openai/gpt-oss-20b")
    lesson = next((item for item in LESSONS if item["id"] == lesson_id), LESSONS[0])
    section = next((item for item in lesson["sections"] if item["id"] == section_id), lesson["sections"][0])
    payload = {
        "model": model,
        "temperature": 0.4,
        "max_tokens": 450,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Tu es le tuteur RENDFORT, un professeur de mathematiques Seconde C. "
                    "Reponds en francais simple, avec rigueur. Ne donne pas de solution brute de devoir. "
                    "N'utilise jamais les termes interdits dans l'application. "
                    "Guide l'eleve par intuition, exemple et verification rapide."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Lecon: {lesson['title']}\n"
                    f"Section: {section['title']}\n"
                    f"Extrait: {section['body']}\n"
                    f"Question eleve: {question}"
                ),
            },
        ],
    }
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=18) as response:
            data = json.loads(response.read().decode("utf-8"))
        answer = data["choices"][0]["message"]["content"].strip()
        return {
            "answer": answer,
            "suggested_action": "continue_lesson",
            "detected_gap": "a_preciser",
            "next_prompt": "On continue la lecon ?",
            "source": "provider",
        }
    except (urllib.error.URLError, KeyError, TimeoutError, json.JSONDecodeError):
        return None


class RENDFORTHandler(SimpleHTTPRequestHandler):
    server_version = "RENDFORTPreview/1.0"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/api/v1/health":
            return json_response(self, {"status": "ok", "time": int(time.time())})
        if path == "/api/v1/me":
            return json_response(self, {"user": DEMO_USER})
        if path == "/api/v1/dashboard":
            return json_response(self, dashboard_payload())
        if path == "/api/v1/syllabus":
            groups: dict[str, dict[str, Any]] = {}
            for lesson in LESSONS:
                key = lesson["competence"]
                groups.setdefault(key, {"competence": key, "themes": {}})
                theme = groups[key]["themes"].setdefault(lesson["theme"], [])
                theme.append(public_lesson(lesson))
            response = []
            for group in groups.values():
                response.append(
                    {
                        "competence": group["competence"],
                        "themes": [
                            {"title": title, "lessons": lessons}
                            for title, lessons in group["themes"].items()
                        ],
                    }
                )
            return json_response(self, {"items": response})
        if path == "/api/v1/lessons":
            return json_response(self, {"items": [public_lesson(item) for item in LESSONS]})
        if path.startswith("/api/v1/lessons/"):
            lesson_id = path.rsplit("/", 1)[-1]
            lesson = next((item for item in LESSONS if item["id"] == lesson_id), None)
            if not lesson:
                return json_response(self, {"error": "Lecon introuvable"}, HTTPStatus.NOT_FOUND)
            return json_response(self, public_lesson(lesson, include_sections=True))
        if path.startswith("/api/v1/quizzes/"):
            quiz_id = path.rsplit("/", 1)[-1]
            quiz = QUIZZES.get(quiz_id)
            if not quiz:
                return json_response(self, {"error": "Quiz introuvable"}, HTTPStatus.NOT_FOUND)
            public_questions = [
                {k: v for k, v in question.items() if k not in {"answer", "explanation"}}
                for question in quiz["questions"]
            ]
            return json_response(self, {**quiz, "questions": public_questions})
        if path == "/api/v1/sync/offline-pack":
            return json_response(self, {"lessons": [public_lesson(item, include_sections=True) for item in LESSONS], "quizzes": QUIZZES})
        if path == "/":
            self.path = "/index.html"
            return super().do_GET()
        if not path.startswith("/api/"):
            target = WEB_DIR / path.lstrip("/")
            if target.exists() and target.is_file():
                return super().do_GET()
            self.path = "/index.html"
            return super().do_GET()
        return json_response(self, {"error": "Route introuvable"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        payload = read_json(self)
        if path in {"/api/v1/auth/register", "/api/v1/auth/login"}:
            token = secrets.token_urlsafe(24)
            first_name = payload.get("first_name") or payload.get("firstName") or "Kouadio"
            user = {**DEMO_USER, "first_name": first_name, "email": payload.get("email", DEMO_USER["email"])}
            SESSIONS[token] = user
            return json_response(self, {"token": token, "user": user, "verified": True})
        if path == "/api/v1/auth/verify-email":
            return json_response(self, {"verified": True})
        if path.endswith("/attempts") and path.startswith("/api/v1/quizzes/"):
            quiz_id = path.split("/")[-2]
            quiz = QUIZZES.get(quiz_id)
            if not quiz:
                return json_response(self, {"error": "Quiz introuvable"}, HTTPStatus.NOT_FOUND)
            answers = payload.get("answers", {})
            correct = 0
            corrections = []
            for question in quiz["questions"]:
                selected = answers.get(question["id"])
                is_correct = selected == question["answer"]
                correct += int(is_correct)
                corrections.append(
                    {
                        "question_id": question["id"],
                        "correct": is_correct,
                        "expected": question["answer"],
                        "explanation": question["explanation"],
                    }
                )
            score = round((correct / len(quiz["questions"])) * 20)
            attempt = {
                "quiz_id": quiz_id,
                "lesson_id": quiz["lesson_id"],
                "title": quiz["title"].replace("Quiz : ", ""),
                "score": score,
                "created_at": "Maintenant",
            }
            QUIZ_ATTEMPTS.append(attempt)
            return json_response(self, {"score": score, "corrections": corrections, "attempt": attempt})
        if path in {"/api/v1/tutor/question", "/api/v1/assistant/question"}:
            question = str(payload.get("question", "")).strip()
            if not question:
                return json_response(self, {"error": "Question vide"}, HTTPStatus.BAD_REQUEST)
            lesson_id = payload.get("lesson_id")
            section_id = payload.get("section_id")
            answer = groq_tutor_answer(question, lesson_id, section_id) or fallback_tutor_answer(question, lesson_id)
            return json_response(self, answer)
        if path.startswith("/api/v1/progress/lessons/"):
            lesson_id = path.rsplit("/", 1)[-1]
            progress = int(payload.get("progress", 0))
            for lesson in LESSONS:
                if lesson["id"] == lesson_id:
                    lesson["progress"] = max(lesson["progress"], progress)
                    return json_response(self, {"lesson": public_lesson(lesson)})
            return json_response(self, {"error": "Lecon introuvable"}, HTTPStatus.NOT_FOUND)
        return json_response(self, {"error": "Route introuvable"}, HTTPStatus.NOT_FOUND)


def main() -> None:
    parser = argparse.ArgumentParser(description="RENDFORT preview server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if not WEB_DIR.exists():
        raise SystemExit(f"Frontend introuvable: {WEB_DIR}")

    server = ThreadingHTTPServer((args.host, args.port), RENDFORTHandler)
    print(f"RENDFORT preview running on http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping RENDFORT preview")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
