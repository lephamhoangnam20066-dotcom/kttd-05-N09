# Bài thực hành Kiểm thử phần mềm – Tuần 9, W1

**Kiểm thử tự động Web bằng Selenium – Nhóm N09**

| | |
|---|---|
| Chức năng | 4 – Dữ liệu & trạng thái đặc biệt |
| Đề bài | Bảng dữ liệu sắp xếp được (Sortable Data Tables) |
| Trang kiểm thử | https://the-internet.herokuapp.com/tables |
| Nhánh | `week-09` |
| Kiến thức | `find_elements`, `By.XPATH`, `By.CSS_SELECTOR`, `By.TAG_NAME`, `.text`, `.click()`, `sorted()` |
| Tài liệu | 4.3 By XPath · 4.5 By Tag Name · 4.7 By CSS Selector · 7.20 WebElement |

## Mục tiêu

- Đọc dữ liệu của bảng HTML theo cột, theo dòng bằng `find_elements`.
- So sánh 3 cách định vị: XPath (bảng không có class), CSS selector (bảng có class), Tag Name (duyệt `tr` → `td`).
- Kiểm tra chức năng sắp xếp: bấm tiêu đề 1 lần tăng dần, 2 lần giảm dần, đối chiếu với `sorted()` của Python.
- Nhận ra các bẫy khi kiểm thử bảng: cột tiền tệ phải so sánh theo số, dữ liệu ban đầu đã có thứ tự, giá trị trùng nhau.

## Cấu trúc thư mục

```
tuan-09/W1/
├── anh/                 # ảnh chụp bảng sau khi sắp xếp (tự sinh khi chạy test)
├── README.md            # file này
├── cai_dat.bat          # cài thư viện (chạy 1 lần)
├── chay_kiem_thu.bat    # chạy toàn bộ test và mở report.html
├── notes.md             # ghi chú kiến thức XPath, CSS, Tag Name, WebElement, sorted()
├── pytest.ini           # cấu hình pytest + pytest-html
├── report.html          # báo cáo kết quả (tự sinh khi chạy test)
├── requirements.txt     # selenium, pytest, pytest-html
├── test_w1.py           # mã kiểm thử
└── testcases.md         # bảng mô tả 11 test case
```

## Cách chạy

Yêu cầu: Python 3.9+ và trình duyệt Google Chrome (Selenium 4 tự tải ChromeDriver phù hợp).

1. Chạy `cai_dat.bat` (hoặc `pip install -r requirements.txt`).
2. Chạy `chay_kiem_thu.bat` (hoặc `pytest`). Kết quả ghi vào `report.html`, ảnh chụp lưu ở `anh/`.
3. Muốn chạy ẩn trình duyệt: `set HEADLESS=1` rồi `pytest`.
4. Chạy riêng 1 test: `pytest -k tc06` hoặc `pytest -k "tc04 and Due"`.

## Tóm tắt test case

| Mã | Nội dung | Số test |
|---|---|---|
| TC01 | Mở trang, có đúng 2 bảng `table1`, `table2` | 1 |
| TC02 | Bảng 1 có 6 cột đúng tên, 4 dòng × 6 ô | 1 |
| TC03 | Tìm dòng "Doe" bằng XPath, kiểm tra dữ liệu dòng | 1 |
| TC04 | Bảng 1: bấm 1 lần → tăng dần (5 cột, XPath) | 5 |
| TC05 | Bảng 1: bấm 2 lần → giảm dần (5 cột, XPath) | 5 |
| TC06 | Cột Due sắp theo số ($51 < $100), không theo chữ | 1 |
| TC07 | Bảng 2: tăng rồi giảm dần (5 cột, CSS selector) | 5 |
| TC08 | Sắp xếp không làm lệch dữ liệu trong dòng | 1 |
| TC09 | Sắp xếp bảng 1 không ảnh hưởng bảng 2 | 1 |
| TC10 | Class của tiêu đề đổi sau mỗi lần bấm | 1 |
| TC11 | Cột Action có edit/delete, bấm edit → `#edit` | 1 |
| | **Tổng** | **23** |

Chi tiết từng bước và kết quả mong đợi: xem [testcases.md](testcases.md). Giải thích kiến thức: xem [notes.md](notes.md).
