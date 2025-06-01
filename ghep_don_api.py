from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Điều chỉnh lại model để tương thích dữ liệu PowerApps
class DonHang(BaseModel):
    ProductName: str
    DinhLuong: int
    PaperSize: float
    Quantity: int

class RequestData(BaseModel):
    gioi_han: float
    danh_sach: List[DonHang]

@app.post("/ghep_don")
def ghep_don(data: RequestData):
    from itertools import combinations

    best_combo = []
    best_total = 0

    # Lặp qua các tổ hợp từ 2 đến 4 phần tử
    for r in range(2, 5):
        for combo in combinations(data.danh_sach, r):
            tong = sum(item.PaperSize for item in combo)
            if tong <= data.gioi_han and tong > best_total:
                best_total = tong
                best_combo = combo

    return {
        "mang": [item.dict() for item in best_combo],
        "tong": best_total
    }