# Khung báo cáo đồ án / môn học

> Copy từng chương sang Word, định dạng theo quy định trường (font, lề, mục lục tự động).

---

## LỜI MỞ ĐẦU

## MỤC LỤC

## DANH MỤC HÌNH ẢNH / BẢNG BIỂU

---

## CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI

1.1. Đặt vấn đề  
1.2. Mục tiêu nghiên cứu  
1.3. Đối tượng và phạm vi  
1.4. Ý nghĩa khoa học và thực tiễn  
1.5. Phương pháp nghiên cứu  
1.6. Cấu trúc báo cáo  

*Nguồn:* `docs/DE_CUONG.md` mục I–IV, VII.

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT

2.1. Tổng quan cây mít và yêu cầu canh tác  
2.2. Sâu bệnh và tiêu chí độ chín trái mít  
2.3. Thị giác máy tính và tiền xử lý ảnh  
2.4. Học máy và học sâu (CNN, transfer learning)  
2.5. Kiến trúc Web/API và PWA  
2.6. Khảo sát giải pháp liên quan  

*Hình gợi ý:* sơ đồ CNN, pipeline CV.

---

## CHƯƠNG 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG

3.1. Yêu cầu chức năng và phi chức năng  
3.2. Use case (Upload ảnh, Chụp PWA, Xem dashboard, Quản lý vườn)  
3.3. Kiến trúc tổng thể (3 lớp: Client – API – ML)  
3.4. Thiết kế CSDL — `THIET_KE_ERD.md`  
3.5. Thiết kế API — `THIET_KE_API.md`  
3.6. Thiết kế giao diện (wireframe Web, Mobile)  
3.7. Thiết kế module AI và khuyến nghị  

*Hình bắt buộc:* ERD, sequence diagram luồng analyze.

---

## CHƯƠNG 4: TRIỂN KHAI HỆ THỐNG

4.1. Môi trường phát triển  
4.2. Xây dựng dataset (`dataset/DATASET.md`)  
4.3. Huấn luyện mô hình (`ml/train.py`)  
4.4. Triển khai backend FastAPI  
4.5. Triển khai frontend React + PWA  
4.6. Dashboard và tích hợp  
4.7. Docker Compose  

*Hình:* screenshot từng màn hình, cấu trúc thư mục.

---

## CHƯƠNG 5: KIỂM THỬ VÀ ĐÁNH GIÁ

5.1. Kịch bản kiểm thử (`CHECKLIST_TEST.md`)  
5.2. Kết quả metric ML (accuracy, F1, confusion matrix)  
5.3. Đánh giá hiệu năng API (thời gian inference)  
5.4. Đánh giá UX (qualitative)  
5.5. Thảo luận hạn chế và hướng phát triển  

*Bảng mẫu metric:*

| Task | Accuracy | F1 macro |
|------|----------|----------|
| Disease | … | … |
| Ripeness | … | … |

---

## KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

- Tóm tắt kết quả đạt được  
- So sánh với mục tiêu đề cương  
- Hướng mở rộng: YOLO detection, IoT, đa ngôn ngữ, app native  

---

## TÀI LIỆU THAM KHẢO

## PHỤ LỤC

- A: Hướng dẫn cài đặt (README)  
- B: Mẫu API request/response  
- C: Danh sách class dataset  
- D: Source code (CD/Git link)  
