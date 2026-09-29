from app import db
from sqlalchemy import delete
from pydantic import ValidationError
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from sqlalchemy import null
from sqlalchemy import select
from fastapi import FastAPI , Depends
from sqlalchemy import text
from datetime import datetime
from app.db.database import engine,get_db
from app.db.models import Base, Expenses
from app.schemas import ExpensePydantic
app = FastAPI()

Base.metadata.create_all(bind=engine) 
@app.get("/")
async def root():
    return {"message" : "Hello World"}


@app.get("/session_test")
def session_test(db = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    value = result.scalar()
    return {"database" :value}


@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        value = result.scalar()
    
    return {"database" :value}


@app.post("/add_test")
def add_expense(data:ExpensePydantic ,db = Depends(get_db)):
    expense = Expenses(
        amount=data.amount,
        category=data.category,
        spent_at=data.spent_at
    )
    db.add(expense)
    db.commit()

    return expense


@app.get("/all_expenses")
def all_expenses(db = Depends(get_db)):

    result = db.query(Expenses).all()
    # print(result)

    # statement = select(Expenses)

    # # list of ``User`` objects
    # user_obj = db.scalars(statement).all()
    # print(user_obj)

    return result


@app.get("/get_expense_id/{id}")
def get_exact_expense(id:int , db = Depends(get_db)):
    result = db.get(Expenses, id)

    if(result is None):
        raise HTTPException(status_code=404,detail="The request Id doesnt Exist!")
    
    return result


@app.put("/update/{id}")
def updating_expense(id:int, data:ExpensePydantic , db = Depends(get_db)):       
    result = db.get(Expenses, id)
    
    try :
    
        updates = data.model_dump(exclude_unset=True)
        
        print(data.model_dump())
        print(data.model_fields_set)
        # setattr(expense, field, value)
        # print(updates)
        for field,value in updates.items():
            # print(field)
            # print(value)
            setattr(result,field,value)
        
        db.commit()
    except ValidationError as e:
        print(e.errors())
        return e.errors()

    return result



@app.delete("/delete/{id}")
def delete_expense(id:int,db = Depends(get_db)):
    result = db.get(Expenses, id)

    if(result is None):
        raise HTTPException(status_code=404,detail="The request Id doesnt Exist!")
    
    db.delete(result)
    db.commit()
    return {"messsgae" : "Successfully Deleted"}

