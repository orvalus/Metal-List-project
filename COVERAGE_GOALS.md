# Test Coverage Goals

**Target:** 95% code coverage across backend and frontend  
**Last Updated:** April 24, 2026

---

## Backend (Python)

### Setup
- **Framework:** pytest 7.4.3
- **Coverage Tool:** pytest-cov 4.1.0
- **Config File:** `backend/.coveragerc`

### Coverage Targets
- **Lines:** 95%
- **Functions:** 95%
- **Branches:** 90%

### Running Coverage

```bash
cd backend
venv\Scripts\activate
python -m pytest --cov=. --cov-report=html --cov-report=term-missing
```

### View Report
- Terminal output: Shows missing lines
- HTML report: `backend/htmlcov/index.html`

### What's Covered
- ✅ Models (SQLModel definitions)
- ✅ Database (CRUD operations)
- ✅ Parser (Google Docs format)
- ✅ Importer (import logic)
- ✅ API endpoints (main.py)
- ✅ Audit functionality (Sputnikmusic scraping)

### What's Not (Yet) Covered
- ❌ Edge cases in parser (rare format variations)
- ❌ Network failures in audit (rate limiter stress tests)
- ❌ Database migration scenarios

---

## Frontend (React + Vitest)

### Setup
- **Framework:** Vitest 1.0.4
- **Testing Library:** @testing-library/react 16.0.1
- **Config File:** `frontend/vitest.config.js`

### Coverage Targets
- **Lines:** 80% (MVP minimum, eventually 95%)
- **Functions:** 80%
- **Branches:** 80%
- **Statements:** 80%

### Running Coverage

```bash
cd frontend
npm install --legacy-peer-deps
npm run test:coverage
```

### View Report
- Terminal output: Shows coverage summary
- HTML report: `frontend/coverage/index.html`

### What's Covered
- ✅ App.jsx (routing, navigation)
- ✅ ListPage.jsx (rendering, filtering — in progress)
- ⏳ ManagePage.jsx (CRUD forms — pending)
- ⏳ ImportPage.jsx (text parsing — pending)
- ⏳ AuditPage.jsx (disabled state — pending)
- ⏳ api.js (API calls — pending)

### What's Not (Yet) Covered
- ❌ User interactions (clicks, form submissions)
- ❌ API error scenarios
- ❌ Loading/error states in detail
- ❌ Mobile responsive behavior

---

## CI/CD Integration

### GitHub Actions Workflow
**File:** `.github/workflows/test-coverage.yml`

**Triggers:**
- On push to `main` or `feat/**` branches
- On pull requests to `main`

**Steps:**
1. Install backend dependencies
2. Run backend tests with coverage
3. Upload coverage to Codecov
4. Install frontend dependencies
5. Run frontend tests with coverage
6. Upload coverage to Codecov
7. Summary report

### Codecov Integration
- Dashboard: https://codecov.io/gh/orvalus/Metal-List-project
- Coverage badges for README
- PR comments with coverage impact

---

## Coverage Expectations by Module

### Backend

| Module | Current | Target | Notes |
|--------|---------|--------|-------|
| models.py | ~100% | 100% | All entities tested |
| main.py | ~70% | 95% | Need endpoint tests |
| parser.py | ~85% | 95% | Most cases covered |
| importer.py | ~60% | 95% | Need integration tests |
| audit.py | ~40% | 90% | Need mocking for scraper |
| database.py | ~100% | 100% | All CRUD ops tested |

### Frontend

| Component | Current | Target | Notes |
|-----------|---------|--------|-------|
| App.jsx | ~50% | 90% | Route rendering tested |
| ListPage.jsx | ~30% | 90% | Need filter tests |
| ManagePage.jsx | 0% | 85% | Not started |
| ImportPage.jsx | 0% | 85% | Not started |
| AuditPage.jsx | 50% | 85% | Just disabled state |
| api.js | 0% | 90% | Need mocking |

---

## Workflow: Adding Tests

1. **Before coding:** Check current coverage
   ```bash
   cd backend && python -m pytest --cov --cov-report=term-missing
   cd frontend && npm run test:coverage
   ```

2. **Write tests first:** (TDD)
   - Red: Tests fail
   - Green: Code passes tests
   - Refactor: Improve coverage

3. **Verify coverage improvement:**
   ```bash
   pytest --cov --cov-report=html  # Backend
   npm run test:coverage            # Frontend
   ```

4. **Open report in browser:**
   - `backend/htmlcov/index.html`
   - `frontend/coverage/index.html`

5. **Commit with coverage context:**
   ```
   test: add tests for X feature (coverage: 72% → 85%)
   ```

---

## Future Improvements

- [ ] Set coverage thresholds in CI (fail if < 95%)
- [ ] Add SonarQube for code quality
- [ ] Parallel test execution for speed
- [ ] Coverage trend tracking
- [ ] Branch coverage focus (hardest 10% of code)
- [ ] E2E test coverage (Playwright/Cypress)

---

## References

- **Backend:** https://pytest-cov.readthedocs.io/
- **Frontend:** https://vitest.dev/guide/coverage.html
- **Codecov:** https://docs.codecov.com/

