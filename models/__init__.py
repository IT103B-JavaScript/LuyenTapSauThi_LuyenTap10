"""Gom các model để SQLAlchemy nhận diện đầy đủ quan hệ khi tạo bảng."""
from models.product_category import ProductCategory
from models.product import Product

__all__ = ["ProductCategory", "Product"]
