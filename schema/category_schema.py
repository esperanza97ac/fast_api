from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Name of the category",
        examples=["Postres", "Aperitivos", "Primeros", "Segundos"]
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Name of the category",
        examples=["Postres", "Aperitivos"]
    )


class CategoryResponse(CategoryBase):
    id: int = Field(..., description="PK database")

    model_config = ConfigDict(from_attributes=True)