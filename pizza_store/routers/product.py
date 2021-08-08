from fastapi import APIRouter, Depends, File, Form, Response, UploadFile, status
from pizza_store import models
from pizza_store.dependencies.services import get_product_service
from pizza_store.enums.permissions import ProductPermission
from pizza_store.services import AuthService, IProductService

product_router = APIRouter(prefix="/product")
router = product_router


@router.get("", response_model=list[models.Product])
async def get_products(
    service: IProductService = Depends(get_product_service),
):
    return await service.get_products()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=models.Product)
async def add_product(
    name: str = Form(...),
    category_id: int = Form(...),
    weight: int = Form(...),
    price: int = Form(...),
    image: UploadFile = File(...),
    service: IProductService = Depends(get_product_service),
    _: models.UserInToken = Depends(
        AuthService.get_current_user(required_permissions=(ProductPermission.CREATE,))
    ),
):
    product_create = models.ProductCreate(
        name=name, category_id=category_id, weight=weight, price=price, image=image
    )
    return await service.add_product(product_create=product_create)


@router.delete(
    "/{product_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
async def delete_product(
    product_id: int,
    service: IProductService = Depends(get_product_service),
    _: models.UserInToken = Depends(
        AuthService.get_current_user(required_permissions=(ProductPermission.DELETE,))
    ),
):
    await service.delete_product(product_id=product_id)
