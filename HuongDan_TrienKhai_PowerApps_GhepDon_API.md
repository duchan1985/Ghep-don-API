# HƯỚNG DẪN TRIỂN KHAI GHÉP ĐƠN POWER APPS CÓ DEPLOY API

## 🎯 MỤC TIÊU
Xây hệ thống cho phép người dùng nhập kích thước máy (VD: 3000mm), và hệ thống tự động tìm tổ hợp mã hàng (giấy carton) gần nhất để ghép, dùng Power Apps + API Python.

---

## ✅ THÀNH PHẦN HỆ THỐNG

1. **Power Apps**: giao diện nhập và hiển thị kết quả
2. **Dataverse**: lưu đơn hàng chờ ghép (bảng `DonDatHangCho`)
3. **Power Automate**: gọi API
4. **API Python (FastAPI)**: xử lý ghép tổ hợp mã gần nhất

---

## 🔧 BƯỚC 1: TẠO BẢNG DATAVERSE

Bảng: `DonDatHangCho`

| Tên cột     | Kiểu dữ liệu   |
|-------------|----------------|
| ma_hang     | Text           |
| kich_thuoc  | Whole Number   |
| gsm         | Whole Number   |
| so_luong    | Whole Number   |
| ngay_dat    | Date and Time  |

---

## 🐍 BƯỚC 2: TẠO VÀ DEPLOY API PYTHON

### 📄 Tạo file `api.py`:
- Copy nội dung từ `ghep_don_api.py` trong gói này

### 📁 requirements.txt:
```
fastapi
uvicorn
```

### 🌐 Deploy lên [https://render.com](https://render.com)
- New Web Service
- Start command:
```
uvicorn api:app --host 0.0.0.0 --port 10000
```

Sau deploy thành công, bạn sẽ có URL như:
```
https://your-api.onrender.com/ghep_don
```

---

## 🔄 BƯỚC 3: TẠO FLOW POWER AUTOMATE

### 1. Tạo flow dạng: "Instant cloud flow (trigger from Power Apps)"
### 2. Các bước:

- Get items từ bảng `DonDatHangCho`
- Dùng `Select` để định dạng thành JSON:
```json
{
  "gioi_han": 3000,
  "danh_sach": [
    {"ma": "M1", "kich_thuoc": 950},
    ...
  ]
}
```
- Dùng HTTP action POST tới API
- Parse JSON kết quả
- Trả kết quả về Power Apps

---

## 🖥 BƯỚC 4: THIẾT KẾ GIAO DIỆN POWER APPS

- Text input: `txt_KichThuocMay`
- Button `btn_GhepDon`:
```powerfx
Set(KetQua, Flow_GhepDon.Run(Value(txt_KichThuocMay)))
```

- Label kết quả:
```powerfx
Concat(KetQua.mang, ma & " - " & Text(kich_thuoc) & "mm", Char(10)) & Char(10) & "Tổng: " & Text(KetQua.tong) & "mm"
```

---

## ✅ BẠN CÓ THỂ MỞ RỘNG:

- Lọc thêm theo GSM, giấy trắng/nâu...
- Ghi lại kết quả vào bảng `DonHangTong`
- Tự động chạy mỗi ngày qua Power Automate Schedule