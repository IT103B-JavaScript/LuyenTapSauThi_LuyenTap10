"""
main.py - Điểm khởi chạy ứng dụng warehouse_management.
Chạy: uvicorn main:app --reload  ->  Swagger UI: http://127.0.0.1:8000/docs
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

import models  # noqa: F401  (đăng ký model trước khi tạo bảng)
from database import Base, SessionLocal, engine
from routers import product_router, product_category_router
from services.product_category_service import seed_default_product_categories
from utils.exceptions import AppException
from utils.response import build_response


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Tạo bảng và dữ liệu danh mục sản phẩm mặc định khi khởi động."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_default_product_categories(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Quản lý Kho hàng API", lifespan=lifespan)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Trả lỗi nghiệp vụ (404, 409, 400) theo cấu trúc response chung."""
    return build_response(exc.status_code, exc.message, data=None, error=exc.error)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Trả lỗi validate dữ liệu đầu vào (422) theo cấu trúc response chung."""
    details = [
        {"field": ".".join(str(loc) for loc in err["loc"][1:]), "detail": err["msg"]}
        for err in exc.errors()
    ]
    return build_response(422, "Dữ liệu đầu vào không hợp lệ", data=details, error="Unprocessable Entity")


app.include_router(product_router.router)
app.include_router(product_category_router.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Quản lý Kho hàng API đang chạy. Truy cập /docs để test API."}
