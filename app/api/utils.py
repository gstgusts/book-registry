# app/api/utils.py
from sqlalchemy.inspection import inspect


def model_to_dict(obj):
    """Serialize SQLAlchemy model columns to a dict (simple & safe)."""
    data = {}
    mapper = inspect(obj).mapper
    for col in mapper.column_attrs:
        val = getattr(obj, col.key)
        # handle date/datetime via isoformat if available
        if hasattr(val, "isoformat"):
            val = val.isoformat()
        data[col.key] = val
    return data


def paginate_query(query, page: int, per_page: int):
    """Return items + meta for simple pagination."""
    page = max(page, 1)
    per_page = min(max(per_page, 1), 100)
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    total = query.order_by(None).count()  # avoid count(*) with ORDER BY
    return items, {
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total + per_page - 1) // per_page if per_page else 0,
    }
