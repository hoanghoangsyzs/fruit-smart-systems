# Kế hoạch chi tiết 4 tuần — Nhóm 2 người

## Checkpoint bắt buộc mỗi tuần

- **T1:** API trả kết quả (mock hoặc model thật) khi POST ảnh.
- **T2:** Web upload → lưu DB → hiển thị kết quả + khuyến nghị.
- **T3:** PWA chụp ảnh + Dashboard có biểu đồ.
- **T4:** Docker + báo cáo + video demo 3–5 phút.

---

## Tuần 1 — Nền tảng, dữ liệu, AI baseline

### Người B (AI/Data)

- [ ] Đọc `dataset/DATASET.md`, tạo cấu trúc thư mục class
- [ ] Thu thập ≥30 ảnh/class (hoặc tải subset PlantVillage làm baseline)
- [ ] Ghi `metadata.csv` mẫu (10 dòng thật)
- [ ] Chạy `ml/train.py --task disease` → lưu `ml/artifacts/disease_best.pt`
- [ ] Notebook/log: accuracy, loss curve (screenshot cho báo cáo)

### Người A (Full-stack)

- [ ] Clone/setup repo, README
- [ ] Backend chạy: health, auth đơn giản, `POST /analyze` (mock)
- [ ] Frontend: layout, trang Login (demo user), trang Upload
- [ ] Viết nháp Chương 3 sơ đồ kiến trúc (copy từ `THIET_KE_*.md`)

### Tài liệu tuần 1

- [ ] Hoàn thiện đề cương (`DE_CUONG.md` → Word/PDF nộp)
- [ ] Chương 1–2 nháp (2–3 tr/người)

**Demo tuần 1:** Swagger `POST /api/v1/analyze` trả JSON mẫu.

---

## Tuần 2 — Hai model + Web E2E

### Người B

- [ ] Train ripeness model → `ripeness_best.pt`
- [ ] Export labels: `ml/artifacts/disease_labels.json`, `ripeness_labels.json`
- [ ] Confusion matrix PNG cho báo cáo
- [ ] Tích hợp `ml/inference.py` vào backend (thay mock)

### Người A

- [ ] DB: users, orchards, predictions (migration hoặc auto create)
- [ ] API: đăng ký/đăng nhập JWT, CRUD vườn, lịch sử predict
- [ ] Web: form chọn vườn, upload, hiển thị disease/ripeness/quality/recommendations
- [ ] `docs/THIET_KE_API.md` — đánh dấu endpoint đã implement

### Tài liệu tuần 2

- [ ] Chương 3 đầy đủ (use case, ERD, API)
- [ ] Nhật ký thí nghiệm ML (bảng hyperparameter)

**Demo tuần 2:** Upload ảnh trên Web → kết quả thật từ model.

---

## Tuần 3 — PWA + Dashboard + giám sát vườn

### Người A

- [ ] Trang Dashboard: Recharts (pie bệnh, line theo ngày, filter orchard)
- [ ] PWA: `manifest.json`, service worker cơ bản, nút "Chụp tại vườn"
- [ ] Responsive mobile

### Người B

- [ ] Fine-tune nếu F1 < 0.7 (thêm augmentation, điều chỉnh epoch)
- [ ] Hoàn thiện `ml/config/recommendations.yaml`
- [ ] Test 20 ảnh hold-out, ghi bảng kết quả cho Chương 5

### Tài liệu tuần 3

- [ ] Chương 4 nháp (triển khai backend/frontend/ml)

**Demo tuần 3:** Điện thoại mở PWA → chụp → dashboard cập nhật.

---

## Tuần 4 — Hoàn thiện, kiểm thử, nộp

### Cả nhóm

- [ ] E2E test thủ công (checklist 10 case trong `docs/CHECKLIST_TEST.md`)
- [ ] `docker compose up` — chạy được một lệnh
- [ ] Sửa bug, tối ưu thời gian inference (<3s/ảnh CPU)
- [ ] Quay video demo + slide 10–15 trang
- [ ] Báo cáo hoàn chỉnh Chương 1–5 + Kết luận
- [ ] Đóng gói: code + `docs/` + hướng dẫn cài trong README

**Demo tuần 4:** Trình diễn đủ 5 khối slide "Sản phẩm hoàn thiện".

---

## Rủi ro & plan B

| Rủi ro | Plan B |
|--------|--------|
| Thiếu ảnh mít | Giảm class; dùng PlantVillage ghi chú trong báo cáo |
| Model yếu | Binary healthy/disease trước, multi-class sau |
| PWA camera lỗi | Upload file từ thư viện ảnh |
| Trễ 2 ngày | Cắt auth phức tạp, dùng 1 user demo cố định |

---

## Issue tracker gợi ý (GitHub/GitLab)

Tạo label: `week-1` … `week-4`, `person-a`, `person-b`, `docs`, `blocked`.
