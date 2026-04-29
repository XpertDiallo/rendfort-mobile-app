# RENDFORT Maths App - MVP V1

RENDFORT Maths App est une application mobile de renforcement en mathematiques pour la classe de Seconde C. Le produit vise a jouer le role d'un professeur particulier dans la poche de l'eleve : expliquer les lecons du programme, donner des exemples concrets, permettre de poser une question au bon moment, suivre la progression et aider l'eleve a identifier ses lacunes.

Ce depot contient le squelette technique du MVP V1. Il n'est pas encore une application executable complete. Il sert de base de travail pour structurer le mobile, le backend, le pipeline de contenu, les donnees pedagogiques et les futures briques d'assistance.

## 1. Vision Produit

### Objectif principal

Construire une premiere version utilisable de RENDFORT qui permet a un eleve de Seconde C de :

- creer un compte et retrouver sa progression ;
- acceder au programme officiel de mathematiques Seconde C ;
- suivre des lecons structurees avec objectifs, explications, exemples et quiz ;
- interrompre une lecon pour poser une question contextualisee au tuteur RENDFORT ;
- consulter son tableau de bord : competences acquises, quiz passes, scores, lecons faites et lecons a faire ;
- utiliser les contenus essentiels hors ligne, sans assistance interactive lorsque la connexion est absente.

### Positionnement

RENDFORT n'est pas un chatbot generaliste. C'est un tuteur specialise, aligne sur le programme educatif officiel de Mathematiques Seconde C, avec une experience pedagogique guidee.

Le produit doit privilegier :

- la progression pas a pas ;
- la clarte des objectifs ;
- les exemples issus de la vie courante ;
- la correction des erreurs et lacunes ;
- la maitrise des couts d'assistance ;
- la fiabilite pedagogique.

## 2. Sources Pedagogiques

Les documents de reference identifies pour le MVP sont :

- `06.Prog Educt maths 2C CND 0923.pdf`
  - Programme officiel.
  - PDF texte directement exploitable.
  - Source maitresse pour l'arborescence pedagogique.

- `cours maths apc 2nde C ecole-online ci.pdf`
  - Cours adopte pour construire les lecons et les quiz RENDFORT.
  - PDF texte majoritairement extractible.
  - Source principale pour le parcours pedagogique MVP.

- Supports autorises de reference interne
  - Utilisables pour l'analyse, les illustrations et les recoupements pedagogiques.
  - Ne doivent pas etre cites par leur nom dans l'application.

### Regle importante

Le programme officiel doit rester la source d'autorite pour le MVP.

Les autorisations d'utilisation des supports de reference sont considerees comme obtenues. Ils peuvent donc alimenter le travail pedagogique du projet selon les termes accordes. Dans l'application, ne jamais afficher les noms internes des sources : utiliser des formulations neutres comme "support de cours", "manuel de reference" ou "guide pedagogique".

### Regle de vocabulaire dans l'application

Certains termes techniques ou noms de sources internes ne doivent jamais apparaitre dans l'application mobile, dans les textes visibles par l'utilisateur, dans les notifications, dans les emails transactionnels, dans les messages d'erreur ni dans les contenus pedagogiques publies.

Lexique utilisateur recommande :

- `tuteur RENDFORT`
- `prof RENDFORT`
- `assistant RENDFORT`
- `Micro-RENDFORT`
- `support de cours`
- `manuel de reference`
- `guide pedagogique`
- `assistance interactive`

Cette regle concerne l'experience utilisateur. Les documents techniques internes peuvent decrire les briques sous-jacentes, mais aucun libelle technique ne doit remonter dans l'interface.

## 3. Perimetre MVP V1

### Inclus en V1

1. Authentification
   - Inscription avec nom, prenoms, email et mot de passe.
   - Verification email.
   - Connexion par email et mot de passe.
   - Session persistante avec refresh token.

2. Onboarding pedagogique
   - Questionnaire initial.
   - Niveau ressenti.
   - Objectif de l'eleve.
   - Points noirs declares.
   - Diagnostic court sous forme de QCM.

