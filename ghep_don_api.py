from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from itertools import combinations

app = FastAPI()

class Product(BaseModel):
    ProductName: str
    PaperSize: float
    DinhLuong: float
    Quantity: int

class InputData(BaseModel):
    gioi_han_min: float
    gioi_han_max: float
    danh_sach: List[Product]

@app.post("/ghep_kho_giay")
def ghep_kho_giay(data: InputData):
    min_limit = data.gioi_han_min
    max_limit = data.gioi_han_max

    # Tách sản phẩm theo Quantity (explode)
    all_items = []
    for p in data.danh_sach:
        for _ in range(p.Quantity):
            all_items.append(Product(**p.dict(), Quantity=1))

    used = set()
    groups = []

    # Sắp xếp giảm dần theo PaperSize
    sorted_items = sorted(enumerate(all_items), key=lambda x: x[1].PaperSize, reverse=True)

    for i, item in sorted_items:
        if i in used:
            continue
        group = [item]
        total = item.PaperSize
        used.add(i)

        for j, other in sorted_items:
            if j in used or i == j:
                continue
            if total + other.PaperSize <= max_limit:
                group.append(other)
                total += other.PaperSize
                used.add(j)
                if total >= min_limit:
                    break

        if min_limit <= total <= max_limit:
            groups.append(group)
        else:
            for g in group:
                index = all_items.index(g)
                used.discard(index)

    return {
        "danh_sach_nhom": groups
    }