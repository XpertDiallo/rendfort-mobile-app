from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st


DATA_PATH = Path("content/generated/seed/rendfort_content.json")


@st.cache_data
def load_content() -> dict[str, Any]:
    if not DATA_PATH.exists():
        st.error("Le fichier de contenu est introuvable.")
        st.stop()
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


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


def render_progress(lessons: list[dict[str, Any]]) -> None:
    completed = sum(1 for lesson in lessons if lesson.get("progress", 0) >= 80)
    active = sum(1 for lesson in lessons if 0 < lesson.get("progress", 0) < 80)
    total = len(lessons)

    col1, col2, col3 = st.columns(3)
    col1.metric("Lecons", total)
    col2.metric("En cours", active)
    col3.metric("Avancees", completed)


def render_lesson(data: dict[str, Any], lesson: dict[str, Any]) -> None:
    st.subheader(lesson["title"])
    st.caption(f"{lesson.get('theme', 'Theme')} - {lesson.get('competence', 'Competence')}")

    progress = int(lesson.get("progress", 0))
    st.progress(min(max(progress, 0), 100), text=f"Progression locale : {progress}%")

    with st.expander("Objectifs", expanded=True):
        for objective in lesson.get("objectives", []):
            st.write(f"- {objective}")

    abilities = lesson.get("abilities", [])
    if abilities:
        with st.expander("Ce que tu dois savoir faire", expanded=True):
            for ability in abilities:
                st.write(f"- {ability}")

    for section in lesson.get("sections", []):
        st.markdown(f"### {section.get('title', 'Section')}")
        st.write(section.get("body", ""))
        formula = section.get("formula")
        if formula:
            st.code(formula, language="text")

    quiz = get_lesson_quiz(data, lesson)
    if quiz:
        render_quiz(quiz)


def render_quiz(quiz: dict[str, Any]) -> None:
    st.divider()
    st.subheader(quiz.get("title", "Quiz"))

    answers: dict[str, int] = {}
    for index, question in enumerate(quiz.get("questions", []), start=1):
        choices = question.get("choices", [])
        if not choices:
            continue
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
            st.write(f"OK - {correction['prompt']}")
        else:
            expected = correction["choices"][correction["expected"]]
            st.write(f"A revoir - {correction['prompt']}")
            st.caption(f"Bonne reponse : {expected}")
        if correction["explanation"]:
            st.caption(correction["explanation"])


def main() -> None:
    st.set_page_config(page_title="RENDFORT Maths", page_icon="R", layout="wide")
    data = load_content()
    lessons = sorted(data.get("lessons", []), key=lambda item: item.get("order", 0))

    st.title(data.get("app", {}).get("name", "RENDFORT Maths"))
    st.caption(data.get("app", {}).get("level", "Seconde C"))

    if not lessons:
        st.warning("Aucune lecon disponible pour le moment.")
        return

    render_progress(lessons)

    st.sidebar.title("Parcours")
    themes = ["Tous les themes"] + sorted({lesson.get("theme", "Autre") for lesson in lessons})
    selected_theme = st.sidebar.selectbox("Theme", themes)

    filtered_lessons = lessons
    if selected_theme != "Tous les themes":
        filtered_lessons = [lesson for lesson in lessons if lesson.get("theme") == selected_theme]

    selected_title = st.sidebar.radio(
        "Lecon",
        [lesson["title"] for lesson in filtered_lessons],
        index=0,
    )
    selected_lesson = next(lesson for lesson in filtered_lessons if lesson["title"] == selected_title)

    render_lesson(data, selected_lesson)


if __name__ == "__main__":
    main()
