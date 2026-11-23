from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Expenses
from app.schemas import ExpensePydantic
from app.services import expense_services 
router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@router.post("")
def add_expense(data: ExpensePydantic, db: Session = Depends(get_db)):
    # expense = Expenses(
    #     amount=data.amount,
    #     category=data.category,
    #     spent_at=data.spent_at
    # )
    # db.add(expense)
    # db.commit()
    # return expense
    return expense_services.add_expense(data, db)

@router.get("")
def all_expenses(db: Session = Depends(get_db)):
    return expense_services.all_expenses(db)

@router.get("/{id}")
def get_exact_expense(id: int, db: Session = Depends(get_db)):
    expense = expense_services.get_expense_by_id(id, db)
    if expense is None:
        raise HTTPException(status_code=404, detail="The requested Id doesn't exist!")
    return expense

@router.put("/{id}")
def updating_expense(id: int, data: ExpensePydantic, db: Session = Depends(get_db)):
    # result = db.get(Expenses, id)
    # if result is None:
    #     raise HTTPException(status_code=404, detail="The request Id doesn't exist!")
    
    # updates = data.model_dump(exclude_unset=True)
    # for field, value in updates.items():
    #     setattr(result, field, value)
    
    # db.commit()
    # return result
    expense = expense_services.update_expense(id, data, db)
    if expense is None:
        raise HTTPException(status_code=404, detail="The requested Id doesn't exist!")
    return expense

@router.delete("/{id}")
def delete_expense(id: int, db: Session = Depends(get_db)):
    # result = db.get(Expenses, id)
    # if result is None:
    #     raise HTTPException(status_code=404, detail="The request Id doesn't exist!")
    
    # db.delete(result)
    # db.commit()
    # return {"message": "Successfully Deleted"}
    success = expense_services.delete_expense(id, db)
    if not success:
        raise HTTPException(status_code=404, detail="The requested Id doesn't exist!")
    return {"message": "Successfully Deleted"}