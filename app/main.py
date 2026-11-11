from calendar import month
import string
from unittest import result
from app.routers import expenses
from app import db
from sqlalchemy import delete, func
from pydantic import ValidationError
from fastapi import HTTPException, Path, Query
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_404_NOT_FOUND
from sqlalchemy import null
from sqlalchemy import select
from fastapi import FastAPI , Depends
from sqlalchemy import text
from datetime import datetime
from app.db.database import engine,get_db
from app.db.models import Base, Expenses, MonthlyBudget
from app.schemas import ExpensePydantic, MonthlyBudgetPydantic
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routers import budgets
from app.routers import analytics




app = FastAPI(title="Phonix Expense Tracker", description="A simple expense tracker API built with FastAPI and SQLAlchemy", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(expenses.router)
app.include_router(budgets.router)
app.include_router(analytics.router)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

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


# @app.post("/expenses")
# def add_expense(data:ExpensePydantic ,db = Depends(get_db)):

#     # print(RequestValidationError)

#         expense = Expenses(
#             amount=data.amount,
#             category=data.category,
#             spent_at=data.spent_at 
#         )
#         db.add(expense)
#         db.commit()

#         return expense
#     # except ValidationError as e:
#     #     print(e.errors())
#     #     return e.errors()
#     # try:
# #     res = ExpensePydantic(**raw)
# #     print(res)
# #     print(res.model_fields_set)
# # except ValidationError as e:
# #     print(e.errors())


# @app.get("/expenses")
# def all_expenses(db = Depends(get_db)):

#     result = db.query(Expenses).all()
#     # print(result)

#     # statement = select(Expenses)

#     # # list of ``User`` objects
#     # user_obj = db.scalars(statement).all()
#     # print(user_obj)

#     return result


# @app.get("/expenses/{id}")
# def get_exact_expense(id:int , db = Depends(get_db)):
#     result = db.get(Expenses, id)

#     if(result is None):
#         raise HTTPException(status_code=404,detail="The request Id doesnt Exist!")
    
#     return result


# @app.put("/expenses/{id}")
# def updating_expense(id:int, data:ExpensePydantic , db = Depends(get_db)):       
#     result = db.get(Expenses, id)
    
#     try :
    
#         updates = data.model_dump(exclude_unset=True)
        
#         print(data.model_dump())
#         print(data.model_fields_set)
#         # setattr(expense, field, value)
#         # print(updates)
#         for field,value in updates.items():
#             # print(field)
#             # print(value)
#             setattr(result,field,value)
        
#         db.commit()
#     except ValidationError as e:
#         print(e.errors())
#         return e.errors()

#     return result



# @app.delete("/expenses/{id}")
# def delete_expense(id:int,db = Depends(get_db)):
#     result = db.get(Expenses, id)

#     if(result is None):
#         raise HTTPException(status_code=404,detail="The request Id doesnt Exist!")
    
#     db.delete(result)
#     db.commit()
#     return {"messsgae" : "Successfully Deleted"}



# @app.get("/budgets/{month}/{year}")
# def get_monthly_budget(month: int = Path(ge=1, le=12, description="Month must be between 1 and 12"),
#     year: int = Path(ge=2026, le=9999),db = Depends(get_db)):
#         result = db.query(MonthlyBudget).filter_by(month=month, year=year).first()
    
#         if(result is None):
#             raise HTTPException(status_code=404,detail="The Buget for the request Month and Year doesnt Exist!")
    
#         return result


# @app.post("/budgets")
# def add_monthly_budget(data:MonthlyBudgetPydantic,db = Depends(get_db)):

    
#     result = db.query(MonthlyBudget).filter_by(month=data.month, year=data.year).first()

#     if(result is not None):
#         raise HTTPException(status_code=409,detail="The Buget for the request Month and Year already Exist!")

#     bugdet = MonthlyBudget(
#         month=data.month,
#         year=data.year,
#         monthly_budget=data.monthly_budget
#     )
#     db.add(bugdet)
#     db.commit()
#     return {"message" : "Successfully Added!"}


# @app.put("/budgets")
# def update_monthly_budget(data:MonthlyBudgetPydantic,db = Depends(get_db)):

#     result = db.query(MonthlyBudget).filter_by(month=data.month, year=data.year).first()

#     if(result is None):
#         raise HTTPException(status_code=404,detail="The Buget for the request Month and Year doesnt Exist!")

#     updates = data.model_dump(exclude_unset=True)
        
#     print(data.model_dump())
#     print(data.model_fields_set)
#     # setattr(expense, field, value)
#     # print(updates)
#     for field,value in updates.items():
#         # print(field)
#         # print(value)
#         setattr(result,field,value)
    
#     db.commit()

#     return {"message" : "Successfully Updated!"}


# @app.get("/analytics/monthly-expenses/{month}/{year}")
# def specific_month_expenses(month: int = Path(ge=1, le=12, description="Month must be between 1 and 12"),
#     year: int = Path(ge=2026, le=9999),db = Depends(get_db)):

#     start_date = datetime(year, month, 1)
#     if month == 12:
#         end_date = datetime(year + 1, 1, 1)
#     else:
#         end_date = datetime(year, month + 1, 1)

#     result = db.query(func.sum(Expenses.amount)).filter(Expenses.spent_at >= start_date, Expenses.spent_at < end_date).scalar() or 0

#     return {"month": month, "year": year, "total_expenses": result or 0}

# @app.get("/budgets/{month}/{year}/status")
# def budget_status(month: int = Path(ge=1, le=12, description="Month must be between 1 and 12"),
#     year: int = Path(ge=2026, le=9999),db = Depends(get_db)):

#     result  = get_monthly_budget(month,year,db)
#     budget = result.monthly_budget
#     result2 = specific_month_expenses(month,year,db)
#     expenses = result2["total_expenses"]

#     is_over = expenses > budget
#     diff = abs(expenses - budget)

#     return {
#     "month": month,
#     "year": year,
#     "budget": budget,
#     "expenses": expenses,
#     "is_over_budget": is_over,
#     "difference": diff,
#     "status": f"Over Budget by {diff}" if is_over else (f"Under Budget by {diff}" if expenses < budget else "On Budget")
#     }

# @app.get("/analytics/category-spending/{month}/{year}")
# def category_spending(month: int = Path(ge=1, le=12, description="Month must be between 1 and 12"),
#     year: int = Path(ge=2026, le=9999),sort_by_highest: bool = Query(True, description="Sort categories by highest spend first"),db = Depends(get_db)):

#     start_date = datetime(year, month, 1)
#     if month == 12:
#         end_date = datetime(year + 1, 1, 1)
#     else:
#         end_date = datetime(year, month + 1, 1)

#     # result = db.query(Expenses.category, func.sum(Expenses.amount)).filter(Expenses.spent_at >= start_date, Expenses.spent_at < end_date).group_by(Expenses.category).all()
    
#     total_amount = func.sum(Expenses.amount)
#     query = (
#     db.query(Expenses.category, total_amount)
#     .filter(Expenses.spent_at >= start_date, Expenses.spent_at < end_date)
#     .group_by(Expenses.category)
#     )
# # Apply sorting based on the query parameter:
#     if sort_by_highest:
#         query = query.order_by(total_amount.desc())
#     else:
#          query = query.order_by(Expenses.category.asc())  # alphabetical order!


#     result = query.all()
#     # print(result)
#     return {
#     "month": month,
#     "year": year,
#     "category_spending": [
#         {"category": category, "total": total}
#         for category, total in result
#     ]
# }



# @app.get("/analytics/top-expenses/{month}/{year}")
# def top_expenses(
#     month: int = Path(ge=1, le=12, description="Month must be between 1 and 12"),
#     year: int = Path(ge=2026, le=9999),
#     top_n: int = Query(5, ge=1, le=50, description="Number of top expenses to retrieve"),
#     category: str | None = Query(None, description="Optional category to filter by"),
#     db = Depends(get_db)
# ):
#     start_date = datetime(year, month, 1)
#     if month == 12:
#         end_date = datetime(year + 1, 1, 1)
#     else:
#         end_date = datetime(year, month + 1, 1)

#     query = db.query(Expenses).filter(
#         Expenses.spent_at >= start_date,
#         Expenses.spent_at < end_date
#     )

#     if category:
#         query = query.filter(Expenses.category == category)

#     result = query.order_by(Expenses.amount.desc()).limit(top_n).all()

#     return {
#         "month": month,
#         "year": year,
#         "category": category,
#         "count": len(result),
#         "expenses": result
#     }

