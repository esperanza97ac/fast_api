
from fastapi import APIRouter

from routes.recipe_routes import router as recipe_router
from routes.category_routes import router as category_router

router = APIRouter()
router.include_router(recipe_router)
router.include_router(category_router)