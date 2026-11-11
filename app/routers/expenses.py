from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Expenses
from app.schemas import ExpensePydantic

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@router.post("")
def add_expense(data: ExpensePydantic, db: Session = Depends(get_db)):
    expense = Expenses(
        amount=data.amount,
        category=data.category,
        spent_at=data.spent_at
    )
    db.add(expense)
    db.commit()
    return expense

@router.get("")
def all_expenses(db: Session = Depends(get_db)):
    return db.query(Expenses).all()

@router.get("/{id}")
def get_exact_expense(id: int, db: Session = Depends(get_db)):
    result = db.get(Expenses, id)
    if result is None:
        raise HTTPException(status_code=404, detail="The request Id doesn't exist!")
    return result

@router.put("/{id}")
def updating_expense(id: int, data: ExpensePydantic, db: Session = Depends(get_db)):
    result = db.get(Expenses, id)
    if result is None:
        raise HTTPException(status_code=404, detail="The request Id doesn't exist!")
    
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(result, field, value)
    
    db.commit()
    return result

@router.delete("/{id}")
def delete_expense(id: int, db: Session = Depends(get_db)):
    result = db.get(Expenses, id)
    if result is None:
        raise HTTPException(status_code=404, detail="The request Id doesn't exist!")
    
    db.delete(result)
    db.commit()
    return {"message": "Successfully Deleted"}