3. Programme Seconde C
   - Liste des competences.
   - Themes.
   - Lecons.
   - Objectifs pedagogiques.
   - Prerequis.
   - Capacites attendues.

4. Lecteur de lecon
   - Introduction de la lecon.
   - Objectifs avant demarrage.
   - Explication decoupee en sections courtes.
   - Exemples concrets.
   - Formules affichees proprement.
   - Progression de lecture.
   - Bouton `Question ?`.

5. Tuteur RENDFORT contextualise
   - Question texte en V1.
   - Voix optionnelle simple si budget et delai le permettent.
   - Reponse basee sur la lecon en cours, le niveau de l'eleve et le point exact d'interruption.
   - Le tuteur explique, donne un indice ou reformule, mais ne doit pas encourager la triche.

6. Quiz
   - Quiz par lecon.
   - Score sur 20.
   - Correction immediate.
   - Explication des erreurs.
   - Recommandation de revision.

7. Dashboard
   - Resume de progression.
   - Bloc "Ce que tu es capable de faire maintenant".
   - Derniers quiz avec score sur 20.
   - Acces au programme : lecons faites et a faire.
   - Points a renforcer.

8. Mode hors ligne
   - Consultation des lecons deja synchronisees.
   - Lecture des contenus texte.
   - Acces aux quiz locaux si deja telecharges.
   - Desactivation de l'assistance interactive sans connexion.

9. Back-office minimal par fichiers
   - Les contenus pedagogiques du MVP peuvent d'abord etre versionnes en fichiers Markdown, JSON ou YAML.
   - Une interface admin complete n'est pas requise en V1.

### Exclus de la V1

Ces fonctionnalites sont importantes, mais doivent etre repoussees :

- scan manuscrit d'exercices ;
- resolution automatique complete d'exercices photographies ;
- vocal illimite ;
- social learning ou clubs de revision ;
- espace parents/professeurs complet ;
- paiement integre ;
- OCR automatique complet dans l'application mobile ;
- calcul de volume d'objets reels depuis une photo ;
- generation automatique non validee de tout le programme.

## 4. Arborescence du Projet

```text
.
|-- apps/
|   `-- mobile/
|       |-- assets/
|       |   |-- audio/
|       |   |-- fonts/
|       |   `-- images/
|       |-- lib/
|       |   |-- app/
|       |   |-- core/
|       |   |   |-- config/
|       |   |   |-- network/
|       |   |   `-- storage/
|       |   |-- features/
|       |   |   |-- assistant/
|       |   |   |-- auth/
|       |   |   |-- dashboard/
|       |   |   |-- lesson_player/
|       |   |   |-- onboarding/
|       |   |   |-- quiz/
|       |   |   |-- settings/
|       |   |   `-- syllabus/
|       |   `-- shared/
|       |       |-- theme/
|       |       `-- widgets/
|       `-- test/
|-- services/
|   `-- api/
|       |-- app/
|       |   |-- api/
|       |   |   `-- v1/
|       |   |-- core/
|       |   |-- models/
|       |   |-- repositories/
|       |   |-- schemas/
|       |   |-- services/
|       |   |   |-- tutor/
|       |   |   |-- auth/
|       |   |   |-- content/
|       |   |   |-- progress/
|       |   |   `-- quiz/
|       |   `-- workers/
|       `-- tests/
|-- content/
|   |-- programme_2c/
|   |   |-- official/
|   |   |-- lessons/
|   |   `-- quizzes/
|   |-- sources_autorisees/
|   |   |-- raw/
|   |   |-- ocr/
|   |   |-- cleaned/
|   |   `-- mapping/
|   `-- generated/
|       |-- fixtures/
|       `-- seed/
|-- tools/
|   `-- content_pipeline/
|       |-- extractors/
|       |-- ocr/
|       `-- validators/
|-- docs/
|   |-- legal/
|   |-- pedagogy/
|   |-- product/
|   `-- technical/
|-- infra/
|   |-- db/
|   |   `-- migrations/
|   `-- docker/
`-- scripts/
```

## 5. Responsabilites des Dossiers

### `apps/mobile`

Application mobile Flutter.

