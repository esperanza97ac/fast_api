from sqlalchemy import Column, Integer, Text, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.database import Base

class Recipe(Base):

    __tablename__="recipes" 

    id = Column (Integer,primary_key=True, index=True,autoincrement=True)
    title = Column(String(100), nullable=False, index=True)
    ingredients = Column(Text, nullable=False, index=True)
    instructions = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False)
    category_id= Column(
        Integer, 
        ForeignKey("categorias.id", ondelete="CASCADE"),
        nullable=False)

    category = relationship("Category", back_populates="recipes")

    def __repr__(self):
        return (
            f"<Recipe(id={self.id}, title={self.title}, "
            f"ingredients={self.ingredients}, difficulty={self.difficulty}, "
            f"category_id={self.category_id})>"
        )