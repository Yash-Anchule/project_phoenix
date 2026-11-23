from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import Expenses, MonthlyBudget
from app.schemas import MonthlyBudgetPydantic


def get_monthly_budget(month: int, year: int, db: Session):
    return db.query(MonthlyBudget).filter_by(month=month, year=year).first()


def add_monthly_budget(data: MonthlyBudgetPydantic, db: Session):
    existing = db.query(MonthlyBudget).filter_by(month=data.month, year=data.year).first()
    if existing is not None:
        return None

    budget = MonthlyBudget(
        month=data.month,
        year=data.year,
        monthly_budget=data.monthly_budget
    )
    db.add(budget)
    db.commit()
    return budget


def update_monthly_budget(data: MonthlyBudgetPydantic, db: Session):
    budget = db.query(MonthlyBudget).filter_by(month=data.month, year=data.year).first()
    if budget is None:
        return None

    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(budget, field, value)

    db.commit()
    return budget


def get_budget_status(month: int, year: int, db: Session):
    # 1. Fetch budget
    budget_row = db.query(MonthlyBudget).filter_by(month=month, year=year).first()
    if budget_row is None:
        return None

    budget = budget_row.monthly_budget

    # 2. Sum expenses for this month
    start_date = datetime(year, month, 1)
    end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)

    total_expenses = db.query(func.sum(Expenses.amount)).filter(
        Expenses.spent_at >= start_date,
        Expenses.spent_at < end_date
    ).scalar() or 0

    is_over = total_expenses > budget
    diff = abs(total_expenses - budget)

    return {
        "month": month,
        "year": year,
        "budget": budget,
        "expenses": total_expenses,
        "is_over_budget": is_over,
        "difference": diff,
        "status": f"Over Budget by {diff}" if is_over else (f"Under Budget by {diff}" if total_expenses < budget else "On Budget")
    }
