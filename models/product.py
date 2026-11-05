"""
Model bảng products (sản phẩm) - phía "N" của quan hệ 1-N.
"""
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_code = Column(String(10), unique=True, nullable=False)
    unit_price = Column(Float, nullable=False)
    product_category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=False)

    # Mỗi sản phẩm thuộc về một danh mục sản phẩm
    product_category = relationship("ProductCategory", back_populates="products")
