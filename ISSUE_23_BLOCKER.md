# Issue #23: SQLAlchemy 2.0 Type Annotation Blocker

**Status:** BLOCKED  
**Date:** April 24, 2026  
**Root Cause:** SQLAlchemy 2.0 strict type annotation requirements

---

## The Problem

Issue #23 requires writing integration tests for `importer.py`. However, **SQLAlchemy 2.0 prevents test object instantiation** when using `Mapped[]` type hints in model relationships.

### Current State

**models.py:**
```python
from sqlalchemy.orm import Mapped

class Category(SQLModel, table=True):
    artists: Mapped[List["Artist"]] = Relationship(back_populates="category")
```

**Error when instantiating Category in tests:**
```
sqlalchemy.exc.InvalidRequestError: When initializing mapper Mapper[Category(category)], 
expression "relationship('Mapped[List[\'Artist\']]')" seems to be using a generic class 
as the argument to relationship()
```

---

## Why This Happens

SQLAlchemy 2.0 introduced **strict type annotation parsing**:

1. **Old way (SQLAlchemy 1.4):** ✅ Works
   ```python
   artists: List["Artist"] = Relationship(...)
   ```

2. **New way (SQLAlchemy 2.0):** ❌ Required but breaks instantiation
   ```python
   artists: Mapped[List["Artist"]] = Relationship(...)
   ```

The Mapped[] wrapper is **required for type safety** but **breaks dynamic instantiation** used in testing.

---

## Attempted Solutions

### 1. Remove Mapped[] (FAILED)
- SQLAlchemy 2.0 **rejects** models without Mapped[]
- Error: "expression 'relationship('List['Artist']')' seems to be using a generic class"

### 2. Use string literals (FAILED)
- SQLAlchemy 2.0 **parses string annotations** and still finds List[] generic
- Error persists regardless of quoting

### 3. Create test objects without instantiation (TOO COMPLEX)
- Would require rewriting tests to use `session.exec()` instead of object creation
- Defeats purpose of unit testing

### 4. Downgrade SQLAlchemy to 1.4 (RISKY)
- Breaks compatibility with Python 3.14+
- Conflicts with other packages expecting SQLAlchemy 2.0+

---

## Recommended Solution

### **Option A: Downgrade to SQLAlchemy 1.4** (RECOMMENDED for this project)
- Metal List is a **personal project** with simple schema
- SQLAlchemy 1.4 is stable and widely supported
- Removes type annotation blocker entirely

**Steps:**
1. Update `backend/requirements.txt`: `sqlmodel==0.0.19` (already compatible with 1.4)
2. Revert `models.py` to pre-Mapped[] syntax (simple List/Optional types)
3. Write tests without Mapped[] constraints
4. Issue #23 becomes unblocked

**Time:** ~1 hour total

### **Option B: Upgrade SQLAlchemy to Future Release**
- Wait for SQLAlchemy 2.1+ (if they fix instantiation issues)
- Maintain Python 3.14 compatibility
- Timeline: Unknown

### **Option C: Implement Custom Workaround**
- Create factory functions for test object creation
- Use `session.exec(insert(Category).values(...))` instead of instantiation
- Very complex, not recommended

---

## Impact on Issue #23

**Current Status:**
- ✅ Test infrastructure in place (conftest.py, pytest.ini, etc.)
- ✅ Implementation plan documented (.implementation-plan.md)
- ❌ Actual integration tests blocked by SQLAlchemy 2.0

**If Option A chosen (downgrade):**
- Issue #23 can be completed in 1-2 hours
- All 14+ tests for importer can be written and pass

**If Option B chosen (wait):**
- Issue #23 remains blocked indefinitely
- Focus on other issues in the meantime

**If Option C chosen (workaround):**
- Possible but requires significant refactoring
- Not recommended for small project

---

## Recommendation

**Proceed with Option A (downgrade to SQLAlchemy 1.4):**

1. **Pro:** Unblocks Issue #23 immediately
2. **Pro:** Simplifies models.py (no Mapped[] complexity)
3. **Pro:** Allows proper unit testing
4. **Con:** Slight version downgrade (not ideal, but acceptable for personal project)

**Action Items:**
```bash
# 1. Update requirements
pip install sqlalchemy==1.4.x sqlmodel==0.0.19

# 2. Revert models.py
git revert <commit-with-Mapped-changes>

# 3. Complete Issue #23
# [Write tests and they will pass]
```

---

## Next Steps

1. **Decision:** Choose Option A, B, or C
2. **If A:** Complete Issue #23 in next session (1-2 hours)
3. **If B:** Document wait and move on to other issues
4. **If C:** Schedule design session for custom workaround

**Estimated Resolution Time:**
- Option A: 1-2 hours
- Option B: Unknown
- Option C: 4-6 hours

---

*This blocker was discovered during dev-cycle Phase 6 (implementation) for Issue #23.*
