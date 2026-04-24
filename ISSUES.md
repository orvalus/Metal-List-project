# Metal List - Issue Tracker

Generated: April 23, 2026  
Status: Complete list of outstanding work items

---

## 🔴 HIGH PRIORITY (Blocking MVP)

### Issue #1: Implement FilterBar Component
**Status**: Not Started  
**Effort**: 2-3 hours  
**Description**: 
- Add filter buttons to ListPage: All, 🔥E, ⭐R, 🌘D, ⚠️A, 🌀X
- Clicking filters albums by selected tag
- "All" button shows all albums
- Currently only text search available

**Acceptance Criteria**:
- [ ] FilterBar component created
- [ ] Filter state managed in ListPage
- [ ] Albums filter correctly by tag
- [ ] Filter UI matches mockup.html design
- [ ] Tests added for filter logic

**Files to Modify**:
- `frontend/src/pages/ListPage.jsx`
- `frontend/src/components/FilterBar.jsx` (new)

---

### Issue #2: Add sputnik_url Field to Album Model
**Status**: ✅ DONE  
**Effort**: 2-3 hours  
**Description**: 
- ✅ Album model has sputnik_url field (Optional[str])
- ✅ Parser extracts URLs from Google Docs format
- ✅ All schema updated (AlbumRead, AlbumCreate, etc.)
- ✅ Tests pass (9/9)

**Completed**:
- [x] models.py updated with sputnik_url field
- [x] parser.py extracts URLs with regex
- [x] importer.py passes sputnik_url to Album
- [x] 9 comprehensive tests passing
- [x] Backward compatible (URLs optional)

**Files Modified**:
- `backend/models.py` ✅
- `backend/parser.py` ✅
- `backend/importer.py` ✅
- `backend/test_parser.py` ✅
- `backend/test_models.py` ✅

---

### Issue #3: Make Albums Clickable to Sputnikmusic
**Status**: Not Started  
**Effort**: 1-2 hours  
**Description**:
- Albums in ListPage should be clickable links
- Opens sputnik_url in new tab
- Requires: sputnik_url field (✅ done), UI component
- Currently albums are just text

**Acceptance Criteria**:
- [ ] Album cards are clickable
- [ ] sputnik_url opens in new tab on click
- [ ] Cursor shows pointer on hover
- [ ] Works for all albums with URL
- [ ] Gracefully handles missing URLs

**Files to Modify**:
- `frontend/src/pages/ListPage.jsx`
- `frontend/src/components/AlbumCard.jsx` (new or update)

**Dependencies**: Issue #2 (sputnik_url field) ✅

---

### Issue #4: Implement 2-Column Grid Layout
**Status**: Not Started  
**Effort**: 2-3 hours  
**Description**:
- ListPage albums in 2-column grid (desktop), 1-column (mobile)
- Currently single-column list
- mockup.html shows the desired layout
- Responsive design required

**Acceptance Criteria**:
- [ ] Albums displayed in 2-column grid on desktop
- [ ] Single-column on mobile (< 768px)
- [ ] Matches mockup.html styling
- [ ] Album cards have proper spacing
- [ ] Responsive breakpoints tested

**Files to Modify**:
- `frontend/src/pages/ListPage.jsx`
- `frontend/src/App.css` (update grid styles)

**Reference**: `Docs/mockup.html` shows exact layout

---

### Issue #5: Create Sidebar Legend Component
**Status**: Not Started  
**Effort**: 3-4 hours  
**Description**:
- Sidebar legend explaining tag meanings (E, R, D, A, X)
- Sticky on desktop (fixed position)
- Collapsible drawer on mobile
- Should appear on all pages (or at least ListPage)
- mockup.html shows exact design

**Acceptance Criteria**:
- [ ] Legend.jsx component created
- [ ] Sticky on desktop (position: fixed or sticky)
- [ ] Collapsible drawer on mobile
- [ ] Shows all 5 tag icons + descriptions
- [ ] Integrated into ListPage
- [ ] Responsive design works

