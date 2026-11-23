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
