from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import Expenses


def get_monthly_expenses(month: int, year: int, db: Session):
    start_date = datetime(year, month, 1)
    end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)

    result = db.query(func.sum(Expenses.amount)).filter(
        Expenses.spent_at >= start_date,
        Expenses.spent_at < end_date
    ).scalar() or 0

    return {"month": month, "year": year, "total_expenses": result}


def get_category_spending(month: int, year: int, sort_by_highest: bool, db: Session):
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


def get_top_expenses(month: int, year: int, top_n: int, category: str | None, db: Session):
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