Responsibilities :

- interface eleve ;
- navigation ;
- lecture de lecons ;
- quiz ;
- dashboard ;
- stockage local ;
- synchronisation ;
- mode hors ligne ;
- capture audio eventuelle ;
- affichage des formules mathematiques.

### `services/api`

Backend applicatif, recommande en Python FastAPI.

Responsibilities :

- authentification ;
- gestion utilisateur ;
- progression ;
- contenus pedagogiques ;
- quiz ;
- tuteur RENDFORT ;
- journalisation des interactions utiles ;
- securite et quotas ;
- synchronisation avec le mobile.

### `content`

Source de verite pedagogique versionnee.

Responsibilities :

- programme officiel structure ;
- lecons originales ;
- quiz ;
- mapping entre programme officiel et supports autorises ;
- contenus nettoyes issus d'OCR ;
- jeux de donnees de seed pour initialiser la base.

### `tools/content_pipeline`

Outils internes pour transformer les PDF et supports bruts en contenus exploitables.

Responsibilities :

- extraction du programme officiel ;
- OCR des scans ;
- nettoyage ;
- decoupage par chapitre ;
- detection des formules ;
- conversion vers Markdown/JSON ;
- validation de schema ;
- generation de fixtures.

### `docs`

Documentation projet.

Responsibilities :

- decisions produit ;
- decisions techniques ;
- notes legales ;
- notes pedagogiques ;
- cahier de tests ;
- specifications d'ecrans.

### `infra`

Infrastructure de developpement et de deploiement.

Responsibilities :

- Docker ;
- migrations SQL ;
- configuration base de donnees ;
- eventuels fichiers de deploiement.

## 6. Stack Technique Recommandee

### Mobile

- Flutter.
- Dart.
- Gestion d'etat : Riverpod ou Bloc.
- Stockage local : SQLite, Drift ou Hive.
- Formules : rendu LaTeX via package Flutter adapte.
- Audio V1 optionnel : speech-to-text natif ou API selon budget.

### Backend

- Python 3.11 ou plus.
- FastAPI.
- PostgreSQL.
- `pgvector` pour la recherche vectorielle interne.
- SQLAlchemy ou SQLModel.
- Alembic pour les migrations.
- Redis optionnel pour cache et jobs.

### Moteur d'assistance

Pour le MVP, privilegier une architecture API first :

- LLM via API externe pour limiter la complexite initiale ;
- embeddings pour recherche dans contenus pedagogiques ;
- RAG restreint au programme et aux lecons validees ;
- prompts controles ;
- logs d'evaluation pedagogique.

Le passage vers des modeles open source auto-heberges peut etre etudie plus tard pour reduire les couts.

## 7. Modules Fonctionnels

### 7.1 Authentification

Flux d'inscription :

1. L'utilisateur saisit nom, prenoms, email, mot de passe.
2. Le backend cree un compte non verifie.
3. Un email de verification est envoye.
4. L'utilisateur clique sur le lien ou saisit un code.
5. Le compte devient actif.
6. L'utilisateur complete son onboarding pedagogique.

Connexion :

- identifiant recommande : email ;
- mot de passe ;
- refresh token securise ;
- option future : biometrie cote mobile.

Note : la connexion par nom seul est deconseillee, car les doublons sont inevitables.

### 7.2 Onboarding

Questions minimales :

- classe : Seconde C ;
- objectif : remise a niveau, prochain controle, excellence, examen ;
- aisance en mathematiques : 1 a 5 ;
- points noirs : calcul litteral, fonctions, geometrie, statistiques, vecteurs ;
- disponibilite hebdomadaire ;
- preference : explication courte, detaillee ou progressive.

Sortie attendue :

- profil pedagogique ;
- niveau de depart ;
- premieres lecons recommandees.

### 7.3 Programme et Syllabus

Le MVP doit structurer le programme en :

- competence ;
- theme ;
- lecon ;
- objectifs ;
- prerequis ;
- contenus ;
- competences attendues ;
- limites du programme ;
- quiz associes.

Exemple de domaines couverts d'apres le programme :

