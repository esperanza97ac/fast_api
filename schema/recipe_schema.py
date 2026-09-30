from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from schema.category_schema import CategoryResponse

class RecipeBase(BaseModel):

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Title Recipe",
        examples=["Tarta de queso"]
    )

    ingredients: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Ingredients Recipe",
        examples=["600g Queso crema, 200g leche condensada, 4 huevos (tamaño L)"]
    )

    instructions: str = Field(
        ...,
        min_length=1,
        description="Instructions to prepare the recipe",
        examples=[
            "1. Precalienta el horno a 190 ºC\n"
            "2. Bate los huevos\n"
            "3. Añade la leche condensada y el queso crema\n"
            "4. Bate hasta que no queden grumos\n"
            "5. Hornea durante 50 min\n"
            "6. Enfría a temperatura ambiente y guarda en la nevera."
        ]
    )

    difficulty: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Difficulty level of the recipe",
        examples=["Fácil", "Medio", "Difícil"]
    )

    category_id: int = Field(
        ...,
        ge=1,
        description="Recipe category ID",
        examples=[1]
    )


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    ingredients: Optional[str] = Field(None, min_length=1, max_length=500)
    instructions: Optional[str] = Field(None, min_length=1)
    difficulty: Optional[str] = Field(None, min_length=1, max_length=20)
    category_id: Optional[int] = Field(None, ge=1)


class RecipeResponse(RecipeBase):
    id: int = Field(..., description="PK database")
    category: CategoryResponse = Field(
        ...,
        description="Category the recipe belongs to",
    )

    model_config = ConfigDict(from_attributes=True)