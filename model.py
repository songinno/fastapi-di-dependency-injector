from ulid import ULID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, Integer

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id: str = Column(String, primary_key=True, default=str(ULID()))
    name: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False)