# Architecture: Metal Expand Your Horizons List

## Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Backend | Python 3.12+ / FastAPI | Fast, modern, great for APIs + web scraping |
| Database | SQLite + SQLModel | Simple, zero-config, sufficient for personal project scale |
| Frontend | React 18+ / Vite | Component-based, fast dev experience, easy state management |
| Scraping | BeautifulSoup / Requests | Parse Sputnikmusic.com for audit feature |

## Data Model

### Core Entities

```
Category
├── name (str, unique) — e.g., "PROTO-METAL / HARD ROCK"
├── description (str) — short genre description
└── order (int) — display order

Artist
├── name (str)
├── category_id (FK)
├── genre (str) — e.g., "Hard Rock / Blues Rock / Proto-Metal"
├── description (str) — artist overview
└── order (int)

Album
├── title (str)
├── artist_id (FK)
├── year (int)
├── rating (float, 3.0–4.7 scale)
├── tag (enum: E, R, D, A, X)
├── description (str) — one-line review
└── order (int)
```

### Tag Semantics

| Tag | Icon | Meaning | Use Case |
|-----|------|---------|----------|
| **E** | 🔥 | Essential | Peak albums, foundational works |
| **R** | ⭐ | Recommended | Strong, accessible albums |
| **D** | 🌘 | Dense | Progressive, complex, demanding |
| **A** | ⚠️ | Harsh | Harsh/extreme vocals dominant |
| **X** | 🌀 | Historical | Early/raw/inconsistent (context only) |

**Constraints:**
- Do NOT use 🌘D for weak albums
- Use 🌀X for early/raw/inconsistent work
- Use ⚠️A ONLY when harsh vocals are dominant

## UI Architecture

### Pages

#### 1. ListPage (Read-Only)
- Display full curated list
- Sidebar with legend (sticky on desktop, collapsible on mobile)
- Categories collapsible/expandable
- Albums in 2-column grid (responsive: 1 col on mobile)
- Filter buttons: All, 🔥E, ⭐R, 🌘D, ⚠️A, 🌀X
- Search/quick filter (optional MVP+)

#### 2. ManagePage (Admin CRUD)
- Category management (add/edit/delete)
- Artist management (add/edit/delete)
- Album management (add/edit/delete with inline form)
- Drag-to-reorder (optional MVP+)
- Bulk import button

#### 3. ImportPage
- Paste Google Docs text or raw markdown
- Parse structure (categories → artists → albums)
- Preview parsed data before committing
- Validate ratings, tags, format
- Import to database

#### 4. AuditPage
- Cross-reference albums against Sputnikmusic
- Display found ratings vs. our ratings
- Flag significant discrepancies
- Update notes (optional)

### Component Structure

```
App.jsx
├── Navbar (nav between pages)
├── ListPage.jsx
│   ├── Legend.jsx (sidebar)
│   ├── FilterBar.jsx
│   ├── CategorySection.jsx
│   │   ├── ArtistCard.jsx
│   │   └── AlbumCard.jsx
├── ManagePage.jsx
│   ├── CategoryManager.jsx
│   ├── ArtistManager.jsx
│   └── AlbumManager.jsx
├── ImportPage.jsx
│   ├── TextInput.jsx
│   ├── Parser.jsx
│   └── PreviewTable.jsx
└── AuditPage.jsx
    ├── AuditResults.jsx
    └── DiscrepancyList.jsx
```

## Backend API Routes

### Categories
- `GET /api/categories` — list all
- `POST /api/categories` — create
- `PUT /api/categories/{id}` — update
- `DELETE /api/categories/{id}` — delete

### Artists
- `GET /api/artists?category_id=X` — list by category
- `POST /api/artists` — create
- `PUT /api/artists/{id}` — update
- `DELETE /api/artists/{id}` — delete

### Albums
- `GET /api/albums?artist_id=X` — list by artist
- `POST /api/albums` — create
- `PUT /api/albums/{id}` — update
- `DELETE /api/albums/{id}` — delete

