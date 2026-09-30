from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    Integer,
    Text,
)
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)
    location = Column(
        Enum("MSK", "SPB", name="Location"),
        nullable=False
    )
    published = Column(Boolean, nullable=False)
    rating = Column(Float, nullable=False)
    genre_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)