- calculs algebriques ;
- fonctions ;
- statistiques a une variable ;
- geometrie du plan ;
- geometrie de l'espace ;
- transformations du plan ;
- arithmetique, si retenue dans le referentiel final.

### 7.4 Lecteur de Lecon

Chaque lecon doit contenir :

- titre ;
- situation d'apprentissage ;
- objectifs ;
- prerequis ;
- explication principale ;
- exemples concrets ;
- mini-exercices ;
- recapitulatif ;
- quiz final ;
- ressources hors ligne.

Le lecteur doit :

- sauvegarder la progression ;
- permettre de reprendre la ou l'eleve s'est arrete ;
- afficher les formules proprement ;
- proposer le bouton `Question ?` a tout moment.

### 7.5 Tuteur RENDFORT `Question ?`

Comportement attendu :

- stopper la lecture ou l'audio en cours ;
- capturer le contexte exact : lecon, section, timestamp, formule ou paragraphe ;
- permettre une question texte ;
- repondre en tenant compte du niveau de l'eleve ;
- proposer une reformulation, un exemple ou un indice ;
- offrir un bouton `On continue ?`.

Le tuteur doit eviter :

- de donner une solution brute a un devoir scanne ;
- d'inventer un contenu non present dans le programme ;
- de sortir du niveau Seconde C sans l'indiquer ;
- de valider une reponse douteuse sans verification.

### 7.6 Quiz

Types de questions V1 :

- QCM ;
- vrai/faux ;
- reponse numerique courte ;
- appariement simple ;
- question a etapes guidees, si simple a implementer.

Sortie attendue :

- score sur 20 ;
- correction ;
- notion maitrisee ou fragile ;
- recommandation de revision ;
- mise a jour des competences acquises.

### 7.7 Dashboard

Blocs obligatoires :

1. Header
   - prenom ;
   - niveau ;
   - serie de jours ou progression simple.

2. Reprendre l'etude
   - derniere lecon ;
   - progression ;
   - bouton reprendre.

3. Ce que tu es capable de faire maintenant
   - competences acquises formulees en langage eleve.
   - exemple : "Tu sais resoudre une equation avec valeur absolue simple."

4. Mon programme
   - lecons faites ;
   - lecons a faire ;
   - lecons recommandees.

5. Mes derniers quiz
   - titre ;
   - score sur 20 ;
   - date ;
   - bouton revoir.

6. Points a renforcer
   - notions faibles ;
   - proposition de mini-revision.

## 8. Mode Hors Ligne

Le mode hors ligne est un avantage important du MVP.

Disponible hors ligne :

- liste des lecons deja synchronisees ;
- texte des lecons ;
- formules ;
- quiz deja telecharges ;
- scores locaux non synchronises ;
- lecture audio locale eventuelle si generee a l'avance.

Non disponible hors ligne :

- tuteur RENDFORT ;
- analyse de nouveaux documents ;
- OCR ;
- synchronisation multi-appareils ;
- generation dynamique de nouvelles explications.

Regle d'interface :

- si l'app est hors ligne, le bouton `Question ?` doit afficher clairement que l'assistance interactive necessite Internet ;
- l'app doit proposer de continuer la lecon sans assistance interactive.

## 9. Pipeline de Contenu

### 9.1 Programme officiel

Le programme officiel etant extractible, il peut etre transforme en donnees structurees.

Format cible conseille :

```yaml
id: lecon-nombres-reels
level: seconde_c
competence: calculs_algebriques_et_fonctions
theme: calculs_algebriques
title: Ensemble des nombres reels
objectives:
  - Connaitre la valeur absolue d'un nombre reel
  - Resoudre une equation du type |x - a| = r
prerequisites:
  - Nombres rationnels
  - Ordre dans R
sections:
  - id: introduction
    title: Situation d'apprentissage
    type: explanation
  - id: cours
    title: Cours
    type: lesson
  - id: exemples
    title: Exemples
    type: examples
quiz_id: quiz-nombres-reels-01
```

### 9.2 Supports de reference autorises

Les supports de reference autorises doivent passer par :

