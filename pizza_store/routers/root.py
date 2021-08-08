from fastapi import APIRouter
from pizza_store.routers.auth import auth_router
from pizza_store.routers.category import category_router
from pizza_store.routers.product import product_router

router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(category_router)
router.include_router(product_router)
