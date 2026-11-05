# ĐÁNH GIÁ CHẤT LƯỢNG KỸ NĂNG – PYTHON, FASTAPI VÀ DATABASE
## KIỂM TRA ĐÁNH GIÁ NĂNG LỰC CNTT – [Mã đề: 011]
**THỜI GIAN: 90 phút**

---

## Yêu cầu
Tạo project folder theo hướng dẫn sau:
- Tạo folder [Mã Lớp]\_[Họ Tên]\_[Mã Đề] chứa toàn bộ file mã nguồn. *Ví dụ: HN_KS25_CNTT1_NguyenVanA_11*
- Sau khi hoàn thành project, đẩy code lên GitHub và nộp link cho người phụ trách.
- Công nghệ & công cụ sử dụng: Python core + FastAPI + MySQL + SQLAlchemy ORM, Visual Studio Code.

## Thực hành

### 1. Bối cảnh
Hệ thống Quản lý Kho hàng (warehouse_management) cần xây dựng các chức năng xử lý dữ liệu sản phẩm bằng Python Core, cấu hình dữ liệu đầu vào/đầu ra với Pydantic, kết nối cơ sở dữ liệu MySQL và viết các API quản lý sản phẩm (products) và danh mục sản phẩm (product_categories).

Sinh viên cần xây dựng API quản lý sản phẩm, cho phép thêm mới sản phẩm, xem danh sách sản phẩm kèm chi tiết danh mục sản phẩm, và xóa danh mục sản phẩm kèm xử lý ràng buộc đặc biệt.

### 2. Tài liệu

#### 2.1 Dữ liệu sản phẩm (dùng cho Phần 1)
Cho trước danh sách dữ liệu thô chứa thông tin các sản phẩm giả định sau:
```python
raw_products = [
    {"product_code": "P1001", "category": "electronics",
     "unit_price": 15000000, "status": "in_stock"},
    {"product_code": " p1002 ", "category": "furniture",
     "unit_price": 3200000, "status": "in_stock"},
    {"product_code": "P2001", "category": "stationery",
     "unit_price": 45000, "status": "out_of_stock"},
    {"product_code": "P20A", "category": "stationery",
     "unit_price": 30000, "status": "in_stock"},
    {"product_code": "P1003", "category": "electronics",
     "unit_price": 8900000, "status": "discontinued"},
    {"product_code": "P2002", "category": "stationery",
     "unit_price": 120000, "status": "in_stock"}
]
```

#### 2.2 Cơ sở dữ liệu
Database đặt tên là: **warehouse_db**

**Bảng product_categories:**
| Trường | Kiểu dữ liệu | Mô tả |
|---|---|---|
| **id** | int | Mã danh mục sản phẩm, khóa chính, tự tăng |
| **name** | string | Tên danh mục sản phẩm, tối đa 50 ký tự, độc nhất, không trống |

**Bảng products:**
| Trường | Kiểu dữ liệu | Mô tả |
|---|---|---|
| **id** | int | Mã định danh sản phẩm, khóa chính, tự tăng |
| **product_code** | string | Mã sản phẩm, tối đa 10 ký tự, độc nhất, không trống |
| **unit_price** | float | Đơn giá, không trống |
| **product_category_id** | int | Khóa ngoại liên kết tới bảng product_categories |

#### 2.3 Bảng danh sách API
| STT | Chức năng | Method | Endpoint |
|---|---|---|---|
| 1 | Truy vấn danh sách sản phẩm | GET | /products |
| 2 | Thêm sản phẩm mới | POST | /products |
| 3 | Xóa danh mục sản phẩm | DELETE | /product-categories/{id} |

#### 2.4 Quy chuẩn cấu trúc Response chung
Tất cả các API bắt buộc phải trả về dữ liệu dưới dạng đồng nhất gồm 4 trường sau:
- **statusCode** (số nguyên): mã trạng thái HTTP (200, 201, 404, ...).
- **error** (chuỗi hoặc null): lỗi nếu có (ví dụ: "Not Found").
- **message** (chuỗi): thông báo trạng thái thực hiện hành động cho người dùng.
- **data** (object/mảng hoặc null): dữ liệu kết quả trả về từ database.

