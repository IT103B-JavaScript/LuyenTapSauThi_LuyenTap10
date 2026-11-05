"""
Model bảng product_categories (danh mục sản phẩm) - phía "1" của quan hệ 1-N.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    # Một danh mục sản phẩm có nhiều sản phẩm
    products = relationship("Product", back_populates="product_category")
