"""
Service xử lý nghiệp vụ sản phẩm.
"""
from sqlalchemy.orm import Session, joinedload

from models.product import Product
from models.product_category import ProductCategory
from schemas.product_schema import ProductCreate
from utils.exceptions import AppException


def get_all_products(db: Session):
    """Lấy toàn bộ sản phẩm kèm thông tin danh mục sản phẩm."""
    return (
        db.query(Product)
        .options(joinedload(Product.product_category))
        .order_by(Product.id)
        .all()
    )


def create_product(db: Session, payload: ProductCreate) -> Product:
    """Thêm mới sản phẩm: kiểm tra danh mục sản phẩm tồn tại và mã sản phẩm không bị trùng."""
    type_obj = db.get(ProductCategory, payload.product_category_id)
    if type_obj is None:
        raise AppException(
            404, "Not Found",
            f"Không tìm thấy danh mục sản phẩm có id = {payload.product_category_id}",
        )

    duplicated = db.query(Product).filter(Product.product_code == payload.product_code).first()
    if duplicated is not None:
        raise AppException(
            409, "Conflict",
            f"Mã sản phẩm {payload.product_code} đã tồn tại",
        )

    new_product = Product(**payload.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
