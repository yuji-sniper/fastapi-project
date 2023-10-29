from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

db_user = "fastapi"
db_password = "password"
db_host = "mysql"
db_port = 3306
db_name = "fastapi"

db_url = URL.create(
    drivername="mysql+pymysql",
    username=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
    database=db_name
)

Engine = create_engine(str(db_url))

SessionLocal = scoped_session(
    sessionmaker(
        bind=Engine,
        autocommit=False,
        autoflush=True
    )
)

Base = declarative_base()

def get_url() -> str:
    return str(db_url)
