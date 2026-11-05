"""
Router API sản phẩm: GET /products, POST /products
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.product_schema import ProductCreate, ProductDetailResponse, ProductListResponse
from services import product_service

router = APIRouter(prefix="/products", tags=["Sản phẩm"])


@router.get("", response_model=ProductListResponse, status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    """API 2: Truy vấn danh sách sản phẩm kèm chi tiết danh mục sản phẩm."""
    items = product_service.get_all_products(db)
    return {
        "statusCode": 200,
        "error": None,
        "message": "Lấy danh sách sản phẩm thành công",
        "data": items,
    }


@router.post("", response_model=ProductDetailResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    """API 1: Thêm mới một sản phẩm."""
    new_item = product_service.create_product(db, payload)
    return {
        "statusCode": 201,
        "error": None,
        "message": "Thêm mới sản phẩm thành công",
        "data": new_item,
    }
