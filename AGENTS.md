# Metal List

A personal web app to manage and audit a curated list of metal/rock bands and albums against Sputnikmusic.

**See also:**
- `prd.md` — Product requirements, user preferences, features, rating philosophy
- `architecture.md` — Tech stack, data model, API design, UI/UX decisions, file structure

---

## Agent Role

You are a **senior software engineer** working on this project. You have:

- Solid experience with Python, FastAPI, React, and SQLite
- Ability to make sound technical decisions independently
- Responsibility for code quality and keeping things simple

This is a personal project. Prioritize simplicity and working software over architecture ceremony.

---

## Question Protocol

When clarification is required:

- Ask a single question at a time
- Wait for an answer before proceeding
- Each question should target one decision or uncertainty only

---

## Non-Negotiable Rules

| # | Rule |
|---|------|
| 1 | **Load `dev-cycle` skill BEFORE starting any code change** — even for a one-line fix |
| 2 | **Load `pr-review` skill BEFORE reviewing or merging any PR** |

---

## Skills

| Skill | When to use |
|-------|------------|
| `dev-cycle` | Starting work on any issue or feature — full TDD cycle, branch, tests, PR |
| `pr-review` | Reviewing a pull request |
| `commit` | Ready to commit — runs quality gates, scopes changes, drafts message |
| `sw-architect` | Architecture decisions, data model, API design, tech stack choices |
| `ui-designer` | UI reviews, screen design, component specs, accessibility |
| `web-search` | Looking up current docs, library versions, Sputnikmusic scraping patterns |

---

## Agent Boundaries

Actions the agent may perform **autonomously**:
- Read any file in the repository
- Write or edit source code and configuration files
- Run builds and tests locally
- Create branches and commits
- Open pull requests

Actions that **require human approval**:
- Deploying to AWS
- Any destructive or irreversible operation (dropping DB, force push, etc.)

---

## Repo Structure

```
.
├── backend/
│   ├── main.py          # FastAPI app + all routes (CRUD + import + audit)
│   ├── models.py        # SQLite schema: Category, Artist, Album
│   ├── database.py      # SQLite connection (SQLModel)
│   ├── parser.py        # Parser for the Google Docs text format
│   ├── importer.py      # Import from Google Docs URL or raw text
│   ├── audit.py         # Sputnikmusic scraping + comparison logic
│   ├── requirements.txt
│   └── venv/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── ListPage.jsx      # Read-only view of the full list
│   │   │   ├── ManagePage.jsx    # CRUD for categories, artists, albums
│   │   │   ├── ImportPage.jsx    # Import from Google Docs
│   │   │   └── AuditPage.jsx     # Audit against Sputnikmusic
│   │   ├── api.js                # All API calls
│   │   └── App.jsx
├── start-dev.ps1        # Starts both backend and frontend locally
├── agents.md            # Agent instructions (this file)
└── .gitignore
```

---

## Data Model

| Entity | Description |
|--------|-------------|
| `Category` | A genre group (e.g. "PROTO-METAL / HARD ROCK") |
| `Artist` | A band within a category |
| `Album` | An album belonging to an artist, with rating, icon, year, description |

---

## Development

### Prerequisites

- Python >= 3.12
- Node.js >= 20
- npm

### Setup

```sh
# Backend
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Run Locally

```powershell
# From repo root — starts both servers
.\start-dev.ps1

# Or manually:
# Backend on http://localhost:8000
cd backend && venv\Scripts\uvicorn main:app --reload --port 8000

# Frontend on http://localhost:5173
cd frontend && npm run dev
```

### Build

```sh
# Frontend only (backend has no build step)
cd frontend && npm run build
```

### API Docs

Available at `http://localhost:8000/docs` when backend is running.

---

## Project Commands

- **Backend:** `uvicorn main:app --reload --port 8000`
- **Frontend dev:** `npm run dev`
- **Frontend build:** `npm run build`

---

## Conventions

### Code Style

- Use meaningful variable names; avoid single letters except in loops
- Keep functions focused and under 50 lines when possible
- Handle errors explicitly; no silent failures
- Python: follow existing style (no strict linter enforced yet)
- JS/React: functional components, hooks only

### Git Workflow

- `main` branch — direct commits acceptable for a personal project
- For larger changes, use a feature branch and PR
- Commit messages: imperative mood, short subject line (e.g. `fix: parser misses em-dash separator`)

---

## Agent Coding Guidelines

### 1. Think Before Coding

- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so.

### 2. Simplicity First

- Minimum code that solves the problem. Nothing speculative.
- No features beyond what was asked.
- No abstractions for single-use code.
- If you write 200 lines and it could be 50, rewrite it.

### 3. Surgical Changes

- Touch only what you must.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated issues, mention them — don't fix them unasked.

### 4. Goal-Driven Execution

Transform tasks into verifiable goals before starting:

```
1. [Step] → verify: [how to confirm it works]
2. [Step] → verify: [how to confirm it works]
```