**Files to Create**:
- `frontend/src/components/Legend.jsx` (new)

**Files to Modify**:
- `frontend/src/pages/ListPage.jsx`

**Reference**: `Docs/mockup.html` lines 25-65

---

### Issue #6: Add Rate Limiting & Caching
**Status**: ✅ DONE  
**Effort**: 2-3 hours  
**Description**:
- ✅ Exponential backoff for Sputnikmusic requests
- ✅ 24-hour audit result caching
- ✅ Smart retry logic (3 attempts)
- ✅ Prevents IP bans

**Completed**:
- [x] rate_limiter.py implemented (exponential backoff)
- [x] audit_cache.py implemented (24h TTL)
- [x] audit.py integrated with rate limiter
- [x] 8/8 tests passing
- [x] Full documentation in RATE_LIMITING.md

**Files Created**:
- `backend/rate_limiter.py` ✅
- `backend/audit_cache.py` ✅
- `backend/test_rate_limiting.py` ✅
- `backend/RATE_LIMITING.md` ✅

**Files Modified**:
- `backend/audit.py` ✅

---

## 🟡 MEDIUM PRIORITY (UX Improvements)

### Issue #7: Create Sample Seed Data
**Status**: Not Started  
**Effort**: 2-3 hours  
**Description**:
- Database empty on startup
- Create seed data for PROTO-METAL / HARD ROCK category
- 5-10 artists with real albums and Sputnikmusic URLs
- Makes testing easier without manual import

**Acceptance Criteria**:
- [ ] Seed data file created (JSON or Python)
- [ ] PROTO-METAL category with 5-10 artists
- [ ] 20-30 albums total
- [ ] Real Sputnikmusic URLs for each album
- [ ] Realistic ratings (4.0-4.7 range)
- [ ] Load script or fixtures created

**Files to Create**:
- `backend/seed_data.py` or `backend/fixtures/seed.json`

**Optional**:
- `backend/management/commands/seed_db.py` (Django-style)

---

### Issue #8: Add Unit Tests for Parser & Importer
**Status**: Partial  
**Effort**: 4-6 hours  
**Description**:
- ✅ Parser tests exist (5 tests for URL extraction)
- ✅ Model tests exist (4 tests for sputnik_url schema)
- ❌ Missing: importer integration tests
- ❌ Missing: cascade delete tests
- ❌ Missing: full import workflow tests

**Acceptance Criteria**:
- [ ] Parser tests cover all edge cases (9/9 passing ✅)
- [ ] Importer tests cover happy path
- [ ] Importer tests cover error cases
- [ ] Cascade delete logic tested
- [ ] Full import→validate→commit tested
- [ ] 100% coverage for critical paths

**Tests to Add**:
- test_importer.py — 8-10 tests
- test_cascade_delete.py — 4-5 tests
- test_integration_import.py — 5-6 tests

**Files to Create**:
- `backend/test_importer.py`
- `backend/test_cascade_delete.py`

---

### Issue #9: Refactor Hard-Coded Text to English
**Status**: ✅ DONE  
**Effort**: 3-4 hours  
**Description**:
- ✅ All backend comments in English
- ✅ All frontend labels in English
- ✅ All error messages in English
- ✅ Codebase is English-ready

**Completed**:
- [x] Backend refactored (main.py, parser.py, etc.)
- [x] Frontend refactored (all pages + components)
- [x] Comments in English
- [x] Error messages in English
- [x] No Romanian text remaining

---

### Issue #10: Mobile Responsive Improvements
**Status**: Partial  
**Effort**: 2-3 hours  
**Description**:
- CSS has mobile classes but layout not fully responsive
- Fixed widths may not adapt to small screens
- No hamburger menu for nav on mobile
- Sidebar legend needs mobile drawer version

