from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

import streamlit as st


DATA_PATH = Path("content/generated/seed/rendfort_content.json")


@st.cache_data
def load_content(content_mtime: float) -> dict[str, Any]:
    if not DATA_PATH.exists():
        st.error("Le fichier de contenu est introuvable.")
        st.stop()
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def clean(value: Any) -> str:
    return html.escape(str(value or ""))


def lesson_minutes(lesson: dict[str, Any]) -> int:
    duration = int(lesson.get("duration", 0))
    return max(8, round(duration / 60)) if duration > 90 else max(8, duration)


def lesson_page_label(lesson: dict[str, Any]) -> str:
    pages = lesson.get("source_pages") or {}
    start = pages.get("start")
    end = pages.get("end")
    if not start or not end:
        return ""
    return f" - pages du support : {start}-{end}"


def get_lesson_quiz(data: dict[str, Any], lesson: dict[str, Any]) -> dict[str, Any] | None:
    quiz_id = lesson.get("quiz_id")
    quizzes = data.get("quizzes", {})
    return quizzes.get(quiz_id) if isinstance(quizzes, dict) else None


def score_quiz(quiz: dict[str, Any], answers: dict[str, int]) -> tuple[int, list[dict[str, Any]]]:
    questions = quiz.get("questions", [])
    correct_count = 0
    corrections = []

    for question in questions:
        question_id = question["id"]
        expected = int(question["answer"])
        selected = answers.get(question_id)
        is_correct = selected == expected
        correct_count += int(is_correct)
        corrections.append(
            {
                "prompt": question["prompt"],
                "selected": selected,
                "expected": expected,
                "choices": question["choices"],
                "is_correct": is_correct,
                "explanation": question.get("explanation", ""),
            }
        )

    total = max(len(questions), 1)
    return round((correct_count / total) * 20), corrections


