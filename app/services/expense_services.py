# from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Expenses
from app.schemas import ExpensePydantic



def add_expense(data: ExpensePydantic, db: Session):
    expense = Expenses(
        amount=data.amount,
        category=data.category,
        spent_at=data.spent_at
    )
    db.add(expense)
    db.commit()
    return expense



def all_expenses(db: Session):
    return db.query(Expenses).all()



def get_expense_by_id(expense_id: int, db: Session):
    return db.get(Expenses, expense_id)



def update_expense(expense_id: int, data: ExpensePydantic, db: Session):
    expense = db.get(Expenses, expense_id)
    if expense is None:
        return None
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(expense, field, value)
    db.commit()
    return expense

def delete_expense(expense_id: int, db: Session):
    expense = db.get(Expenses, expense_id)
    if expense is None:
        return None
    db.delete(expense)
    db.commit()
    return True