# Thiết kế REST API

**Base URL:** `http://localhost:8000`  
**Prefix:** `/api/v1`  
**Auth:** Bearer JWT (trừ `/auth/*` và `/health`)

---

## 1. Health

### `GET /health`

```json
{ "status": "ok", "models_loaded": { "disease": true, "ripeness": true } }
```

---

## 2. Authentication

### `POST /api/v1/auth/register`

```json
{ "email": "user@example.com", "password": "secret", "full_name": "Nguyen Van A" }
```

### `POST /api/v1/auth/login`

```json
{ "email": "user@example.com", "password": "secret" }
```

**Response:**

```json
{ "access_token": "<jwt>", "token_type": "bearer" }
```

---

## 3. Orchards (vườn mít)

### `GET /api/v1/orchards`

Danh sách vườn của user đăng nhập.

### `POST /api/v1/orchards`

```json
{ "name": "Vườn mít nhà", "location": "Dong Nai", "area_ha": 0.5 }
```

### `GET /api/v1/orchards/{orchard_id}`

### `DELETE /api/v1/orchards/{orchard_id}`

---

## 4. Analyze (core)

### `POST /api/v1/analyze`

**Content-Type:** `multipart/form-data`

| Field | Type | Required |
|-------|------|----------|
| `file` | image/jpeg,png | yes |
| `orchard_id` | int | no |
| `note` | string | no |

**Response 200:**

```json
{
  "prediction_id": 42,
  "disease": {
    "label": "leaf_spot",
    "label_vi": "Đốm lá",
    "confidence": 0.87
  },
  "ripeness": {
    "label": "half_ripe",
    "label_vi": "Gần chín",
    "confidence": 0.79
  },
  "quality_score": 72,
  "quality_grade": "B",
  "recommendations": [
    {
      "priority": "high",
      "title": "Phun thuốc phòng đốm lá",
      "detail": "Phát hiện dấu hiệu đốm lá. Kiểm tra vùng ẩm, tỉa cành thoáng."
    }
  ],
  "image_url": "/uploads/abc123.jpg",
  "created_at": "2026-05-21T10:00:00Z"
}
```

**Lỗi:**

- `400` — file không hợp lệ
- `413` — file quá lớn (>10MB)
- `503` — model chưa load

---

## 5. Predictions (lịch sử)

### `GET /api/v1/predictions`

Query: `orchard_id`, `from_date`, `to_date`, `limit`, `offset`

### `GET /api/v1/predictions/{prediction_id}`

---

## 6. Dashboard stats

### `GET /api/v1/dashboard/summary`

Query: `orchard_id` (optional)

```json
{
  "total_scans": 120,
  "disease_distribution": [
    { "label": "healthy", "count": 80 },
    { "label": "leaf_spot", "count": 25 }
  ],
  "ripeness_distribution": [
    { "label": "unripe", "count": 30 },
    { "label": "ripe", "count": 45 }
  ],
  "timeline": [
    { "date": "2026-05-19", "scans": 5, "avg_quality": 68 },
    { "date": "2026-05-20", "scans": 8, "avg_quality": 71 }
  ]
}
```

---

## 7. Mã lỗi chuẩn

```json
{ "detail": "Mô tả lỗi", "code": "INVALID_IMAGE" }
```

| code | HTTP |
|------|------|
| INVALID_IMAGE | 400 |
| UNAUTHORIZED | 401 |
| ORCHARD_NOT_FOUND | 404 |
| MODEL_UNAVAILABLE | 503 |

---

## 8. Mock mode (tuần 1)

Biến môi trường `MOCK_INFERENCE=true` trả response cố định không cần GPU.
