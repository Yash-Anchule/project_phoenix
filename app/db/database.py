from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/personal_ai"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def get_db():

    db = SessionLocal() 
    # se we r just making sesion using the connection of the engine we had earlier and not just insitlasing 
    # but also we will be closing this respectively !!This might help us a lot 
    try:
        yield db
    finally:
        db.close()
# postgresql+psycopg://postgres:postgres@localhost:5432/personal_ai
#        │        │       │        │        │
#        │        │       │        │        └── database
#        │        │       │        └────────── port
#        │        │       └────────────────── host
#        │        └────────────────────────── password
#        └────────────────────────────────── user/driver