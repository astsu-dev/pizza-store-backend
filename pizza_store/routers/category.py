from fastapi import APIRouter, Depends, Response, status
from pizza_store import models
from pizza_store.dependencies.services import get_category_service
from pizza_store.services import ICategoryService

category_router = APIRouter(prefix="/category")
router = category_router


@router.get("", response_model=list[models.Category])
async def get_categories(service: ICategoryService = Depends(get_category_service)):
    return await service.get_categories()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=models.Category)
async def add_category(
    category_create: models.CategoryCreate,
    service: ICategoryService = Depends(get_category_service),
):
    return await service.add_category(category_create=category_create)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_category(
    category_id: int, service: ICategoryService = Depends(get_category_service)
):
    await service.delete_category(id=category_id)
