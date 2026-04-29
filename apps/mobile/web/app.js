const api = {
  async get(path) {
    const res = await fetch(`/api/v1${path}`);
    if (!res.ok) throw new Error(`Erreur ${res.status}`);
    return res.json();
  },
  async post(path, body) {
    const res = await fetch(`/api/v1${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`Erreur ${res.status}`);
    return res.json();
  },
};

const state = {
  user: JSON.parse(localStorage.getItem("rendfort:user") || "null"),
  view: localStorage.getItem("rendfort:view") || "dashboard",
  dashboard: null,
  syllabus: null,
  lessons: [],
  activeLesson: null,
  activeQuiz: null,
  quizAnswers: {},
  quizResult: null,
  tutorOpen: false,
  tutorAnswer: "",
  tutorLoading: false,
  toast: "",
};

const app = document.querySelector("#app");
const BRAND_NAME = "RENDFORT Maths";
const TUTOR_NAME = "Tuteur RENDFORT";

function esc(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function icon(name) {
  const icons = {
    home: "⌂",
    book: "▤",
    mic: "◉",
    settings: "⚙",
    back: "‹",
    check: "✓",
    play: "▶",
    lock: "●",
  };
  return icons[name] || "•";
}

function setView(view) {
  state.view = view;
  localStorage.setItem("rendfort:view", view);
  render();
}

function toast(message) {
  state.toast = message;
  render();
  setTimeout(() => {
    state.toast = "";
    render();
  }, 2600);
}

async function loadInitial() {
  if (!state.user) {
    render();
    return;
  }
  try {
    const [dashboard, syllabus, lessons] = await Promise.all([
      api.get("/dashboard"),
      api.get("/syllabus"),
      api.get("/lessons"),
    ]);
    state.dashboard = dashboard;
    state.syllabus = syllabus;
    state.lessons = lessons.items;
  } catch (error) {
    toast("Connexion locale indisponible.");
  }
  render();
}

async function login(event) {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const firstName = form.get("first_name") || "Kouadio";
  const email = form.get("email") || "demo@rendfort.local";
  try {
    const data = await api.post("/auth/login", { first_name: firstName, email });
    state.user = data.user;
    localStorage.setItem("rendfort:user", JSON.stringify(data.user));
    state.view = "dashboard";
    await loadInitial();
  } catch (error) {
    toast("Connexion impossible pour le moment.");
  }
}

function logout() {
  localStorage.removeItem("rendfort:user");
  state.user = null;
  state.dashboard = null;
  state.view = "dashboard";
  render();
}

async function openLesson(id) {
  try {
    state.activeLesson = await api.get(`/lessons/${id}`);
    state.view = "lesson";
    render();
  } catch (error) {
    toast("Leçon introuvable.");
  }
}

async function openQuiz(quizId) {
  try {
    state.activeQuiz = await api.get(`/quizzes/${quizId}`);
    state.quizAnswers = {};
    state.quizResult = null;
    state.view = "quiz";
    render();
  } catch (error) {
    toast("Quiz introuvable.");
  }
}

async function submitQuiz() {
  if (!state.activeQuiz) return;
  try {
    state.quizResult = await api.post(`/quizzes/${state.activeQuiz.id}/attempts`, {
      answers: state.quizAnswers,
    });
    await loadInitial();
    state.view = "quiz";
    render();
  } catch (error) {
    toast("Correction indisponible.");
  }
}

async function askTutor(event) {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const question = String(form.get("question") || "").trim();
  if (!question) return;
  state.tutorLoading = true;
  state.tutorAnswer = "";
  render();
  try {
    const data = await api.post("/tutor/question", {
      lesson_id: state.activeLesson?.id,
      section_id: state.activeLesson?.sections?.[0]?.id,
      question,
    });
    state.tutorAnswer = data.answer;
  } catch (error) {
    state.tutorAnswer = "Le tuteur est indisponible. Reprends la leçon et réessaie dans un instant.";
  }
  state.tutorLoading = false;
  render();
}

function renderAuth() {
  return `
    <div class="screen auth">
      <div class="brand">
        <div class="brand-mark">R</div>
        <div>
          <div class="brand-title">${BRAND_NAME}</div>
          <div class="brand-subtitle">Seconde C</div>
        </div>
      </div>
      <div class="auth-panel">
        <div class="title-row">
          <div class="eyebrow">Connexion</div>
          <h2>Prêt pour ton renforcement ?</h2>
        </div>
        <form onsubmit="login(event)">
          <div class="field">
            <label>Prénom</label>
            <input name="first_name" autocomplete="given-name" placeholder="Kouadio" />
          </div>
          <div class="field">
            <label>Email</label>
            <input name="email" type="email" autocomplete="email" placeholder="demo@rendfort.local" />
          </div>
          <div class="field">
            <label>Mot de passe</label>
            <input name="password" type="password" autocomplete="current-password" placeholder="••••••••" />
          </div>
          <button class="primary" type="submit">${icon("play")} Entrer</button>
        </form>
        <button class="text-button" onclick="toast('La validation email sera branchée au service de messagerie.')">Créer un compte</button>
      </div>
    </div>
  `;
}

function renderTopbar(title = BRAND_NAME, subtitle = "Seconde C") {
  return `
    <div class="topbar">
      <div class="brand">
        <div class="brand-mark">R</div>
        <div>
          <div class="brand-title">${esc(title)}</div>
          <div class="brand-subtitle">${esc(subtitle)}</div>
        </div>
      </div>
      <button class="icon-button" onclick="logout()" title="Déconnexion">${icon("settings")}</button>
    </div>
  `;
}

function renderDashboard() {
  const data = state.dashboard;
  if (!data) return `<div class="screen">${renderTopbar()}<div class="card">Chargement...</div></div>`;
  const user = state.user || data.user;
  const resume = data.resume_lesson;
  return `
    <div class="screen">
      ${renderTopbar("Salut " + user.first_name, "RENDFORT du jour")}
      <div class="hero-card card">
        <div class="eyebrow">Reprendre l'étude</div>
        <h2>${esc(resume.title)}</h2>
        <p>${esc(resume.theme)} • ${esc(resume.duration)} min</p>
        <div class="progress-track"><div class="progress-fill" style="width:${resume.progress}%"></div></div>
        <p>${resume.progress}% terminé</p>
        <button class="secondary" onclick="openLesson('${resume.id}')">${icon("play")} Continuer</button>
      </div>
      <div class="stats">
        <div class="stat"><div class="stat-value">${data.stats.study_time}</div><div class="stat-label">Cette semaine</div></div>
        <div class="stat"><div class="stat-value">${data.stats.mastery}%</div><div class="stat-label">Maîtrise</div></div>
        <div class="stat"><div class="stat-value">${data.stats.average_score}/20</div><div class="stat-label">Moyenne quiz</div></div>
      </div>
      <div class="card">
        <h3>Ce que tu sais faire maintenant</h3>
        <ul class="ability-list">
          ${data.abilities.map((item) => `<li><span class="check">${icon("check")}</span><span>${esc(item)}</span></li>`).join("")}
        </ul>
      </div>
      <div class="card">
        <h3>Mes derniers défis</h3>
        ${data.recent_quizzes.map((quiz) => `
          <div class="quiz-row">
            <div><strong>${esc(quiz.title)}</strong><div class="brand-subtitle">${esc(quiz.created_at)}</div></div>
            <div class="score">${quiz.score}/20</div>
          </div>
        `).join("")}
      </div>
      <div class="card">
        <h3>Points à renforcer</h3>
        <ul class="weak-list">
          ${data.weak_points.map((item) => `<li><span class="check">!</span><span><strong>${esc(item.title)}</strong><br><span class="brand-subtitle">${esc(item.hint)}</span></span></li>`).join("")}
        </ul>
      </div>
    </div>
  `;
}

function renderProgram() {
  const lessons = state.lessons || [];
  return `
    <div class="screen">
      ${renderTopbar("Mon programme", "Leçons faites et à faire")}
      ${lessons.map((lesson) => `
        <button class="lesson-card" onclick="openLesson('${lesson.id}')">
          <div class="lesson-meta">
            <span class="pill">${esc(lesson.theme)}</span>
            <span class="pill">${esc(lesson.duration)} min</span>
          </div>
          <h3>${esc(lesson.order)}. ${esc(lesson.title)}</h3>
          <div class="progress-track"><div class="progress-fill" style="width:${lesson.progress}%"></div></div>
          <div class="brand-subtitle">${esc(lesson.progress)}% terminé • ${esc(lesson.difficulty)}</div>
        </button>
      `).join("")}
    </div>
  `;
}

function renderLesson() {
  const lesson = state.activeLesson;
  if (!lesson) return renderProgram();
  return `
    <div class="screen">
      <div class="topbar">
        <button class="back-button" onclick="setView('program')">${icon("back")} Programme</button>
        <button class="icon-button" onclick="openQuiz('${lesson.quiz_id}')" title="Quiz">20</button>
      </div>
      <div class="title-row">
        <div class="eyebrow">${esc(lesson.theme)}</div>
        <h2>${esc(lesson.title)}</h2>
      </div>
      <div class="card">
        <h3>Objectifs</h3>
        <ul class="objective-list">${lesson.objectives.map((item) => `<li>${esc(item)}</li>`).join("")}</ul>
      </div>
      ${lesson.sections.map((section) => `
        <section class="section">
          <h3>${esc(section.title)}</h3>
          <p>${esc(section.body)}</p>
          ${section.formula ? `<div class="formula">${esc(section.formula)}</div>` : ""}
        </section>
      `).join("")}
      <div class="floating-actions">
        <button class="question-button" onclick="state.tutorOpen = true; render()">Question ?</button>
        <button class="primary" onclick="openQuiz('${lesson.quiz_id}')">Faire le quiz</button>
      </div>
      ${state.tutorOpen ? renderTutorModal() : ""}
    </div>
  `;
}

function renderTutorModal() {
  return `
    <div class="modal">
      <div class="tutor-panel">
        <div class="topbar">
          <div>
            <div class="eyebrow">${TUTOR_NAME}</div>
            <h3>Dis-moi ce qui bloque</h3>
          </div>
          <button class="icon-button" onclick="state.tutorOpen=false; state.tutorAnswer=''; render()">×</button>
        </div>
        <form onsubmit="askTutor(event)">
          <div class="field">
            <label>Ta question</label>
            <textarea name="question" placeholder="Exemple : pourquoi la valeur absolue donne une distance ?"></textarea>
          </div>
          <button class="primary" type="submit">${state.tutorLoading ? "Réflexion..." : "Demander"}</button>
        </form>
        ${state.tutorAnswer ? `<div class="answer">${esc(state.tutorAnswer)}</div>` : ""}
      </div>
    </div>
  `;
}

function renderQuiz() {
  const quiz = state.activeQuiz;
  if (!quiz) return renderProgram();
  if (state.quizResult) {
    return `
      <div class="screen">
        <button class="back-button" onclick="setView('dashboard')">${icon("back")} Accueil</button>
        <div class="title-row">
          <div class="eyebrow">Résultat</div>
          <h2>${esc(state.quizResult.score)}/20</h2>
        </div>
        ${state.quizResult.corrections.map((item, index) => `
          <div class="quiz-card">
            <strong>Question ${index + 1}</strong>
            <p>${item.correct ? "Bonne réponse." : "À revoir."}</p>
            <p class="brand-subtitle">${esc(item.explanation)}</p>
          </div>
        `).join("")}
        <button class="primary" onclick="setView('dashboard')">Retour au tableau de bord</button>
      </div>
    `;
  }
  return `
    <div class="screen">
      <button class="back-button" onclick="setView('lesson')">${icon("back")} Leçon</button>
      <div class="title-row">
        <div class="eyebrow">Défi</div>
        <h2>${esc(quiz.title)}</h2>
      </div>
      ${quiz.questions.map((question, qIndex) => `
        <div class="quiz-card">
          <h3>${qIndex + 1}. ${esc(question.prompt)}</h3>
          <div class="choices">
            ${question.choices.map((choice, index) => `
              <button class="choice ${state.quizAnswers[question.id] === index ? "selected" : ""}" onclick="state.quizAnswers['${question.id}']=${index}; render()">
                <span class="dot"></span>
                <span>${esc(choice)}</span>
              </button>
            `).join("")}
          </div>
        </div>
      `).join("")}
      <button class="primary" onclick="submitQuiz()">Corriger</button>
    </div>
  `;
}

function renderSettings() {
  return `
    <div class="screen">
      ${renderTopbar("Réglages", "Compte et préférences")}
      <div class="card">
        <h3>Préférences</h3>
        <p class="brand-subtitle">Voix native du téléphone prévue pour le français. Le mode texte reste prioritaire dans cette V1.</p>
      </div>
      <button class="danger-soft" onclick="logout()">Se déconnecter</button>
    </div>
  `;
}

function renderNav() {
  if (!state.user) return "";
  const items = [
    ["dashboard", "Accueil", "home"],
    ["program", "Cours", "book"],
    ["lesson", "Tuteur", "mic"],
    ["settings", "Réglages", "settings"],
  ];
  return `
    <nav class="bottom-nav">
      ${items.map(([view, label, iconName]) => `
        <button class="nav-item ${state.view === view ? "active" : ""}" onclick="${view === "lesson" && state.activeLesson ? "setView('lesson')" : `setView('${view === "lesson" ? "program" : view}')`}">
          <span>${icon(iconName)}</span>
          <span>${label}</span>
        </button>
      `).join("")}
    </nav>
  `;
}

function renderPhone() {
  if (!state.user) return `<div class="phone">${renderAuth()}</div>`;
  const views = {
    dashboard: renderDashboard,
    program: renderProgram,
    lesson: renderLesson,
    quiz: renderQuiz,
    settings: renderSettings,
  };
  return `<div class="phone">${(views[state.view] || renderDashboard)()}${renderNav()}</div>`;
}

function renderDesktopPanel() {
  return `
    <aside class="desktop-panel">
      <div class="eyebrow">Parcours Seconde C</div>
      <h1>${BRAND_NAME}</h1>
      <p>Un parcours progressif de 14 leçons pour consolider les bases, reprendre les méthodes et vérifier chaque notion avec un score sur 20.</p>
      <div class="desktop-grid">
        <div class="desktop-note"><strong>Séquence actuelle</strong><span>Vecteurs et points du plan, puis nombres réels.</span></div>
        <div class="desktop-note"><strong>Objectif du jour</strong><span>Identifier les données, choisir la méthode et justifier.</span></div>
        <div class="desktop-note"><strong>Défi rapide</strong><span>Trois questions corrigées après chaque leçon.</span></div>
        <div class="desktop-note"><strong>À renforcer</strong><span>Valeur absolue, fonctions, transformations et trigonométrie.</span></div>
      </div>
    </aside>
  `;
}

function render() {
  app.innerHTML = `
    <main class="shell">
      ${renderPhone()}
      ${renderDesktopPanel()}
    </main>
    ${state.toast ? `<div class="toast">${esc(state.toast)}</div>` : ""}
  `;
}

window.login = login;
window.logout = logout;
window.setView = setView;
window.openLesson = openLesson;
window.openQuiz = openQuiz;
window.submitQuiz = submitQuiz;
window.askTutor = askTutor;
window.toast = toast;
window.state = state;

render();
loadInitial();