1. OCR.
2. Nettoyage.
3. Decoupage par chapitre.
4. Correction des formules.
5. Mapping avec le programme officiel.
6. Reecriture originale pour l'application.
7. Validation par un professeur.

Les scans ne doivent pas etre injectes tels quels dans l'application. Les contenus publies doivent etre nettoyes, structures et conformes au vocabulaire utilisateur RENDFORT.

### 9.3 Validation pedagogique

Chaque lecon doit etre validee selon :

- alignement programme ;
- absence de notion hors programme non signalee ;
- exactitude mathematique ;
- clarte des exemples ;
- progression de difficulte ;
- quiz coherent avec les objectifs.

## 10. Donnees et Modele Metier

Tables principales recommandees :

```text
users
profiles
email_verifications
refresh_tokens
competencies
themes
lessons
lesson_sections
lesson_assets
quizzes
quiz_questions
quiz_attempts
quiz_answers
student_progress
student_skills
assistant_interactions
content_embeddings
```

### `users`

- id
- email
- password_hash
- first_name
- last_name
- is_verified
- created_at
- updated_at
- last_login_at

### `profiles`

- id
- user_id
- level
- objective
- comfort_score
- declared_weaknesses
- preferred_explanation_style

### `lessons`

- id
- title
- slug
- competence_id
- theme_id
- order_index
- estimated_duration_minutes
- offline_available
- status : draft, reviewed, published

### `student_progress`

- id
- user_id
- lesson_id
- status : not_started, in_progress, completed
- progress_percent
- last_section_id
- last_position_seconds
- completed_at

### `assistant_interactions`

- id
- user_id
- lesson_id
- section_id
- question
- answer_summary
- detected_gap
- created_at

Ne pas stocker les audios par defaut. Stocker uniquement la transcription ou un resume si necessaire.

## 11. API MVP

Base URL locale :

```text
http://localhost:8000/api/v1
```

Endpoints proposes :

```text
POST   /auth/register
POST   /auth/verify-email
POST   /auth/login
POST   /auth/refresh
POST   /auth/logout

GET    /me
PATCH  /me/profile

GET    /syllabus
GET    /lessons
GET    /lessons/{lesson_id}
GET    /lessons/{lesson_id}/sections

POST   /progress/lessons/{lesson_id}
GET    /progress

GET    /quizzes/{quiz_id}
POST   /quizzes/{quiz_id}/attempts
GET    /quizzes/attempts/recent

POST   /assistant/question
GET    /dashboard

GET    /sync/offline-pack
POST   /sync/progress
```

### Exemple `POST /assistant/question`

Request :

```json
{
  "lesson_id": "lecon-nombres-reels",
  "section_id": "valeur-absolue-definition",
  "question": "Pourquoi |x - a| represente une distance ?",
  "student_context": {
    "level": "seconde_c",
    "comfort_score": 2,
    "last_quiz_score": 9
  }
}
```

Response :

```json
{
  "answer": "Pense a une droite graduee. La valeur |x - a| mesure l'ecart entre le point x et le point a, sans tenir compte du sens...",
  "suggested_action": "continue_lesson",
  "detected_gap": "valeur_absolue_comme_distance",
  "next_prompt": "Veux-tu un exemple avec deux nombres sur une droite graduee ?"
}
```

## 12. Strategie du Moteur d'Assistance

### Principe

Le moteur d'assistance du MVP doit etre encadre. Il ne doit pas improviser un cours entier sans reference.

Contexte minimal envoye au LLM :

- identifiant de la lecon ;
- extrait de la section en cours ;
- objectifs de la lecon ;
- niveau de l'eleve ;
- historique court des lacunes ;
- question de l'eleve.

### Modes de reponse

- `explain` : expliquer une notion.
- `rephrase` : reformuler plus simplement.
- `hint` : donner un indice.
- `example` : donner un exemple analogue.
- `check_understanding` : poser une mini-question.

### Garde-fous

Le prompt systeme doit imposer :

- niveau Seconde C ;
- rigueur mathematique ;
- pas de solution brute sans guidage ;
- signalement des incertitudes ;
- reponse courte par defaut ;
- exemples concrets ;
- pas de contenu hors programme sans mention.

