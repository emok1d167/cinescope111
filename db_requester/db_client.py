from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.env_config import EnvConfig


USERNAME = EnvConfig.require("DB_MOVIES_USERNAME")
PASSWORD = EnvConfig.require("DB_MOVIES_PASSWORD")
HOST = EnvConfig.require("DB_MOVIES_HOST")
PORT = EnvConfig.require("DB_MOVIES_PORT")
DATABASE_NAME = EnvConfig.require("DB_MOVIES_NAME")


engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}",
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db_session():
    return SessionLocal()