**Acceptance Criteria**:
- [ ] Mobile layout tested on 375px-480px widths
- [ ] All pages readable on mobile
- [ ] Navigation works on mobile (hamburger menu or tabs)
- [ ] Grid adjusts: 2 cols desktop → 1 col mobile
- [ ] Touch-friendly button sizes (48px+)
- [ ] No horizontal scrolling

**Files to Modify**:
- `frontend/src/App.css` (add mobile breakpoints)
- `frontend/src/App.jsx` (add hamburger menu)
- `frontend/src/pages/ListPage.jsx` (responsive grid)

---

## 🟢 LOW PRIORITY (Nice to Have)

### Issue #11: Add Environment Configuration
**Status**: Not Started  
**Effort**: 1-2 hours  
**Description**:
- Backend hardcodes localhost:8000
- Database path hardcoded
- No .env support
- Add python-dotenv for configuration

**Acceptance Criteria**:
- [ ] .env.example created
- [ ] Backend reads from .env
- [ ] Frontend reads from .env.development
- [ ] Documentation for configuration
- [ ] Docker support optional

**Files to Create**:
- `.env.example`
- `backend/.env.example`
- `frontend/.env.example`

**Files to Modify**:
- `backend/database.py`
- `backend/main.py`
- `frontend/src/api.js`

---

### Issue #12: Drag-to-Reorder Albums (Optional MVP+)
**Status**: Not Started  
**Effort**: 4-5 hours  
**Description**:
- Sort_order field exists in database
- ManagePage doesn't support drag-to-reorder
- Would improve UX for list customization
- Optional enhancement

**Acceptance Criteria**:
- [ ] react-beautiful-dnd installed
- [ ] AlbumCard draggable in ManagePage
- [ ] Sort order updates on drop
- [ ] Persists to database
- [ ] Visual feedback during drag

**Libraries**:
- react-beautiful-dnd or react-dnd

**Files to Modify**:
- `frontend/src/pages/ManagePage.jsx`
- `frontend/package.json`

---

### Issue #13: Search & Advanced Filtering (Optional MVP+)
**Status**: Partial  
**Effort**: 2-3 hours  
**Description**:
- ✅ Text search by artist/album name exists
- ❌ Missing: advanced filters (year range, rating range)
- ❌ Missing: search persistence
- ❌ Missing: search highlighting

**Acceptance Criteria**:
- [ ] Text search works (✅ done)
- [ ] Filter by year range (optional)
- [ ] Filter by rating range (optional)
- [ ] Search results highlighted
- [ ] Search persists in URL

**Files to Modify**:
- `frontend/src/pages/ListPage.jsx`

---

