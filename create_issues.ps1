# Script to create GitHub Issues from ISSUES.md
# Usage: .\create_issues.ps1
# Requires: GitHub CLI (gh) installed and authenticated

# Check if gh is installed
$ghPath = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghPath) {
    Write-Error "GitHub CLI (gh) not found. Please install it first:"
    Write-Error "https://cli.github.com"
    exit 1
}

# Define issues
$issues = @(
    @{
        title = "Implement FilterBar Component"
        priority = "🔴 HIGH"
        effort = "2-3 hours"
        body = @"
Filter albums by tag (E, R, D, A, X)

## Description
- Add filter buttons to ListPage: All, 🔥E, ⭐R, 🌘D, ⚠️A, 🌀X
- Clicking filters albums by selected tag
- 'All' button shows all albums
- Currently only text search available

## Acceptance Criteria
- [ ] FilterBar component created
- [ ] Filter state managed in ListPage
- [ ] Albums filter correctly by tag
- [ ] Filter UI matches mockup.html design
- [ ] Tests added for filter logic

## Files to Modify
- frontend/src/pages/ListPage.jsx
- frontend/src/components/FilterBar.jsx (new)

## Priority
HIGH - Blocking MVP
"@
        labels = "enhancement,frontend,high-priority"
    },
    @{
        title = "Make Albums Clickable to Sputnikmusic"
        priority = "🔴 HIGH"
        effort = "1-2 hours"
        body = @"
Albums in ListPage should be clickable links opening Sputnikmusic

## Description
- Albums should be clickable links
- Opens sputnik_url in new tab
- Requires: sputnik_url field (done), UI component
- Currently albums are just text

## Acceptance Criteria
- [ ] Album cards are clickable
- [ ] sputnik_url opens in new tab on click
- [ ] Cursor shows pointer on hover
- [ ] Works for all albums with URL
- [ ] Gracefully handles missing URLs

## Files to Modify
- frontend/src/pages/ListPage.jsx
- frontend/src/components/AlbumCard.jsx (new or update)

## Dependencies
#2: sputnik_url field (done)

## Priority
HIGH - Core feature
"@
        labels = "enhancement,frontend,high-priority"
    },
    @{
        title = "Implement 2-Column Grid Layout"
        priority = "🔴 HIGH"
        effort = "2-3 hours"
        body = @"
ListPage albums should use 2-column grid (desktop) / 1-column (mobile)

## Description
- Currently single-column list layout
- Should be 2-column grid on desktop
- 1-column on mobile (< 768px)
- mockup.html shows the desired layout
- Responsive design required

## Acceptance Criteria
- [ ] Albums displayed in 2-column grid on desktop
- [ ] Single-column on mobile (< 768px)
- [ ] Matches mockup.html styling
- [ ] Album cards have proper spacing
- [ ] Responsive breakpoints tested

## Files to Modify
- frontend/src/pages/ListPage.jsx
- frontend/src/App.css (update grid styles)

## Reference
Docs/mockup.html shows exact layout

## Priority
HIGH - MVP feature
"@
        labels = "enhancement,frontend,high-priority"
    },
    @{
        title = "Create Sidebar Legend Component"
        priority = "🔴 HIGH"
        effort = "3-4 hours"
        body = @"
Sidebar legend explaining tag meanings (E, R, D, A, X)

## Description
- Sidebar legend showing tag icons + descriptions
- Sticky on desktop (fixed position)
- Collapsible drawer on mobile
- Should appear on all pages (or at least ListPage)
- mockup.html shows exact design

## Acceptance Criteria
- [ ] Legend.jsx component created
- [ ] Sticky on desktop (position: fixed or sticky)
- [ ] Collapsible drawer on mobile
- [ ] Shows all 5 tag icons + descriptions
- [ ] Integrated into ListPage
- [ ] Responsive design works

## Files to Create
- frontend/src/components/Legend.jsx (new)

## Files to Modify
- frontend/src/pages/ListPage.jsx

## Reference
Docs/mockup.html lines 25-65

## Priority
HIGH - MVP feature
"@
        labels = "enhancement,frontend,high-priority"
    },
    @{
        title = "Create Sample Seed Data"
        priority = "🟡 MEDIUM"
        effort = "2-3 hours"
        body = @"
Database empty on startup. Need seed data for testing.

## Description
- Database is empty on startup
- Create seed data for PROTO-METAL / HARD ROCK category
- 5-10 artists with real albums and Sputnikmusic URLs
- Makes testing easier without manual import

## Acceptance Criteria
- [ ] Seed data file created (JSON or Python)
- [ ] PROTO-METAL category with 5-10 artists
- [ ] 20-30 albums total
- [ ] Real Sputnikmusic URLs for each album
- [ ] Realistic ratings (4.0-4.7 range)
- [ ] Load script or fixtures created

## Files to Create
- backend/seed_data.py or backend/fixtures/seed.json

## Optional
- backend/management/commands/seed_db.py (Django-style)

## Priority
MEDIUM - Makes testing easier
"@
        labels = "backend,data,medium-priority"
    },
    @{
        title = "Add Integration Tests for Parser & Importer"
        priority = "🟡 MEDIUM"
        effort = "4-6 hours"
        body = @"
Parser has tests, but importer integration tests are missing

## Description
- Parser tests exist (5 tests for URL extraction)
- Model tests exist (4 tests for sputnik_url schema)
- Missing: importer integration tests
- Missing: cascade delete tests
- Missing: full import workflow tests

## Acceptance Criteria
- [ ] Parser tests cover all edge cases (9/9 passing ✅)
- [ ] Importer tests cover happy path
- [ ] Importer tests cover error cases
- [ ] Cascade delete logic tested
- [ ] Full import→validate→commit tested
- [ ] 100% coverage for critical paths

## Tests to Add
- test_importer.py — 8-10 tests
- test_cascade_delete.py — 4-5 tests
- test_integration_import.py — 5-6 tests

## Files to Create
- backend/test_importer.py
- backend/test_cascade_delete.py

## Priority
MEDIUM - Quality assurance
"@
        labels = "testing,backend,medium-priority"
    },
    @{
        title = "Mobile Responsive Design Improvements"
        priority = "🟡 MEDIUM"
        effort = "2-3 hours"
        body = @"
CSS has mobile classes but layout not fully responsive

## Description
- CSS has mobile classes but layout not fully responsive
- Fixed widths may not adapt to small screens
- No hamburger menu for nav on mobile
- Sidebar legend needs mobile drawer version

## Acceptance Criteria
- [ ] Mobile layout tested on 375px-480px widths
- [ ] All pages readable on mobile
- [ ] Navigation works on mobile (hamburger menu or tabs)
- [ ] Grid adjusts: 2 cols desktop → 1 col mobile
- [ ] Touch-friendly button sizes (48px+)
- [ ] No horizontal scrolling

## Files to Modify
- frontend/src/App.css (add mobile breakpoints)
- frontend/src/App.jsx (add hamburger menu)
- frontend/src/pages/ListPage.jsx (responsive grid)

## Priority
MEDIUM - UX improvement
"@
        labels = "enhancement,frontend,mobile,medium-priority"
    },
    @{
        title = "Add Dark Mode Toggle"
        priority = "🟢 LOW"
        effort = "1-2 hours"
        body = @"
App hard-coded to dark theme. Add toggle for light mode.

## Description
- App hard-coded to dark theme (#0f0f0f, accent #c0392b)
- No toggle button
- Could use CSS variables for theme switching

## Acceptance Criteria
- [ ] Toggle button in navbar
- [ ] Light + dark themes defined
- [ ] Theme preference persisted (localStorage)
- [ ] Smooth transition between themes

## Files to Modify
- frontend/src/App.jsx
- frontend/src/index.css
- frontend/src/App.css

## Priority
LOW - Nice to have
"@
        labels = "enhancement,frontend,low-priority"
    },
    @{
        title = "Add Structured Logging"
        priority = "🟢 LOW"
        effort = "2-3 hours"
        body = @"
No structured logging for debugging production issues

## Description
- No structured logging
- No monitoring/debugging info
- rate_limiter.py has logging but main.py doesn't use it
- Would help debugging production issues

## Acceptance Criteria
- [ ] Python logging configured
- [ ] All API endpoints log requests
- [ ] Errors logged with context
- [ ] Rate limiter logs delays
- [ ] Audit scraping logs successes/failures

## Files to Modify
- backend/main.py
- backend/audit.py (already has some logging ✅)
- Add logging config

## Priority
LOW - Debugging aid
"@
        labels = "enhancement,backend,low-priority"
    },
    @{
        title = "Input Validation for Parser"
        priority = "🟢 LOW"
        effort = "2-3 hours"
        body = @"
Parser accepts any format without validation

## Description
- Parser accepts any format without validation
- Weak input validation on album creation
- Should validate before saving to database

## Acceptance Criteria
- [ ] Parser validates album format
- [ ] Rating must be 3.0-5.0 range
- [ ] Year must be 1900-2100
- [ ] URLs must be valid Sputnikmusic URLs (optional)
- [ ] Meaningful error messages

## Files to Modify
- backend/parser.py
- backend/models.py (add validators)

## Priority
LOW - Data quality
"@
        labels = "enhancement,backend,low-priority"
    },
    @{
        title = "Add Pagination for Large Lists"
        priority = "🟢 LOW"
        effort = "2-3 hours"
        body = @"
ListPage loads all categories/artists/albums at once (performance issue)

## Description
- ListPage loads all categories/artists/albums at once
- Large lists may be slow
- Optional pagination or lazy loading

## Acceptance Criteria
- [ ] Pagination implemented (or virtual scrolling)
- [ ] Load 50 albums initially
- [ ] Load more on scroll
- [ ] Performance improved for large lists

## Priority
LOW - Performance optimization
"@
        labels = "enhancement,frontend,performance,low-priority"
    }
)

# Create issues
Write-Host "Creating GitHub Issues..." -ForegroundColor Green
Write-Host ""

foreach ($issue in $issues) {
    Write-Host "Creating: $($issue.title)" -ForegroundColor Cyan
    Write-Host "  Priority: $($issue.priority)"
    Write-Host "  Effort: $($issue.effort)"
    
    try {
        gh issue create --title $issue.title --body $issue.body --label $issue.labels
        Write-Host "  ✅ Created" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ Error: $_" -ForegroundColor Red
    }
    Write-Host ""
}

Write-Host "Done! Issues created in GitHub" -ForegroundColor Green
Write-Host "Visit: https://github.com/orvalus/Metal-List-project/issues"