### Import
- `POST /api/import/parse` — parse text, return preview
- `POST /api/import/commit` — import to database

### Audit
- `POST /api/audit/check` — scrape Sputnikmusic, compare ratings
- `GET /api/audit/results` — return stored audit results

## Parser Format (Google Docs)

```
CATEGORY NAME
*description in italics*

***Artist Name*** – short genre/style description
- Album Title (Year) – ICON – ★Rating – one-line description
- Album Title (Year) – ICON – ★Rating – one-line description

***Another Artist*** – genre
- Album (Year) – ICON – ★Rating – description
```

## Design Decisions

### 1. Sidebar Legend (Fixed)
- **Why:** User needs to understand tag meanings at a glance
- **How:** Sticky sidebar on desktop, collapsible drawer on mobile
- **Rationale:** Reduces cognitive load for new users

### 2. 2-Column Album Grid
- **Why:** Fit more albums per screen without truncating descriptions
- **How:** CSS Grid, responsive (1 col on mobile)
- **Rationale:** Balance readability and information density

### 3. Collapsible Categories
- **Why:** Long list becomes unwieldy; users want to focus on specific genres
- **How:** Click category header to toggle visibility
- **Rationale:** Reduces scroll fatigue, improves UX

### 4. Color-Coded Tags
- **Why:** Visual scanning is faster than reading text
- **How:** Subtle background colors for each tag (E, R, D, A, X)
- **Rationale:** Accessibility + quick filtering

### 5. SQLite Backend
- **Why:** Personal project, no scaling concerns, fast iteration
- **How:** Single-file DB, SQLModel for type safety
- **Rationale:** Zero DevOps, easy to backup, sufficient for data size

### 6. FastAPI
- **Why:** Modern Python, async support, built-in validation + API docs
- **How:** Pydantic models, dependency injection, auto-generated OpenAPI schema
- **Rationale:** Fast development, maintainable code

## Deployment (Future)

### Development
- Backend: `uvicorn main:app --reload --port 8000`
- Frontend: `npm run dev` (Vite dev server on :5173)
- Both via: `./start-dev.ps1`

### Production (AWS)
- Backend: Docker container + ECS / App Runner
- Frontend: S3 + CloudFront (static build)
- Database: RDS SQLite → or managed PostgreSQL if scaling

## Future Considerations

### MVP+
- Search/filter by album title, artist, year
- Sorting (by rating, year, added date)
- User accounts (if multi-user)
- Dark mode toggle

### Scale
- Expand to more categories (80s metal, 90s grunge, etc.)
- User ratings / personal notes per album
- Collaborative lists / sharing
- Mobile app (React Native or PWA)

## File Structure

```
.
├── backend/
│   ├── main.py              # FastAPI app + all routes
│   ├── models.py            # SQLModel definitions
│   ├── database.py          # SQLite connection, session management
│   ├── parser.py            # Google Docs text parser
│   ├── importer.py          # Import logic (parse → validate → commit)
│   ├── audit.py             # Sputnikmusic scraping + comparison
│   ├── requirements.txt
│   └── venv/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── ListPage.jsx
│   │   │   ├── ManagePage.jsx
│   │   │   ├── ImportPage.jsx
│   │   │   └── AuditPage.jsx
│   │   ├── components/
│   │   │   ├── Legend.jsx
│   │   │   ├── FilterBar.jsx
│   │   │   ├── CategorySection.jsx
│   │   │   ├── ArtistCard.jsx
│   │   │   ├── AlbumCard.jsx
│   │   │   └── ... (other components)
│   │   ├── api.js           # All API calls
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── prd.md                   # Product requirements
├── architecture.md          # This file
├── agents.md                # Agent instructions
├── start-dev.ps1            # Dev startup script
└── .gitignore
```

## Notes

- Ratings calibrated to Sputnikmusic philosophy (realistic, not inflated)
- Categories organized chronologically and by genre
- Album selection prioritizes **discovery over comprehensiveness**
- Descriptions are concise one-liners, not detailed reviews
