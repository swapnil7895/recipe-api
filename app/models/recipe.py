from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=True)
    description = Column(Integer, nullable=False)
    cooking_time_minutes = Column(Integer, nullable=False)
    instructions = Column(Text, nullable=False)
