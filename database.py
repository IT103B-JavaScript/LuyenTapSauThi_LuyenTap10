"""
database.py - Cấu hình kết nối cơ sở dữ liệu MySQL bằng SQLAlchemy.
Database: warehouse_db
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Chuỗi kết nối: mysql+pymysql://<user>:<password>@<host>:<port>/<database>
# Có thể ghi đè bằng biến môi trường DATABASE_URL nếu máy dùng mật khẩu khác.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:123456@localhost:3306/warehouse_db",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency cấp phiên làm việc với DB cho mỗi request, tự đóng sau khi xong."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
