import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg://{username}:{password}" f"@{host}:{port}/{database}"
)

engine = create_engine(DATABASE_URL)

# sessionmaker is factory that creates SQLAlchemy session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(
    DeclarativeBase
):  # we use DeclarativeBase as the foundation for our ORM models.
    pass
