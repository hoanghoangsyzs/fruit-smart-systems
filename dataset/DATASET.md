# Quy chuẩn Dataset — Hybrid (D3)

## Cấu trúc thư mục

```
dataset/
├── disease/
│   ├── train/
│   │   ├── healthy/
│   │   ├── leaf_spot/
│   │   └── anthracnose/
│   ├── val/
│   └── test/
├── ripeness/
│   ├── train/
│   │   ├── unripe/
│   │   ├── half_ripe/
│   │   └── ripe/
│   ├── val/
│   └── test/
└── metadata.csv
```

## Class mặc định (có thể mở rộng)

### Disease (sâu bệnh / sức khỏe lá)

| Label EN | Label VI | Mô tả |
|----------|----------|--------|
| healthy | Khỏe mạnh | Lá/trái không dấu hiệu bệnh rõ |
| leaf_spot | Đốm lá | Đốm nâu/xám trên lá |
| anthracnose | Thán thư | Vết lõm, thối đen |

**Mục tiêu số ảnh:** ≥80 ảnh/class (train), ≥15/class (val), ≥15/class (test).

### Ripeness (độ chín trái)

| Label EN | Label VI |
|----------|----------|
| unripe | Chưa chín |
| half_ripe | Gần chín |
| ripe | Chín |

## metadata.csv

```csv
path,task,label,source,orchard_location,captured_at,notes
disease/train/healthy/img001.jpg,disease,healthy,self,Dong Nai,2026-05-01,
ripeness/train/ripe/img010.jpg,ripeness,ripe,kaggle,,2026-04-15,subset plant doc
```

- **source:** `self` | `kaggle` | `web` (ghi nguồn trong báo cáo)
- Không trùng cùng 1 quả trong train và test

## Quy tắc chụp ảnh (self)

1. Ánh sáng tự nhiên, tránh chói.
2. Một đối tượng chính (1 lá hoặc 1 trái) chiếm ≥50% khung hình.
3. Định dạng JPG/PNG, min 640×640.
4. Đặt tên: `{class}_{YYYYMMDD}_{seq}.jpg`

## Baseline nhanh (tuần 1)

Tải subset PlantVillage hoặc fruit ripeness dataset → map nhãn gần đúng → fine-tune tuần 2–3 bằng ảnh mít thật.

## .gitignore

Không commit ảnh lớn lên Git; dùng Google Drive / LFS và ghi link trong README.
