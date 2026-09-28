
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from model.recipe_model import Recipe
from schema.recipe_schema import RecipeCreate, RecipeUpdate


def get_recipes(db: Session, skip: int = 0, limit: int = 100) -> list[Recipe]:
    try:
        return db.query(Recipe).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error fetching recipes: {error}",
        ) from error


def get_by_id(db: Session, recipe_id: int) -> Recipe | None:
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()


def get_recipes_by_category(
    db: Session, category_id: int, skip: int = 0, limit: int = 100
) -> list[Recipe]:
    return (
        db.query(Recipe)
        .filter(Recipe.category_id == category_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def search_recipes(
    db: Session, q: str, skip: int = 0, limit: int = 100
) -> list[Recipe]:
    pattern = f"%{q}%"
    return (
        db.query(Recipe)
        .filter(Recipe.title.ilike(pattern) | Recipe.ingredients.ilike(pattern))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_recipe(db: Session, recipe_data: RecipeCreate) -> Recipe:
    new_recipe = Recipe(
        title=recipe_data.title,
        ingredients=recipe_data.ingredients,
        instructions=recipe_data.instructions,
        difficulty=recipe_data.difficulty,
        category_id=recipe_data.category_id,
    )
    try:
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
        return new_recipe
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Recipe violates a database constraint.",
        ) from error
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error creating recipe: {error}",
        ) from error


def update_recipe(
    db: Session, recipe_id: int, recipe_data: RecipeUpdate
) -> Recipe | None:
    db_recipe = get_by_id(db, recipe_id)
    if not db_recipe:
        return None

    update_data = recipe_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_recipe, field, value)

    try:
        db.commit()
        db.refresh(db_recipe)
        return db_recipe
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Recipe violates a database constraint.",
        ) from error
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error updating recipe: {error}",
        ) from error


def delete_recipe(db: Session, recipe_id: int) -> Recipe | None:
    db_recipe = get_by_id(db, recipe_id)
    if not db_recipe:
        return None
    try:
        db.delete(db_recipe)
        db.commit()
        return db_recipe
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error deleting recipe: {error}",
        ) from error