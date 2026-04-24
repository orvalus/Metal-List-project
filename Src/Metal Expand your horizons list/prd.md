# PRD: Metal Expand Your Horizons List

## Overview
A curated, personal music discovery tool for expanding rock/metal listening horizons with high-quality, musically coherent recommendations.

## Target User
- Listener with established taste: Metallica, Iron Maiden, Tool, System of a Down
- Seeks depth and quality over popularity
- Values melody, structure, and intelligible vocals
- Open to exploration within coherent musical territory

## Core Preferences

### Musical Taste
- **Strong preference for:** melody, structure, clarity, composition, memorable arrangements
- **Acceptable but conditional:** harsh vocals (only if music is exceptional + composition is strong)
- **Avoids:** pure brutality/chaos, extreme vocals without musical depth, technical excess without substance

### Rating Philosophy
- Calibrated to Sputnikmusic standards (realistic, not inflated)
- 4.0+ = clearly strong
- 4.5+ = rare, well-justified
- 4.7+ = extremely rare (top-tier all-time)

## Primary Goal
Build a structured, curated canon optimized for:
1. Musical depth and coherence
2. Long-term listening value
3. Variety within defined musical territory
4. Discovery (not just canonical history)

## Data Model

### Hierarchy
- **Category** (Genre group, e.g., "PROTO-METAL / HARD ROCK")
- **Artist** (Band name + technical description)
- **Album** (Title, year, rating, description, Sputnikmusic URL)

### Rating System
- 🔥 **E** = Essential / peak albums
- ⭐ **R** = Recommended / strong albums
- 🌘 **D** = Dense, complex, demanding (progressive/layered)
- ⚠️ **A** = Harsh / extreme (death, black metal, etc.)
- 🌀 **X** = Historical / optional / weaker albums

## Features (MVP)

### Read-Only List View
- Full curated list with all albums, organized by category
- Legend visible (sidebar or top)
- Filterable by tag (E, R, D, A, X)
- **Clickable albums** — open Sputnikmusic album page in new tab
- Responsive design (desktop + mobile)

### Manage Page (Admin)
- CRUD for categories, artists, albums
- Add/edit/delete albums with ratings, tags, descriptions
- Bulk import from Google Docs format

### Import Page
- Parse curated list from Google Docs text or raw markdown
- Map categories, artists, albums into database
- Validate structure and ratings

### Audit Page
- Cross-reference albums against Sputnikmusic.com
- Compare ratings, flag discrepancies
- Track updates over time

## Content Rules
- Include only relevant albums (not full discographies)
- Prioritize albums that expand taste and introduce new ideas
- Avoid redundancy
- Prefer structured, melodic, intentional music

## Initial Scope
Start with: **PROTO-METAL / HARD ROCK** (pioneers of heavy metal)

## Success Metrics
- List is complete and well-organized
- Ratings are defensible and consistent
- User can easily discover and learn about albums
- Easy to maintain and expand over time
