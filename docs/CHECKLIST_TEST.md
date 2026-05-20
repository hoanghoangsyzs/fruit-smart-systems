# Checklist kiểm thử E2E (Tuần 4)

| # | Kịch bản | Kỳ vọng | OK |
|---|----------|---------|-----|
| 1 | Đăng ký user mới | 201, login được | |
| 2 | Login sai mật khẩu | 401 | |
| 3 | Tạo vườn mới | Hiện trong danh sách | |
| 4 | Upload ảnh JPG hợp lệ | disease + ripeness + quality | |
| 5 | Upload file không phải ảnh | 400 INVALID_IMAGE | |
| 6 | Analyze không token | 401 | |
| 7 | PWA chụp ảnh (mobile) | Kết quả giống upload | |
| 8 | Dashboard sau 3 lần quét | Biểu đồ đổi số liệu | |
| 9 | Lọc dashboard theo vườn | Chỉ hiện predict của vườn đó | |
| 10 | MOCK_INFERENCE=false + model có | Kết quả khác mock | |

## Metric ML (Người B điền)

- Tập test: ___ ảnh, chia từ folder `dataset/*/test`
- Disease F1: ___
- Ripeness F1: ___
