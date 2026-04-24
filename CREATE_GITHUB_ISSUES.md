# How to Create GitHub Issues

This guide explains how to create all 20 issues from ISSUES.md as GitHub Issues.

## Prerequisites

You need **GitHub CLI** installed and authenticated.

### Install GitHub CLI

1. **Windows (using Chocolatey)**:
   ```powershell
   choco install gh
   ```

2. **Windows (using Scoop)**:
   ```powershell
   scoop install gh
   ```

3. **Download**:
   - https://github.com/cli/cli/releases
   - Download `gh_*.msi` for Windows
   - Run the installer

### Authenticate

After installing, authenticate with GitHub:

```powershell
gh auth login
```

Follow the prompts:
- Choose: GitHub.com
- Choose: HTTPS
- Authenticate with your browser
- Confirm

Verify authentication:
```powershell
gh auth status
```

---

## Create Issues Automatically

Once `gh` is installed, run the script:

```powershell
cd "C:\Users\corne\Src\Metal Expand your horizons list"
.\create_issues.ps1
```

This will create **10 issues** automatically.

### What Gets Created

The script creates:
1. ✅ FilterBar Component
2. ✅ Clickable Albums
3. ✅ 2-Column Grid Layout
4. ✅ Sidebar Legend
5. ✅ Sample Seed Data
6. ✅ Integration Tests
7. ✅ Mobile Responsive
8. ✅ Dark Mode Toggle
9. ✅ Structured Logging
10. ✅ Input Validation

Each issue includes:
- Detailed description
- Acceptance criteria
- Files to modify
- Labels (high/medium/low priority)
- Effort estimate

---

## Create Issues Manually (If Script Fails)

Use GitHub web UI:

1. Go to: https://github.com/orvalus/Metal-List-project/issues
2. Click: **New Issue**
3. Copy-paste title + body from `ISSUES.md`
4. Add labels: enhancement, frontend, high-priority (etc.)
5. Click: **Submit new issue**

---

## View Issues

After creation, view them at:

**GitHub Issues Page**:
```
https://github.com/orvalus/Metal-List-project/issues
```

**Filter by Priority**:
- High Priority: https://github.com/orvalus/Metal-List-project/issues?q=label%3A%22high-priority%22
- Medium Priority: https://github.com/orvalus/Metal-List-project/issues?q=label%3A%22medium-priority%22
- Low Priority: https://github.com/orvalus/Metal-List-project/issues?q=label%3A%22low-priority%22

---

## Labels Used

- `enhancement` — Feature request
- `frontend` — Frontend work
- `backend` — Backend work
- `testing` — Testing work
- `mobile` — Mobile-specific
- `high-priority` — Blocking MVP
- `medium-priority` — UX improvements
- `low-priority` — Nice to have
- `data` — Database/data related
- `performance` — Performance optimization

---

## Troubleshooting

### "gh: The term 'gh' is not recognized"

**Solution**: GitHub CLI not installed or not in PATH

```powershell
# Check if installed
gh --version

# If not installed, download from:
# https://github.com/cli/cli/releases
```

### "authentication required"

**Solution**: Run authentication

```powershell
gh auth login
gh auth status
```

### "not authorized to perform this operation"

**Solution**: Check GitHub token permissions

```powershell
gh auth refresh
```

### Script doesn't run

**Solution**: Set execution policy

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Manual Issue Creation (Alternative)

If the script fails, create issues manually using this template:

```markdown
## [ISSUE TITLE]

[Description from ISSUES.md]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Files to Modify
- file1.jsx
- file2.jsx

## Priority
[HIGH/MEDIUM/LOW]

## Effort Estimate
[2-3 hours]
```

---

## Next Steps

1. ✅ Create issues using the script or manually
2. Assign issues to yourself or team members
3. Use **Project board** to track progress
4. Update issues as you work (comment, close when done)
5. Link pull requests to issues (auto-closes on merge)

---

## Linking PRs to Issues

When creating a PR, reference the issue:

```
Closes #1
Closes #3
Fixes #5
```

Example commit message:
```
feat: implement FilterBar component

Closes #1
Closes #3
```

GitHub will automatically close the issue when PR merges!

---

**Time to set up**: 5-10 minutes  
**Help needed?**: See GitHub CLI docs https://cli.github.com/manual
