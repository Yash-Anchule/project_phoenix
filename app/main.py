from fastapi import FastAPI , Depends
from sqlalchemy import text
from app.db.database import engine,get_db

app = FastAPI()


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

