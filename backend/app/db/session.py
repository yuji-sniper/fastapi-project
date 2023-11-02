from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, scoped_session


db_url = URL.create(
    drivername="mysql+pymysql",
    username=config('DB_USER'),
    password=config('DB_PASSWORD'),
    host=config('DB_HOST'),
    port=config('DB_PORT'),
    database=config('DB_NAME')
)

Engine = create_engine(db_url)

SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=Engine
    )
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
