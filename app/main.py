from fastapi import FastAPI
from sqlalchemy import text
from db.database import engine

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Hello World"}


@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        value = result.scalar()
    
    return {"database" :value}

