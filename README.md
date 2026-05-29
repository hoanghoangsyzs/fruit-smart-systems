# Hệ thống thông minh nhận diện trái sầu riêng (Mức Nâng cao)

Dự án SDC: AI + Xử lý ảnh + Nông nghiệp thông minh — nhận diện sâu bệnh, độ chín, đánh giá chất lượng và giám sát vườn sầu riêng.

## Phương án đã chốt

| Hạng mục | Lựa chọn |
|----------|----------|
| Stack | **A** — PyTorch + FastAPI + React + PWA |
| Dataset | **D3** — Hybrid (Kaggle baseline + ảnh tự chụp) |
| Triển khai | **T1** — Monolith + Docker Compose |

## Cấu trúc

```
mit-smart-system/
├── docs/           # Đề cương, thiết kế, kế hoạch 4 tuần
├── dataset/        # Ảnh huấn luyện (xem DATASET.md)
├── ml/             # Huấn luyện & inference
├── backend/        # FastAPI REST API
├── frontend/       # React Web + Dashboard + PWA
└── docker-compose.yml
```

## Yêu cầu

- Python 3.10+
- Node.js 18+
- (Tuần 2+) GPU khuyến nghị cho train; CPU đủ cho inference nhẹ

## Chạy nhanh (development)

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Mở http://localhost:5173 — API proxy tới http://localhost:8000

### ML (huấn luyện)

```powershell
cd ml
pip install -r requirements.txt
python train.py --task disease --data-dir ../dataset/disease
python train.py --task ripeness --data-dir ../dataset/ripeness
```

## Docker (tuần 4)

```powershell
docker compose up --build
```

## Tài liệu báo cáo

| File | Mục đích |
|------|----------|
| [docs/DE_CUONG.md](docs/DE_CUONG.md) | Đề cương đầy đủ |
| [docs/THIET_KE_API.md](docs/THIET_KE_API.md) | REST API |
| [docs/THIET_KE_ERD.md](docs/THIET_KE_ERD.md) | Cơ sở dữ liệu |
| [docs/KE_HOACH_4_TUAN.md](docs/KE_HOACH_4_TUAN.md) | Lộ trình nhóm 2 người |
| [docs/BAO_CAO_KHUNG.md](docs/BAO_CAO_KHUNG.md) | Khung chương báo cáo |
| [dataset/DATASET.md](dataset/DATASET.md) | Quy chuẩn dataset |

## Nhóm 2 người — phân vai

- **Người A:** `backend/` + `frontend/` + tích hợp + dashboard
- **Người B:** `dataset/` + `ml/` + metric + khuyến nghị

## License

Dự án học thuật — SDC.
