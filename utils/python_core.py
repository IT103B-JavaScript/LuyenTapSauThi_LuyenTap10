"""
Phần 1: Python Core & Tư duy thuật toán
- Yêu cầu 1.1: clean_and_validate_products
- Yêu cầu 1.2: search_products (Linear Search)
- Yêu cầu 1.3: sort_products_by_unit_price_desc (Bubble Sort)
Chạy thử: python -m utils.python_core
"""

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


def is_valid_product_code(code):
    """Mã hợp lệ: bắt đầu bằng chữ cái P, theo sau là ít nhất một chữ số (chỉ chữ số)."""
    return len(code) >= 2 and code[0] == "P" and code[1:].isdigit()


def clean_and_validate_products(raw_list):
    """Yêu cầu 1.1: chuẩn hóa product_code (strip + upper) và loại bỏ sản phẩm có mã không hợp lệ."""
    cleaned_list = []
    for item in raw_list:
        code = str(item.get("product_code", "")).strip().upper()
        if is_valid_product_code(code):
            cleaned_item = dict(item)  # tạo bản sao, không sửa dữ liệu gốc
            cleaned_item["product_code"] = code
            cleaned_list.append(cleaned_item)
        else:
            print(f"[Loại bỏ] mã sản phẩm không hợp lệ: {item.get('product_code')!r}")
    return cleaned_list


def search_products(item_list, max_unit_price, status=None):
    """Yêu cầu 1.2: tìm tuyến tính sản phẩm có unit_price <= max_unit_price và đúng status (None = bỏ qua status)."""
    result = []
    for item in item_list:
        if item["unit_price"] > max_unit_price:
            continue
        if status is not None and item["status"] != status:
            continue
        result.append(item)
    return result


def sort_products_by_unit_price_desc(item_list):
    """Yêu cầu 1.3: Bubble Sort giảm dần theo unit_price, trả về danh sách mới."""
    sorted_list = list(item_list)
    n = len(sorted_list)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if sorted_list[j]["unit_price"] < sorted_list[j + 1]["unit_price"]:
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
                swapped = True
        if not swapped:
            break
    return sorted_list


def print_products(title, item_list):
    """In danh sách sản phẩm dạng bảng để kiểm tra kết quả."""
    print(f"\n===== {title} ({len(item_list)}) =====")
    for item in item_list:
        print(
            f"{item['product_code']:<8} | {item['category']:<14} | "
            f"{item['unit_price']:>12,} | {item['status']}"
        )


if __name__ == "__main__":
    valid_products = clean_and_validate_products(raw_products)
    print_products("1.1 Sau khi chuẩn hóa & validate", valid_products)

    print_products(
        "1.2 Tìm sản phẩm có unit_price <= 5000000 và status = 'in_stock'",
        search_products(valid_products, 5000000, "in_stock"),
    )
    print_products(
        "1.2 Tìm sản phẩm có unit_price <= 5000000 (status = None)",
        search_products(valid_products, 5000000),
    )

    print_products("1.3 Sắp xếp unit_price giảm dần (Bubble Sort)", sort_products_by_unit_price_desc(valid_products))
