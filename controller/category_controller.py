from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException, status

from model.category_model import Category
from schema.category_schema import CategoryCreate, CategoryUpdate


def get_categories(db: Session, skip: int = 0, limit: int = 100) -> list[Category]:
    return db.query(Category).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name(db: Session, name: str) -> Category | None:
    return db.query(Category).filter(Category.name == name).first()


def create_category(db: Session, category: CategoryCreate) -> Category:
    new_category = Category(name=category.name)
    if get_category_by_name(db, category.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category name '{category.name}' already exists",
        )
    try:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category name '{category.name}' already exists",
        ) from error
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error creating category: {error}"
        ) from error
    

def update_category(db: Session, category_id: int, category: CategoryUpdate) -> Category | None:
    db_category = get_category(db, category_id)
    if not db_category:
        return None

    existing = get_category_by_name(db, category.name)
    if existing and existing.id != category_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category name '{category.name}' already exists"
        )

    db_category.name = category.name
    try:
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category name '{category.name}' already exists",
        ) from error
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error updating category: {error}"
        ) from error


def delete_category(db: Session, category_id: int) -> Category | None:
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    try:
        db.delete(db_category)
        db.commit()
        return db_category
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Cannot delete category '{db_category.name}' because it "
                "still has related recipes."
            ),
        ) from error
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error deleting category: {error}"
        ) from error