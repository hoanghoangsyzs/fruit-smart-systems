# ĐỀ CƯƠNG NGHIÊN CỨU VÀ TRIỂN KHAI

## HỆ THỐNG THÔNG MINH NHẬN DIỆN VÀ ĐÁNH GIÁ TRÁI/CÂY MÍT DỰA TRÊN TRÍ TUỆ NHÂN TẠO VÀ XỬ LÝ ẢNH

**Đơn vị:** Software Development Centre (SDC)  
**Cấp độ triển khai:** Nâng cao (Web + Mobile PWA + Dashboard + AI + Dataset)  
**Thời gian:** 4 tuần | **Nhóm:** 2 thành viên

---

## I. TÊN ĐỀ TÀI

Hệ thống thông minh nhận diện sâu bệnh, phân loại độ chín và giám sát vườn mít sử dụng học sâu, thị giác máy tính và ứng dụng Web/Mobile.

---

## II. LÝ DO CHỌN ĐỀ TÀI

- Mít là cây ăn quả quan trọng; chất lượng trái phụ thuộc độ chín và tình trạng sức khỏe cây.
- Nông dân cần công cụ hỗ trợ nhanh khi quan sát tại vườn (mobile) và quản lý tổng thể (dashboard).
- Ứng dụng AI/CV trong nông nghiệp thông minh phù hợp định hướng đào tạo CNTT và SDC.

---

## III. MỤC TIÊU NGHIÊN CỨU

### 1. Mục tiêu tổng quát

Xây dựng hệ thống tích hợp cho phép người dùng tải/chụp ảnh mít hoặc lá mít, tự động phân tích và đưa ra khuyến nghị canh tác, đồng thời theo dõi thống kê vườn qua dashboard.

### 2. Mục tiêu cụ thể

1. **Nhận dạng sâu bệnh hại** trên lá/trái mít bằng mô hình học sâu.
2. **Phân loại độ chín trái** (ít nhất 3 mức: chưa chín, gần chín, chín).
3. **Đánh giá chất lượng** dựa trên điểm tổng hợp từ kết quả nhận dạng.
4. **Giám sát vườn mít** qua lịch sử phân tích, biểu đồ thống kê theo thời gian.

---

## IV. ĐỐI TƯỢNG VÀ PHẠM VI

### Trong phạm vi

- Dataset ảnh mít/lá (hybrid: nguồn mở + tự thu thập).
- Hai mô hình phân loại: disease, ripeness.
- API REST, Web upload, PWA chụp ảnh, dashboard thống kê.
- Hệ thống khuyến nghị dạng rule-based.

### Ngoài phạm vi (giai đoạn 4 tuần)

- Robot tự hành, drone, IoT cảm biến thời gian thực.
- Nhận dạng đa giống mít toàn quốc với độ chính xác thương mại.
- App native iOS/Android (dùng PWA thay thế).

---

## V. CÔNG NGHỆ SỬ DỤNG

| Lớp | Công nghệ |
|-----|-----------|
| ML/DL | Python, PyTorch, timm (EfficientNet-B0) |
| CV | OpenCV, torchvision transforms |
| Backend | FastAPI, SQLAlchemy, SQLite/PostgreSQL |
| Frontend | React, Vite, TypeScript, Recharts |
| Mobile | PWA (manifest, service worker, camera API) |
| DevOps | Docker Compose |

---

## VI. NỘI DUNG NGHIÊN CỨU VÀ TRIỂN KHAI

Theo 6 module SDC + dashboard:

1. **Tổng quan cây mít** — sinh học, sâu bệnh thường gặp, tiêu chí chín.
2. **Cơ sở dữ liệu hình ảnh** — thu thập, gán nhãn, metadata.
3. **Mô hình ML/DL** — transfer learning, đánh giá metric.
4. **Giải pháp nhận dạng** — pipeline inference, API.
5. **Hệ thống Web/Mobile** — UX upload/chụp ảnh.
6. **Hệ thống khuyến nghị** — rules từ kết quả AI.
7. **Dashboard giám sát** — thống kê vườn theo thời gian.

### Quy trình kỹ thuật

```
Thu thập dữ liệu → Tiền xử lý ảnh → Huấn luyện mô hình → Triển khai hệ thống
```

---

## VII. PHƯƠNG PHÁP NGHIÊN CỨU

- Khảo sát tài liệu về mít, plant disease datasets, CNN/transfer learning.
- Thực nghiệm: so sánh accuracy/F1 trên tập validation.
- Phát triển phần mềm theo mô hình incremental (demo mỗi tuần).
- Kiểm thử: unit API, E2E luồng upload → predict → dashboard.

---

## VIII. KẾ HOẠCH 4 TUẦN

| Tuần | Công việc chính | Sản phẩm |
|------|-----------------|----------|
| 1 | Dataset + baseline model + API mock | Demo predict (mock/real) |
| 2 | 2 model + Web upload + DB | Luồng Web E2E |
| 3 | PWA + Dashboard + fine-tune | Mobile + biểu đồ |
| 4 | Tích hợp, test, báo cáo, Docker | Hệ thống nộp |

Chi tiết: [KE_HOACH_4_TUAN.md](KE_HOACH_4_TUAN.md)

---

## IX. KẾT QUẢ DỰ KIẾN

1. Bộ mã nguồn `mit-smart-system` (Git).
2. Dataset có mô tả (`dataset/DATASET.md`) và metadata mẫu.
3. Hai file model `.pt` (disease, ripeness) + báo cáo metric.
4. Ứng dụng Web + PWA + Dashboard hoạt động.
5. Báo cáo đồ án (~40–60 tr) và slide + video demo.

---

## X. TÀI LIỆU THAM KHẢO (mẫu)

1. Goodfellow, I. — Deep Learning.
2. PyTorch Documentation — https://pytorch.org/docs/
3. FastAPI Documentation — https://fastapi.tiangolo.com/
4. PlantVillage / các dataset bệnh cây trồng (ghi rõ nguồn trong báo cáo).

---

## XI. PHÂN CÔNG NHÓM

| Thành viên | Trách nhiệm |
|------------|-------------|
| A | Backend, Frontend, Dashboard, Docker, Chương 3–4 (phần hệ thống) |
| B | Dataset, ML train/eval, khuyến nghị, Chương 1–2 + metric Chương 5 |

---

*Tài liệu này là cơ sở cho báo cáo Chương 1 (Giới thiệu) và phần mở đầu đồ án.*
