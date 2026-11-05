"""
Router API danh mục sản phẩm: DELETE /product-categories/{id}
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.product_schema import ProductCategoryDeleteResponse
from services import product_category_service

router = APIRouter(prefix="/product-categories", tags=["Danh mục sản phẩm"])


@router.delete("/{id}", response_model=ProductCategoryDeleteResponse, status_code=status.HTTP_200_OK)
def delete_product_category(id: int, db: Session = Depends(get_db)):
    """API 3: Xóa danh mục sản phẩm theo ID (chỉ khi không còn sản phẩm thuộc loại này)."""
    deleted = product_category_service.delete_product_category(db, id)
    return {
        "statusCode": 200,
        "error": None,
        "message": f"Xóa danh mục sản phẩm '{deleted.name}' thành công",
        "data": deleted,
    }
