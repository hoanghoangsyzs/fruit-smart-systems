# Thư mục lưu Hình 2.8.5 (báo cáo)

Đặt file PNG đã chụp tại đây:

```
docs/figures/2.8.5/
├── Hinh_2_8_5_1_dataset.png
├── Hinh_2_8_5_2_train.png
├── Hinh_2_8_5_2_train_epoch.png
├── Hinh_2_8_5_3_inference.png
├── Hinh_2_8_5_3_inference_service.png
├── Hinh_2_8_5_4_fastapi_main.png
├── Hinh_2_8_5_4_fastapi_analyze.png
├── Hinh_2_8_5_5_web_gui_PLACEHOLDER.png   ← thay bằng screenshot /analyze
└── Hinh_2_8_5_6_web_ket_qua_PLACEHOLDER.png
```

Tạo lại ảnh code/dataset:

```powershell
cd D:\mit-smart-system\backend
.\.venv\Scripts\python.exe ..\scripts\generate_report_figures.py
```

Chụp Web (2.8.5.5–2.8.5.6):

```powershell
.\scripts\capture_web_figures.ps1
```

Ảnh báo cáo thường **không** commit lên Git (kích thước lớn). Thêm `docs/figures/**/*.png` vào `.gitignore` nếu cần.

Hướng dẫn chụp: [../../HUONG_DAN_HINH_2_8_5.md](../../HUONG_DAN_HINH_2_8_5.md)