def inject_theme() -> None:
    st.markdown(
        """
        <style>
        #MainMenu, footer, header { visibility: hidden; }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(241, 184, 75, 0.16), transparent 30%),
                linear-gradient(135deg, #f8f5ed 0%, #eef6f3 100%);
            color: #17212b;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2.2rem;
            padding-bottom: 4rem;
        }

        [data-testid="stSidebar"] {
            background: #edf2f3;
            border-right: 1px solid rgba(23, 33, 43, 0.08);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #17212b;
        }

        [data-testid="stMetric"] {
            padding: 0;
            background: transparent;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.65rem;
            color: #17212b;
        }

        .hero {
            display: grid;
            grid-template-columns: 54px 1fr auto;
            gap: 16px;
            align-items: center;
            padding: 20px;
            border: 1px solid rgba(23, 33, 43, 0.08);
            border-radius: 10px;
            background: linear-gradient(135deg, #0f7c80 0%, #2c9b82 100%);
            color: white;
            box-shadow: 0 18px 40px rgba(23, 33, 43, 0.13);
            margin-bottom: 18px;
        }

        .mark {
            width: 52px;
            height: 52px;
            display: grid;
            place-items: center;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.16);
            border: 1px solid rgba(255, 255, 255, 0.22);
            font-size: 1.8rem;
            font-weight: 900;
        }

        .hero h1 {
            margin: 0;
            font-size: 2rem;
            line-height: 1.05;
            letter-spacing: 0;
        }

        .hero p {
            margin: 6px 0 0;
            color: rgba(255, 255, 255, 0.82);
        }

        .hero-pill {
            min-width: 112px;
            padding: 10px 12px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.14);
            text-align: center;
            font-weight: 800;
        }

        .panel,
        .section-card,
        .side-card {
            border: 1px solid rgba(23, 33, 43, 0.08);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.88);
            box-shadow: 0 10px 24px rgba(23, 33, 43, 0.07);
        }

        .panel {
            padding: 18px;
            margin: 14px 0;
        }

        .section-card {
            padding: 18px;
            margin: 14px 0;
        }

        .side-card {
            padding: 15px;
            margin-bottom: 12px;
        }

        .eyebrow {
            color: #075a5e;
            font-size: 0.76rem;
            font-weight: 850;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .lesson-title {
            margin: 4px 0 6px;
            font-size: 1.55rem;
            line-height: 1.15;
            color: #17212b;
            letter-spacing: 0;
        }

        .muted {
            color: #65717e;
            font-size: 0.92rem;
            line-height: 1.55;
        }

        .progress-outer {
            height: 9px;
            border-radius: 999px;
            overflow: hidden;
            background: #e3e8ea;
            margin: 13px 0 6px;
        }

        .progress-inner {
            height: 100%;
            border-radius: inherit;
            background: #f1b84b;
        }

        .chip-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 12px;
        }

        .chip {
            display: inline-flex;
            align-items: center;
            min-height: 30px;
            padding: 5px 10px;
            border-radius: 999px;
            background: #edf3f1;
            color: #075a5e;
            font-size: 0.86rem;
            font-weight: 750;
        }

        .formula {
            margin-top: 12px;
            padding: 13px 14px;
            border-radius: 8px;
            background: #12252a;
            color: #effbf7;
            font-family: Consolas, "SFMono-Regular", monospace;
            font-size: 0.95rem;
            line-height: 1.45;
        }

        .section-card h3 {
            margin: 0 0 8px;
            color: #17212b;
            font-size: 1.12rem;
            letter-spacing: 0;
        }

        .section-body {
            color: #2b3843;
            line-height: 1.65;
            margin: 0;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
        }

        .quiz-wrap {
            margin-top: 20px;
            padding-top: 8px;
            border-top: 1px solid rgba(23, 33, 43, 0.08);
        }

        .quiz-heading {
            display: flex;
            align-items: end;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 12px;
        }

        .stButton > button {
            min-height: 44px;
            border-radius: 8px;
            border: 0;
            background: #0f7c80;
            color: white;
            font-weight: 850;
        }

        .stButton > button:hover {
            border: 0;
            background: #075a5e;
            color: white;
        }

        div[role="radiogroup"] label {
            padding: 8px 10px;
            border: 1px solid #d9dedb;
            border-radius: 8px;
            background: #fbfaf6;
            margin-bottom: 6px;
        }

        @media (max-width: 760px) {
            .hero {
                grid-template-columns: 44px 1fr;
            }

            .hero-pill {
                grid-column: 1 / -1;
                text-align: left;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(data: dict[str, Any], selected_lesson: dict[str, Any], lesson_count: int) -> None:
    app = data.get("app", {})
    progress = int(selected_lesson.get("progress", 0))
    st.markdown(
        f"""
        <div class="hero">
            <div class="mark">R</div>
            <div>
                <h1>{clean(app.get("name", "RENDFORT Maths"))}</h1>
                <p>{clean(app.get("level", "Seconde C"))} - {lesson_count} lecons structurees</p>
            </div>
            <div class="hero-pill">{progress}%<br><span style="font-size:.76rem;font-weight:650;">lecon active</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_progress(lessons: list[dict[str, Any]]) -> None:
    completed = sum(1 for lesson in lessons if lesson.get("progress", 0) >= 80)
    active = sum(1 for lesson in lessons if 0 < lesson.get("progress", 0) < 80)
    average = round(sum(int(lesson.get("progress", 0)) for lesson in lessons) / max(len(lessons), 1))

    col1, col2, col3 = st.columns(3)
    col1.metric("Lecons", len(lessons))
    col2.metric("En cours", active)
    col3.metric("Avancee moyenne", f"{average}%")
    st.caption(f"{completed} lecon terminee")


def render_lesson_intro(lesson: dict[str, Any]) -> None:
    progress = min(max(int(lesson.get("progress", 0)), 0), 100)
    chips = "".join(
        f'<span class="chip">{clean(objective)}</span>' for objective in lesson.get("objectives", [])
    )
    st.markdown(
        f"""
        <div class="panel">
            <div class="eyebrow">{clean(lesson.get("theme", "Theme"))}</div>
            <div class="lesson-title">{clean(lesson["title"])}</div>
            <div class="muted">{clean(lesson.get("competence", ""))} - {lesson_minutes(lesson)} min{clean(lesson_page_label(lesson))}</div>
            <div class="progress-outer"><div class="progress-inner" style="width:{progress}%"></div></div>
            <div class="muted">Progression locale : {progress}%</div>
            <div class="chip-grid">{chips}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(lessons: list[dict[str, Any]]) -> dict[str, Any]:
    st.sidebar.markdown("## Parcours")
    themes = ["Tous les themes"] + sorted({lesson.get("theme", "Autre") for lesson in lessons})
    selected_theme = st.sidebar.selectbox("Theme", themes)

    filtered_lessons = lessons
    if selected_theme != "Tous les themes":
        filtered_lessons = [lesson for lesson in lessons if lesson.get("theme") == selected_theme]

    selected_id = st.sidebar.selectbox(
        "Lecon",
        [lesson["id"] for lesson in filtered_lessons],
        format_func=lambda lesson_id: next(
            f"{lesson.get('order', 0):02d}. {lesson['title']}"
            for lesson in filtered_lessons
            if lesson["id"] == lesson_id
        ),
    )
    selected_lesson = next(lesson for lesson in filtered_lessons if lesson["id"] == selected_id)

    st.sidebar.markdown("---")
    st.sidebar.caption("Apercu de demonstration")
    st.sidebar.progress(min(max(int(selected_lesson.get("progress", 0)), 0), 100))
    return selected_lesson


def render_lesson(data: dict[str, Any], lesson: dict[str, Any]) -> None:
    render_lesson_intro(lesson)

    left, right = st.columns([2.2, 1])
    with left:
        for section in lesson.get("sections", []):
            formula = section.get("formula")
            formula_html = f'<div class="formula">{clean(formula)}</div>' if formula else ""
            st.markdown(
                f"""
                <div class="section-card">
                    <h3>{clean(section.get("title", "Section"))}</h3>
                    <div class="section-body">{clean(section.get("body", ""))}</div>
                    {formula_html}
                </div>
                """,
                unsafe_allow_html=True,
            )

        quiz = get_lesson_quiz(data, lesson)
        if quiz:
            render_quiz(quiz)

    with right:
        abilities = lesson.get("abilities", [])
        ability_items = "".join(f"<li>{clean(ability)}</li>" for ability in abilities)
        st.markdown(
            f"""
            <div class="side-card">
                <div class="eyebrow">Capacites</div>
                <ul class="muted" style="padding-left:18px;margin-bottom:0;">{ability_items}</ul>
            </div>
            <div class="side-card">
                <div class="eyebrow">Methode de travail</div>
                <p class="muted">Lis la section, reformule l'idee principale, puis verifie avec le quiz.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_quiz(quiz: dict[str, Any]) -> None:
    st.markdown(
        f"""
        <div class="quiz-wrap">
            <div class="quiz-heading">
                <div>
                    <div class="eyebrow">Evaluation rapide</div>
                    <div class="lesson-title" style="font-size:1.3rem;">{clean(quiz.get("title", "Quiz"))}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    answers: dict[str, int] = {}
    for index, question in enumerate(quiz.get("questions", []), start=1):
        choices = question.get("choices", [])
        if not choices:
            continue
        with st.container(border=True):
            selected = st.radio(
                f"{index}. {question['prompt']}",
                options=list(range(len(choices))),
                format_func=lambda item, choices=choices: choices[item],
                key=f"{quiz['id']}:{question['id']}",
            )
        answers[question["id"]] = int(selected)

    if st.button("Corriger le quiz", type="primary", key=f"submit:{quiz['id']}"):
        score, corrections = score_quiz(quiz, answers)
        st.session_state[f"result:{quiz['id']}"] = {"score": score, "corrections": corrections}

    result = st.session_state.get(f"result:{quiz['id']}")
    if not result:
        return

    st.success(f"Score : {result['score']}/20")
    for correction in result["corrections"]:
        if correction["is_correct"]:
            st.write(f"Correct - {correction['prompt']}")
        else:
            expected = correction["choices"][correction["expected"]]
            st.write(f"A revoir - {correction['prompt']}")
            st.caption(f"Bonne reponse : {expected}")
        if correction["explanation"]:
            st.caption(correction["explanation"])


def main() -> None:
    st.set_page_config(page_title="RENDFORT Maths", page_icon="R", layout="wide")
    inject_theme()

    data = load_content(DATA_PATH.stat().st_mtime)
    lessons = sorted(data.get("lessons", []), key=lambda item: item.get("order", 0))

    if not lessons:
        st.warning("Aucune lecon disponible pour le moment.")
        return

    selected_lesson = render_sidebar(lessons)
    render_header(data, selected_lesson, len(lessons))
    render_progress(lessons)
    render_lesson(data, selected_lesson)


if __name__ == "__main__":
    main()
