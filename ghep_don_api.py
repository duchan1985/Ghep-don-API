from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class DonHang(BaseModel):
    ma: str
    kich_thuoc: int

class RequestData(BaseModel):
    gioi_han: int
    danh_sach: List[DonHang]

@app.post("/ghep_don")
def ghep_don(data: RequestData):
    from itertools import combinations

    best_combo = []
    best_total = 0

    for r in range(2, 5):
        for combo in combinations(data.danh_sach, r):
            tong = sum(item.kich_thuoc for item in combo)
            if tong <= data.gioi_han and tong > best_total:
                best_total = tong
                best_combo = combo

    return {
        "mang": [item.dict() for item in best_combo],
        "tong": best_total
    }