import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

CONTAINER_MODE = os.environ.get('CONTAINER_MODE')

DB_URL = (f"postgresql+psycopg2://"
          f"{os.environ.get('POSTGRES_USER') if CONTAINER_MODE else 'pguser'}:"
          f"{os.environ.get('POSTGRES_PASSWORD') if CONTAINER_MODE else 'pgpass'}@"
          f"{'pgdb' if CONTAINER_MODE else 'localhost'}:"
          f"5432/"
          f"postgres")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
