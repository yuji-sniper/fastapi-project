from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, scoped_session

db_user = config('DB_USER')
db_password = config('DB_PASSWORD')
db_host = config('DB_HOST')
db_port = config('DB_PORT')
db_name = config('DB_NAME')

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

def get_url() -> str:
    return str(db_url)
