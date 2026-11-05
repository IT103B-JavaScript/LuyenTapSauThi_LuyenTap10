"""
Schemas Pydantic: validate dữ liệu đầu vào và định nghĩa cấu trúc dữ liệu đầu ra.
"""
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductCategoryResponse(BaseModel):
    """Thông tin danh mục sản phẩm trả về kèm trong sản phẩm."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ProductCreate(BaseModel):
    """Dữ liệu đầu vào khi thêm mới sản phẩm."""
    product_code: str = Field(..., min_length=4, max_length=10, examples=["P3001"])
    unit_price: float = Field(..., gt=0, examples=[15000000])
    product_category_id: int = Field(..., examples=[1])

    @field_validator("product_code")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        """Bỏ khoảng trắng hai đầu, chuyển in hoa và kiểm tra lại độ dài."""
        value = value.strip().upper()
        if len(value) < 4:
            raise ValueError("Mã sản phẩm phải có ít nhất 4 ký tự")
        return value


class ProductResponse(BaseModel):
    """Thông tin sản phẩm trả về (dùng làm response_model)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_code: str
    unit_price: float
    product_category: ProductCategoryResponse


class ProductListResponse(BaseModel):
    """Response chuẩn cho API lấy danh sách sản phẩm."""
    statusCode: int
    error: Optional[str] = None
    message: str
    data: List[ProductResponse]


class ProductDetailResponse(BaseModel):
    """Response chuẩn cho API trả về một sản phẩm."""
    statusCode: int
    error: Optional[str] = None
    message: str
    data: ProductResponse


class ProductCategoryDeleteResponse(BaseModel):
    """Response chuẩn cho API xóa danh mục sản phẩm."""
    statusCode: int
    error: Optional[str] = None
    message: str
    data: Optional[ProductCategoryResponse] = None