### Verification mathematique

Pour le MVP, commencer avec :

- contenu pedagogique valide manuellement ;
- quiz avec corrections statiques ;
- tests unitaires sur corrections numeriques simples.

Pour V1.1 :

- integration SymPy pour verifier certaines expressions ;
- detecteur de reponses equivalentes ;
- banque de transformations algebriques autorisees.

## 13. UX MVP

### Ecrans prioritaires

1. Splash / verification de session.
2. Connexion.
3. Inscription.
4. Verification email.
5. Onboarding.
6. Dashboard.
7. Programme.
8. Detail lecon.
9. Lecteur de lecon.
10. Chat `Question ?`.
11. Quiz.
12. Resultat quiz.
13. Reglages.

### Style

L'application doit etre claire, dense mais respirable, adaptee a l'etude.

Recommandations :

- eviter les effets visuels trop marketing ;
- privilegier la lisibilite ;
- rendre les formules nettes ;
- mettre les actions principales au pouce ;
- afficher les scores et competences sans humilier l'eleve ;
- utiliser une tonalite encourageante mais precise.

## 14. Securite et Confidentialite

### Obligatoire V1

- hash des mots de passe avec Argon2 ou BCrypt ;
- JWT court terme ;
- refresh token revocable ;
- verification email ;
- rate limiting sur auth et assistant ;
- validation stricte des inputs ;
- pas de stockage audio par defaut ;
- logs sans donnees sensibles ;
- suppression possible du compte.

### Donnees sensibles

RENDFORT manipule :

- identite ;
- email ;
- progression scolaire ;
- difficultes de l'eleve ;
- questions posees au tuteur RENDFORT.

Ces donnees doivent etre traitees avec prudence, surtout si l'utilisateur est mineur.

## 15. Environnements

### Local

Objectif :

- developpement mobile ;
- backend local ;
- base locale ;
- donnees de seed ;
- tests.

### Staging

Objectif :

- validation interne ;
- tests avec quelques eleves ;
- observation des couts d'assistance ;
- correction pedagogique.

### Production

Objectif :

- usage reel ;
- monitoring ;
- quotas ;
- sauvegardes ;
- conformite.

## 16. Variables d'Environnement

Exemple :

```env
APP_ENV=local
APP_NAME=RENDFORT Maths Seconde C

DATABASE_URL=postgresql://RENDFORT:RENDFORT@localhost:5432/RENDFORT
REDIS_URL=redis://localhost:6379/0

JWT_SECRET=change-me
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30

EMAIL_FROM=no-reply@RENDFORT.app
EMAIL_PROVIDER=local
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USERNAME=
SMTP_PASSWORD=

TUTOR_PROVIDER=openai_or_other
TUTOR_API_KEY=
TUTOR_MODEL=
EMBEDDING_MODEL=

ASSISTANT_DAILY_FREE_LIMIT=3
ASSISTANT_MAX_TOKENS=600
```

## 17. Installation Future

Ce squelette ne contient pas encore les projets Flutter et FastAPI initialises. Une fois les choix valides, les commandes attendues seront proches de :

### Mobile

```bash
cd apps/mobile
flutter pub get
flutter run
```

### API

```bash
cd services/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Sous Windows PowerShell, l'activation de l'environnement Python sera differente :

```powershell
cd services/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 18. Criteres d'Acceptation MVP V1

Le MVP est considere acceptable si :

- un eleve peut creer un compte et valider son email ;
- un eleve peut completer son onboarding ;
- le dashboard affiche sa progression ;
- le programme Seconde C est navigable ;
- au moins 5 lecons prioritaires sont disponibles ;
- chaque lecon contient objectifs, explication, exemples et quiz ;
- le bouton `Question ?` fonctionne sur une lecon ;
- l'assistant repond avec le contexte de la lecon ;
- un quiz produit un score sur 20 ;
- les resultats de quiz alimentent les competences acquises et points a renforcer ;
- les lecons telechargees restent consultables hors ligne ;
- l'app desactive clairement l'assistance interactive hors ligne ;
- les donnees personnelles sont protegees selon les regles minimales de securite.

