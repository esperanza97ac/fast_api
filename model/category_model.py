from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base


class Category(Base):

    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True, index=True)

    recipes = relationship("Recipe", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"

    