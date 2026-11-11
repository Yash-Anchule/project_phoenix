from datetime import datetime
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Expenses

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/monthly-expenses/{month}/{year}")
def specific_month_expenses(
    month: int = Path(ge=1, le=12, description="Month must be between 1 and 12"),
    year: int = Path(ge=2026, le=9999),
    db: Session = Depends(get_db)
):
    start_date = datetime(year, month, 1)
    end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)

    result = db.query(func.sum(Expenses.amount)).filter(
        Expenses.spent_at >= start_date, 
        Expenses.spent_at < end_date
    ).scalar() or 0

    return {"month": month, "year": year, "total_expenses": result}

@router.get("/category-spending/{month}/{year}")
def category_spending(
    month: int = Path(ge=1, le=12, description="Month must be between 1 and 12"),
    year: int = Path(ge=2026, le=9999),
    sort_by_highest: bool = Query(True, description="Sort categories by highest spend first"),
    db: Session = Depends(get_db)
):
    start_date = datetime(year, month, 1)
    end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)

    total_amount = func.sum(Expenses.amount)
    query = (
        db.query(Expenses.category, total_amount)
        .filter(Expenses.spent_at >= start_date, Expenses.spent_at < end_date)
        .group_by(Expenses.category)
    )

    if sort_by_highest:
        query = query.order_by(total_amount.desc())
    else:
        query = query.order_by(Expenses.category.asc())

    result = query.all()
    return {
        "month": month,
        "year": year,
        "category_spending": [
            {"category": category, "total": total}
            for category, total in result
        ]
    }

@router.get("/top-expenses/{month}/{year}")
def top_expenses(
    month: int = Path(ge=1, le=12, description="Month must be between 1 and 12"),
    year: int = Path(ge=2026, le=9999),
    top_n: int = Query(5, ge=1, le=50, description="Number of top expenses to retrieve"),
    category: str | None = Query(None, description="Optional category to filter by"),
    db: Session = Depends(get_db)
):
    start_date = datetime(year, month, 1)
    end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)

    query = db.query(Expenses).filter(
        Expenses.spent_at >= start_date,
        Expenses.spent_at < end_date
    )

    if category:
        query = query.filter(Expenses.category == category)

    result = query.order_by(Expenses.amount.desc()).limit(top_n).all()

    return {
        "month": month,
        "year": year,
        "category": category,
        "count": len(result),
        "expenses": result
    }