**Ví dụ mẫu Response API lấy danh sách sản phẩm thành công:**
```json
{
  "statusCode": 200,
  "error": null,
  "message": "Lấy danh sách sản phẩm thành công",
  "data": [
    {
      "id": 1,
      "product_code": "P1001",
      "unit_price": 15000000.0,
      "product_category": {
        "id": 1,
        "name": "electronics"
      }
    }
  ]
}
```

### 3. Yêu cầu nghiệp vụ

#### Phần 1: Python Core & Tư duy thuật toán (35 điểm)
**Yêu cầu 1.1 (10 điểm) – Chuẩn hóa & validate dữ liệu:**
Viết hàm `clean_and_validate_products` thực hiện:
- Loại bỏ khoảng trắng thừa ở hai đầu của mã sản phẩm `product_code` và chuyển toàn bộ chữ cái thành dạng in hoa (ví dụ: " p1002 " → "P1002").
- Kiểm tra tính hợp lệ của mã sản phẩm sau khi chuẩn hóa: phải bắt đầu bằng chữ cái P, theo sau là các chữ số. Nếu không hợp lệ, loại bỏ sản phẩm đó khỏi danh sách.

**Yêu cầu 1.2 (12 điểm) – Tìm kiếm tuyến tính (Linear Search):**
Viết hàm `search_products` để tìm kiếm các sản phẩm thỏa mãn đồng thời:
- Đơn giá (`unit_price`) nhỏ hơn hoặc bằng giá trị truyền vào tham số.
- Trạng thái (`status`) trùng khớp với giá trị truyền vào tham số (nếu giá trị truyền vào là None thì chỉ lọc theo đơn giá).

**Yêu cầu 1.3 (13 điểm) – Sắp xếp nổi bọt (Bubble Sort):**
Viết hàm `sort_products_by_unit_price_desc` tự cài đặt thuật toán Bubble Sort để sắp xếp danh sách sản phẩm theo thứ tự đơn giá giảm dần.

#### Phần 2: Parameter & Pydantic Validation (10 điểm)
**Yêu cầu 2.1 (5 điểm) – Định nghĩa Schema & validate dữ liệu:**
Tạo Schema `ProductCreate` để validate dữ liệu đầu vào:
- `product_code`: bắt buộc, độ dài tối thiểu 4 ký tự, tối đa 10 ký tự.
- `unit_price`: bắt buộc, giá trị phải lớn hơn 0.
- `product_category_id`: bắt buộc (ID liên kết với bảng danh mục sản phẩm).

**Yêu cầu 2.2 (5 điểm) – Phản hồi chuẩn RESTful & Response Model:**
Tạo Schema `ProductResponse` dùng làm response_model khi trả về thông tin sản phẩm.

#### Phần 3: Kết nối MySQL & SQLAlchemy ORM (20 điểm)
**Yêu cầu 3.1 (10 điểm) – Khai báo cấu hình CSDL:**
Viết file `database.py` kết nối tới cơ sở dữ liệu MySQL local có tên warehouse_db.

**Yêu cầu 3.2 (10 điểm) – Thiết kế Model quan hệ 1-N:**
Khai báo 2 SQLAlchemy Models trong thư mục `models/` đại diện cho mối quan hệ 1-N:
- Bảng product_categories: tạo các cột tương ứng, thiết lập mối quan hệ.
- Bảng products: tạo các cột tương ứng, thiết lập mối quan hệ.

#### Phần 4: Endpoints API & logic nghiệp vụ (35 điểm)
**Yêu cầu 4.1 (5 điểm) – Chia thư mục/file:** Chia thư mục/file theo cấu trúc phân tầng nêu ở mục 5. Yêu cầu kỹ thuật.