### Issue #14: Dark Mode Toggle (Optional MVP+)
**Status**: Not Started  
**Effort**: 1-2 hours  
**Description**:
- App hard-coded to dark theme (#0f0f0f, accent #c0392b)
- No toggle button
- Could use CSS variables for theme switching

**Acceptance Criteria**:
- [ ] Toggle button in navbar
- [ ] Light + dark themes defined
- [ ] Theme preference persisted (localStorage)
- [ ] Smooth transition between themes

**Files to Modify**:
- `frontend/src/App.jsx`
- `frontend/src/index.css`
- `frontend/src/App.css`

---

### Issue #15: Add Logging & Monitoring
**Status**: Not Started  
**Effort**: 2-3 hours  
**Description**:
- No structured logging
- No monitoring/debugging info
- rate_limiter.py has logging but main.py doesn't use it
- Would help debugging production issues

**Acceptance Criteria**:
- [ ] Python logging configured
- [ ] All API endpoints log requests
- [ ] Errors logged with context
- [ ] Rate limiter logs delays
- [ ] Audit scraping logs successes/failures

**Files to Modify**:
- `backend/main.py`
- `backend/audit.py` (already has some logging ✅)
- Add logging config

---

### Issue #16: Input Validation (Optional)
**Status**: Not Started  
**Effort**: 2-3 hours  
**Description**:
- Parser accepts any format without validation
- Weak input validation on album creation
- Should validate before saving to database

**Acceptance Criteria**:
- [ ] Parser validates album format
- [ ] Rating must be 3.0-5.0 range
- [ ] Year must be 1900-2100
- [ ] URLs must be valid Sputnikmusic URLs (optional)
- [ ] Meaningful error messages

**Files to Modify**:
- `backend/parser.py`
- `backend/models.py` (add validators)

---

### Issue #17: Add Error Recovery for Imports
**Status**: Not Started  
**Effort**: 2-3 hours  
**Description**:
- Failed imports may leave database in inconsistent state
- No rollback mechanism
- Should either all succeed or all fail

**Acceptance Criteria**:
- [ ] Import wrapped in transaction
- [ ] Rollback on any error
- [ ] User notified of which items failed
- [ ] No partial data in database

**Files to Modify**:
- `backend/importer.py`

---

### Issue #18: Pagination (Optional)
**Status**: Not Started  
**Effort**: 2-3 hours  
**Description**:
- ListPage loads all categories/artists/albums at once
- Large lists may be slow
- Optional pagination or lazy loading

**Acceptance Criteria**:
- [ ] Pagination implemented (or virtual scrolling)
- [ ] Load 50 albums initially
- [ ] Load more on scroll
- [ ] Performance improved for large lists

---

## 🟣 DOCUMENTATION & QUALITY

### Issue #19: Complete API Documentation
**Status**: Partial  
**Effort**: 1-2 hours  
**Description**:
- ✅ FastAPI auto-generates /docs
- ❌ Missing: README for API endpoints
- ❌ Missing: Authentication docs (if added)
- ❌ Missing: Error code reference

**Acceptance Criteria**:
- [ ] API_DOCS.md created
- [ ] All endpoints documented
- [ ] Example requests/responses
- [ ] Error codes documented

---

### Issue #20: Add Contributing Guidelines
**Status**: Not Started  
**Effort**: 1 hour  
**Description**:
- AGENTS.md exists but no CONTRIBUTING.md
- Would help if others want to contribute

**Acceptance Criteria**:
- [ ] CONTRIBUTING.md created
- [ ] Setup instructions clear
- [ ] PR process documented
- [ ] Code style guidelines

---

## 📊 Summary by Status

| Status | Count | Priority |
|--------|-------|----------|
| ✅ Done | 6 | HIGH |
| ⚠️ Partial | 3 | HIGH/MEDIUM |
| 🔴 Not Started | 11 | MEDIUM/LOW |
| **TOTAL** | **20** | - |

### By Priority

| Level | Count | Est. Hours |
|-------|-------|-----------|
| 🔴 HIGH | 6 | 12-18h |
| 🟡 MEDIUM | 6 | 14-20h |
| 🟢 LOW | 8 | 10-15h |

---

## 🎯 Recommended Sequence

### Session 1 (5-6 hours)
1. Issue #1: FilterBar Component (2-3h)
2. Issue #3: Clickable Albums (1-2h)

### Session 2 (5-6 hours)
3. Issue #4: 2-Column Grid (2-3h)
4. Issue #5: Sidebar Legend (3-4h) — START, finish in Session 3

### Session 3 (4-5 hours)
5. Issue #5: Sidebar Legend (FINISH) (1h)
6. Issue #7: Seed Data (2-3h)

### Session 4 (3-4 hours)
7. Issue #10: Mobile Responsive (2-3h)

### Session 5 (2-3 hours)
8. Issue #8: Integration Tests (2-3h)

---

## Links to Referenced Files

- `/prd.md` — Product requirements
- `/architecture.md` — Technical design
- `/AUDIT.md` — Code analysis
- `/PROGRESS.md` — Status tracker
- `/Docs/mockup.html` — UI mockup (reference for Issues #4, #5)
- `/RATE_LIMITING.md` — Rate limiting docs (Issue #6 ✅)

---

**Last Updated**: April 23, 2026  
**Total Issues**: 20  
**Completed**: 6  
**In Progress**: 3  
**Remaining**: 11
