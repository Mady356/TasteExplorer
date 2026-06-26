# SQLAlchemy Reserved Attribute Fix

## Problem

SQLAlchemy crashed with:
```
sqlalchemy.exc.InvalidRequestError: Attribute name 'metadata' is reserved when using the Declarative API.
```

The issue occurred because two database models used `metadata` as a column name, which conflicts with SQLAlchemy's internal `Base.metadata` attribute.

---

## Solution

Renamed the column attributes while preserving the database column names:

### 1. Recommendation Model

**Before:**
```python
metadata = Column(JSON, nullable=True)
```

**After:**
```python
recommendation_metadata = Column("metadata", JSON, nullable=True)
```

### 2. TasteCluster Model

**Before:**
```python
metadata = Column(JSON, nullable=True)
```

**After:**
```python
cluster_metadata = Column("metadata", JSON, nullable=True)
```

---

## Changes Made

### Files Modified

1. **`apps/api/database/models.py`**
   - Line 324: `Recommendation.metadata` → `Recommendation.recommendation_metadata`
   - Line 359: `TasteCluster.metadata` → `TasteCluster.cluster_metadata`

2. **`apps/api/user/routes.py`**
   - Line 400: `rec.metadata` → `rec.recommendation_metadata`
   - Line 414: `rec.metadata` → `rec.recommendation_metadata`

---

## Database Impact

**None!** The database column names remain `metadata` thanks to the column name parameter:

```python
recommendation_metadata = Column("metadata", JSON, nullable=True)
                                  ^^^^^^^^
                                  DB column name stays "metadata"
```

This means:
- ✅ No database migration required
- ✅ Existing data unaffected
- ✅ API responses still use `"metadata"` as the field name

---

## Python Code Impact

All Python code now uses the new attribute names:

```python
# OLD (broken)
rec.metadata

# NEW (working)
rec.recommendation_metadata
```

API responses maintain compatibility:
```python
RecommendationResponse(
    ...
    metadata=rec.recommendation_metadata  # API response field is still "metadata"
)
```

---

## Verification

### 1. Compilation Check
```bash
cd apps/api
python -m compileall .
```
✅ All files compile without syntax errors

### 2. Import Check
```python
from database.models import Recommendation, TasteCluster, Base
print(Recommendation.recommendation_metadata)  # Works!
print(TasteCluster.cluster_metadata)            # Works!
```
✅ Models import successfully

### 3. Start Server
```bash
cd apps/api
uvicorn main:app --reload --port 8001
```
✅ Server should start without SQLAlchemy errors

---

## Why This Works

SQLAlchemy uses two different concepts:

1. **Python Attribute Name** - Used in Python code: `rec.recommendation_metadata`
2. **Database Column Name** - Used in SQL: `metadata`

By specifying the column name explicitly, we can use different names:

```python
# Python attribute          DB column
recommendation_metadata = Column("metadata", JSON, nullable=True)
```

This pattern is common for avoiding reserved words:
- `type_` for SQL `type` keyword
- `from_` for SQL `from` keyword
- `recommendation_metadata` for SQLAlchemy's reserved `metadata`

---

## Testing After Fix

### 1. Check Database Initialization
```python
from database.database import init_db
init_db()  # Should create all tables without errors
```

### 2. Create Test Records
```python
from database.models import Recommendation
from database.database import SessionLocal

db = SessionLocal()
rec = Recommendation(
    user_id=user_id,
    recommendation_type="artist",
    score=0.95,
    rank=1,
    recommendation_metadata={"cluster_id": "indie_rock"}
)
db.add(rec)
db.commit()

# Verify
print(rec.recommendation_metadata)  # {'cluster_id': 'indie_rock'}
```

### 3. Query Records
```python
rec = db.query(Recommendation).first()
print(rec.recommendation_metadata)  # Works!
```

---

## Summary

✅ **Fixed:** SQLAlchemy reserved attribute error  
✅ **Database:** No migration needed (column names unchanged)  
✅ **API:** Response format unchanged  
✅ **Code:** All references updated  
✅ **Tests:** Compilation and imports verified  

**Backend should now start successfully!** 🎉

---

## Command to Start Backend

```bash
cd apps/api
uvicorn main:app --reload --port 8001
```

Expected output:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

No more `InvalidRequestError: Attribute name 'metadata' is reserved`! ✅
