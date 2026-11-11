from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Expenses, MonthlyBudget
from app.schemas import MonthlyBudgetPydantic

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)

@router.get("/{month}/{year}")
def get_monthly_budget(
    month: int = Path(ge=1, le=12, description="Month must be between 1 and 12"),
    year: int = Path(ge=2026, le=9999),
    db: Session = Depends(get_db)
):
    result = db.query(MonthlyBudget).filter_by(month=month, year=year).first()
    if result is None:
        raise HTTPException(status_code=404, detail="The budget for the requested month and year doesn't exist!")
    return result

@router.post("")
def add_monthly_budget(data: MonthlyBudgetPydantic, db: Session = Depends(get_db)):
    result = db.query(MonthlyBudget).filter_by(month=data.month, year=data.year).first()
    if result is not None:
        raise HTTPException(status_code=409, detail="The budget for the requested month and year already exists!")

    budget = MonthlyBudget(
        month=data.month,
        year=data.year,
        monthly_budget=data.monthly_budget
    )
    db.add(budget)
    db.commit()
    return {"message": "Successfully Added!"}

@router.put("")
def update_monthly_budget(data: MonthlyBudgetPydantic, db: Session = Depends(get_db)):
    result = db.query(MonthlyBudget).filter_by(month=data.month, year=data.year).first()
    if result is None:
        raise HTTPException(status_code=404, detail="The budget for the requested month and year doesn't exist!")

    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(result, field, value)
    
    db.commit()
    return {"message": "Successfully Updated!"}

@router.get("/{month}/{year}/status")
def budget_status(
    month: int = Path(ge=1, le=12, description="Month must be between 1 and 12"),
    year: int = Path(ge=2026, le=9999),
    db: Session = Depends(get_db)
):
    # 1. Fetch budget
    budget_row = db.query(MonthlyBudget).filter_by(month=month, year=year).first()
    if budget_row is None:
        raise HTTPException(status_code=404, detail="No budget set for this month and year!")
    budget = budget_row.monthly_budget

    # 2. Calculate expenses for this month
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