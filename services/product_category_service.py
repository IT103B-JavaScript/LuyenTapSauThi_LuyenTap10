"""
Service xử lý nghiệp vụ danh mục sản phẩm.
"""
from sqlalchemy.orm import Session

from models.product import Product
from models.product_category import ProductCategory
from utils.exceptions import AppException

DEFAULT_PRODUCT_CATEGORIES = ["electronics", "furniture", "stationery"]


def seed_default_product_categories(db: Session) -> None:
    """Tạo sẵn các danh mục sản phẩm mặc định nếu bảng đang trống (phục vụ test API)."""
    if db.query(ProductCategory).count() > 0:
        return
    for type_name in DEFAULT_PRODUCT_CATEGORIES:
        db.add(ProductCategory(name=type_name))
    db.commit()


def delete_product_category(db: Session, type_id: int) -> ProductCategory:
    """Xóa danh mục sản phẩm theo id, chỉ cho phép khi không còn sản phẩm nào thuộc loại này."""
    type_obj = db.get(ProductCategory, type_id)
    if type_obj is None:
        raise AppException(404, "Not Found", f"Không tìm thấy danh mục sản phẩm có id = {type_id}")

    total_products = db.query(Product).filter(Product.product_category_id == type_id).count()
    if total_products > 0:
        raise AppException(
            400, "Bad Request",
            f"Không thể xóa danh mục sản phẩm '{type_obj.name}' vì còn {total_products} sản phẩm thuộc loại này",
        )

    db.delete(type_obj)
    db.commit()
    return type_obj
