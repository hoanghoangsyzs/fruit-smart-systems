# Hướng dẫn bắt đầu — Tuần 1 (làm ngay hôm nay)

## Bước 1: Mở project trong Cursor

Thư mục gốc:

`C:\Users\ASUS\.cursor\projects\C-Users-ASUS-AppData-Local-Temp-e0739582-14f2-4387-9458-482e73e2a1b5\mit-smart-system`

**File → Open Folder** → chọn thư mục trên.

## Bước 2: Backend (Người A — 15 phút)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

Mở http://127.0.0.1:8000/docs → thử `POST /api/v1/auth/register` rồi `POST /api/v1/analyze`.

## Bước 3: Frontend (Người A — 15 phút)

Terminal mới:

```powershell
cd frontend
npm install
npm run dev
```

Mở http://localhost:5173 → đăng ký → upload ảnh bất kỳ.

## Bước 4: Dataset (Người B — tuần 1)

1. Tạo thư mục theo `dataset/DATASET.md`
2. Bỏ ít nhất 10 ảnh/class vào `train/` và vài ảnh vào `val/`
3. Chạy train:

```powershell
cd ml
pip install -r requirements.txt
python train.py --task disease --data-dir ../dataset/disease
```

## Bước 5: Bật model thật (tuần 2)

Trong `backend/.env`:

```
MOCK_INFERENCE=false
```

Đảm bảo có `ml/artifacts/disease_best.pt` và `ripeness_best.pt`.

## Xuất đề cương Word

Copy `docs/DE_CUONG.md` vào Word, chỉnh font theo quy định trường, thêm tên SV và GVHD.

## Liên hệ công việc

| Tuần | A | B |
|------|---|---|
| 1 | API + Web mock | Dataset + train disease |
| 2 | DB + E2E Web | ripeness model + metric |
| 3 | PWA + Dashboard | Fine-tune + recommendations |
| 4 | Docker + demo | Báo cáo Chương 5 |

Chi tiết: [KE_HOACH_4_TUAN.md](KE_HOACH_4_TUAN.md)
