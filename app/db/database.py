from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/personal_ai"

engine = create_engine(DATABASE_URL)

# postgresql+psycopg://postgres:postgres@localhost:5432/personal_ai
#        │        │       │        │        │
#        │        │       │        │        └── database
#        │        │       │        └────────── port
#        │        │       └────────────────── host
#        │        └────────────────────────── password
#        └────────────────────────────────── user/driver