## 19. Lecons Prioritaires Proposees

Pour un MVP testable, ne pas commencer par tout le programme.

Lot initial conseille :

1. Ensemble des nombres reels.
2. Polynomes et fractions rationnelles.
3. Equations et inequations dans R.
4. Generalites sur les fonctions.
5. Vecteurs et points du plan.

Ces lecons couvrent une base utile, permettent de tester les explications, les formules, les quiz et le suivi de progression.

## 20. Tests

### Mobile

- tests de widgets critiques ;
- tests navigation ;
- tests stockage offline ;
- tests rendu des formules ;
- tests du dashboard.

### Backend

- tests auth ;
- tests permissions ;
- tests endpoints contenus ;
- tests quiz ;
- tests du tuteur avec mocks du moteur d'assistance ;
- tests quotas.

### Contenu

- validation schema ;
- verification que chaque lecon a au moins un objectif ;
- verification que chaque quiz est lie a une lecon ;
- verification que chaque question a une correction ;
- validation manuelle des formules et enonces.

## 21. Risques MVP

### Risque 1 : contenu trop vaste

Mitigation :

- limiter V1 a 5 lecons ;
- valider chaque lecon avant generation massive.

### Risque 2 : erreurs du moteur d'assistance

Mitigation :

- RAG limite aux lecons validees ;
- reponses courtes ;
- tests pedagogiques ;
- feedback utilisateur.

### Risque 3 : couts d'assistance

Mitigation :

- quotas ;
- cache ;
- mode texte prioritaire ;
- vocal payant ou repousse.

### Risque 4 : mauvaise application des autorisations

Mitigation :

- respecter les autorisations obtenues ;
- conserver le mapping comme outil interne ;
- ne jamais afficher les noms internes des sources dans l'application ;
- utiliser les libelles utilisateur valides : "support de cours", "manuel de reference", "guide pedagogique".

### Risque 5 : mauvaise experience hors ligne

Mitigation :

- expliciter les fonctions indisponibles ;
- synchroniser les lecons prioritaires ;
- eviter que l'utilisateur perde son travail.

## 22. Roadmap

### V1

- socle mobile ;
- auth ;
- dashboard ;
- programme ;
- 5 lecons ;
- quiz ;
- assistant texte contextualise ;
- offline basique.

### V1.1

- plus de lecons ;
- correction assistee plus fine ;
- SymPy pour verification ;
- audio TTS simple ;
- meilleur moteur de recommandation.

### V1.2

- upload PDF limite ;
- OCR serveur ;
- resume de document ;
- explication de passages selectionnes ;
- cache offline des analyses.

### V2

- vocal premium ;
- mode examen ;
- espace parents/professeurs ;
- paiement ;
- analytics pedagogiques avances ;
- application multi-niveaux.

## 23. Decisions a Prendre

Avant implementation complete :

- confirmer la liste exacte des lecons V1 ;
- confirmer le pays et le referentiel officiel cible ;
- choisir Riverpod ou Bloc ;
- choisir SQLAlchemy ou SQLModel ;
- choisir le fournisseur du moteur d'assistance initial ;
- definir la politique de quotas ;
- documenter les autorisations obtenues et leurs limites d'usage ;
- valider la charte UI.

## 24. Definition de Qualite

Une fonctionnalite est terminee seulement si :

- elle fonctionne ;
- elle est testee ;
- elle respecte le niveau Seconde C ;
- elle ne cree pas de dette pedagogique evidente ;
- elle reste comprehensible pour un eleve ;
- elle ne fuit pas de donnees sensibles ;
- elle degrade correctement hors ligne.

## 25. Prochaine Etape Recommandee

La prochaine etape consiste a transformer le programme officiel en un fichier structure `content/programme_2c/official/programme_2c.yaml`, puis a rediger la premiere lecon pilote : `Ensemble des nombres reels`.

Cette lecon pilote servira a tester toute la chaine :

- contenu ;
- affichage mobile ;
- quiz ;
- dashboard ;
- question au tuteur RENDFORT ;
- progression ;
- offline.
