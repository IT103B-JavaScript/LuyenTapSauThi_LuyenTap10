"""
Hàm tạo response theo quy chuẩn chung: statusCode, error, message, data.
"""
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def build_response(status_code: int, message: str, data=None, error=None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(
            {"statusCode": status_code, "error": error, "message": message, "data": data}
        ),
    )
