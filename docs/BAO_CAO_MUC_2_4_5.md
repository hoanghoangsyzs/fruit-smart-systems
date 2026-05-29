# Mẫu văn bản — Mục 2.4.5 (copy vào Word)

## 2.4.5. Tích hợp mô hình vào API phục vụ frontend

Sau khi huấn luyện, mô hình được đóng gói dưới dạng file checkpoint (`.pt`) lưu tại `ml/artifacts/`. Để phục vụ giao tiếp với hệ thống Web và PWA, nhóm em triển khai **API REST bằng FastAPI** (vai trò tương đương việc dùng Flask trong các mô hình triển khai ML phổ biến).

Luồng xử lý:

1. Client (React) gửi ảnh qua `POST /api/v1/analyze`.
2. Backend lưu ảnh, gọi module `ml/inference.py` (tương đương `predict.py` trong mẫu báo cáo).
3. Kết quả gồm nhãn sâu bệnh, độ chín, điểm chất lượng, vùng ảnh hưởng (hotspot) và khuyến nghị được trả JSON.

Các hình minh họa:

| Hình | Nội dung |
|------|----------|
| Hình 2.8.5.1 | Cấu trúc thư mục dataset |
| Hình 2.8.5.2 | Mã nguồn `ml/train.py` |
| Hình 2.8.5.3 | Mã nguồn `ml/inference.py` và service inference |
| Hình 2.8.5.4 | Mã nguồn `app/main.py`, `routers/analyze.py` |
| Hình 2.8.5.5 | Giao diện Web — gửi ảnh phân tích |
| Hình 2.8.5.6 | Giao diện Web — kết quả phân tích |

*Hướng dẫn chụp từng hình:* [HUONG_DAN_HINH_2_8_5.md](HUONG_DAN_HINH_2_8_5.md)