**Yêu cầu 4.2 (10 điểm) – API 1: POST /products**
- **Mô tả:** thêm mới một sản phẩm.
- **Yêu cầu:** thêm dữ liệu sản phẩm từ Request Body vào database; xử lý trường hợp `product_category_id` không tồn tại và `product_code` bị trùng.

**Yêu cầu 4.3 (10 điểm) – API 2: GET /products**
- **Mô tả:** truy vấn danh sách sản phẩm.
- **Yêu cầu:** trả về danh sách sản phẩm kèm theo thông tin chi tiết của danh mục sản phẩm đó.

**Yêu cầu 4.4 (10 điểm) – API 3: DELETE /product-categories/{id}**
- **Mô tả:** xóa danh mục sản phẩm theo ID.
- **Yêu cầu:** chỉ cho phép xóa khi không có sản phẩm nào thuộc danh mục sản phẩm này.

### 4. Thang điểm chi tiết
| STT | Nghiệp vụ cần đạt được | Mô tả chi tiết nghiệp vụ | Điểm |
|---|---|---|---|
| 1 | Phần 1 – Python Core & Tư duy thuật toán | Yêu cầu 1.1 – Chuẩn hóa & validate dữ liệu: 10 • Yêu cầu 1.2 – Tìm kiếm tuyến tính: 12 • Yêu cầu 1.3 – Sắp xếp nổi bọt: 13 | 35 |
| 2 | Phần 2 – Parameter & Pydantic Validation | Yêu cầu 2.1 – Schema ProductCreate & validate dữ liệu: 5 • Yêu cầu 2.2 – Schema ProductResponse & response_model: 5 | 10 |
| 3 | Phần 3 – Kết nối MySQL & SQLAlchemy ORM | Yêu cầu 3.1 – Cấu hình kết nối CSDL (database.py): 10 • Yêu cầu 3.2 – Model quan hệ 1-N: 10 | 20 |
| 4 | Phần 4 – Endpoints API & logic nghiệp vụ | Yêu cầu 4.1 – Chia thư mục/file: 5 • Yêu cầu 4.2 – API POST /products: 10 • Yêu cầu 4.3 – API GET /products: 10 • Yêu cầu 4.4 – API DELETE /product-categories/{id}: 10 | 35 |
| | **Tổng cộng** | | **100** |

### 5. Yêu cầu kỹ thuật
- Chạy được chương trình bằng lệnh `uvicorn main:app --reload`.
- Test được API trên Swagger UI.
- Kết nối được FastAPI với MySQL thông qua SQLAlchemy ORM.
- Source code được tách thành nhiều file theo cấu trúc phân tầng rõ ràng và hợp lý.

*Lưu ý: Chỉ tính điểm khi chức năng chương trình thực hiện đúng theo yêu cầu nghiệp vụ được giao.*

---

## Hướng dẫn chạy bài giải mẫu (thư mục `warehouse_management/`)
```
warehouse_management/
├── main.py                     # khởi tạo app, đăng ký router, xử lý lỗi
├── database.py                 # kết nối MySQL warehouse_db
├── models/
│   ├── __init__.py
│   ├── product_category.py
│   └── product.py
├── schemas/
│   ├── __init__.py
│   └── product_schema.py
├── services/
│   ├── __init__.py
│   ├── product_service.py
│   └── product_category_service.py
├── routers/
│   ├── __init__.py
│   ├── product_router.py
│   └── product_category_router.py
├── utils/
│   ├── __init__.py
│   ├── python_core.py          # Phần 1
│   ├── exceptions.py
│   └── response.py
├── create_database.sql
└── requirements.txt
```
1. `pip install -r requirements.txt`
2. Chạy `create_database.sql` trong MySQL (tạo database `warehouse_db`), sửa user/mật khẩu trong `database.py` nếu khác `root/123456`.
3. Phần 1: `python -m utils.python_core`
4. API: `uvicorn main:app --reload` → mở http://127.0.0.1:8000/docs. Khi khởi động, bảng `product_categories` được tạo sẵn các loại: 1 = electronics, 2 = furniture, 3 = stationery.
