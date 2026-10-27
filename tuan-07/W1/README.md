# Bài thực hành Kiểm thử phần mềm – Tuần 7, W1

**Nội dung:** Tải nội dung động (Dynamic Loading) – Chờ đúng lúc (Waits)  
**Công cụ:** Python, Selenium WebDriver, pytest, pytest-html, Chrome, VS Code, Git/GitHub  
**Nhánh tuần:** `week-07`  
**Trang được giao:**

- https://the-internet.herokuapp.com/dynamic_loading/1
- https://the-internet.herokuapp.com/dynamic_loading/2

## 1. Thư mục này gồm những gì?

```text
tuan-07/W1/
├── test_w1.py             # 8 test case Selenium + pytest
├── testcases.md           # Bảng test case và kết quả mong đợi
├── notes.md               # Giải thích lý thuyết Waits và Exceptions
├── README.md              # Hướng dẫn bạn đang đọc
├── requirements.txt       # Danh sách thư viện cần cài
├── pytest.ini             # Cấu hình pytest
├── cai_dat.bat            # Cài đặt lần đầu trên Windows
├── chay_kiem_thu.bat      # Chạy test và tạo báo cáo HTML
├── report.html            # Trang CHỜ CHẠY; sẽ được ghi đè sau khi test
└── anh/                   # Ảnh minh chứng tự tạo sau khi chạy
```

## 2. Chuẩn bị trước khi chạy

Máy Windows cần có:

1. **Python 3** (khuyến nghị Python 3.11 trở lên).
2. **Google Chrome**.
3. **VS Code** (để mở và chỉnh sửa bài).
4. **Internet** (để cài thư viện, driver và mở website thực hành).

## 3. Cách chạy

**Bước 1:** Giải nén `tuan-07_W1.zip` vào **thư mục gốc của repo** `kttd-05-N09` (cùng cấp với `tuan-06`). Sau khi giải nén sẽ có `kttd-05-N09\tuan-07\W1\`.

**Bước 2:** Mở VS Code → **File → Open Folder...** → chọn thư mục `kttd-05-N09`.

**Bước 3:** Vào `tuan-07\W1`, chạy **`cai_dat.bat`** một lần để tạo `.venv` và cài thư viện. Chờ thông báo `DONE`.

**Bước 4:** Chạy **`chay_kiem_thu.bat`**. Chrome sẽ mở 8 lần, mỗi lần có thể chờ khoảng 5–10 giây vì trang cố tình tải chậm. Tổng thời gian khoảng 1 phút.

**Bước 5:** Mở `report.html` để đọc kết quả **PASSED/FAILED**. Mở thư mục `anh/` để xem ảnh minh chứng tự động tạo ra.

### Nếu thích chạy bằng Terminal của VS Code

Mở Terminal bằng **Ctrl + `** (phím dấu huyền), rồi nhập:

```powershell
cd tuan-07\W1
.\cai_dat.bat
.\chay_kiem_thu.bat
```

Sau khi cài xong, có thể chạy trực tiếp:

```powershell
.\.venv\Scripts\python.exe -m pytest test_w1.py -v -s --html=report.html --self-contained-html
```

Chỉ chạy một test để luyện tập:

```powershell
.\.venv\Scripts\python.exe -m pytest test_w1.py::test_tc01_vd1_cho_phan_tu_an_hien_ra -v -s
```

## 4. Kết quả dự kiến và minh chứng

Nếu website, Chrome và chương trình đều hoạt động đúng, kết quả **dự kiến** là `8 passed`.

**Đây KHÔNG phải kết quả đã được kiểm chứng trên máy bạn.** Trong ZIP, `report.html` là trang thông báo **CHƯA CHẠY KIỂM THỬ**. Chỉ sau khi bạn chạy `chay_kiem_thu.bat`, file này mới được pytest-html thay thế bằng báo cáo từ lần chạy thật.

Chương trình cố gắng lưu 1 ảnh PNG vào `anh/` cho mỗi test có mở được trình duyệt, kể cả khi test FAILED.

## 5. Cách đưa lên GitHub (nhánh `week-07`)

Làm **sau khi** đã chạy test và có `report.html` + ảnh thật. Mở Terminal tại thư mục `kttd-05-N09`:

```powershell
git fetch origin
git switch tuan-06
git pull origin tuan-06
git switch -c week-07
```

> Nên tạo nhánh `week-07` **trước khi** giải nén bài vào repo. Nếu đã giải nén rồi cũng không sao: thư mục `tuan-07` chưa được commit nên sẽ đi theo sang nhánh mới.

```powershell
git status
git add tuan-07
git commit -m "Hoan thanh bai kiem thu W1 Tuan 7"
git push -u origin week-07
```

`.venv/`, `__pycache__/` và `.pytest_cache/` được loại khỏi GitHub nhờ `.gitignore` ở thư mục gốc repo.

## 6. Bám sát tài liệu giảng viên

| Mục | Kiến thức sử dụng | Test case |
|---|---|---|
| **5.1** Explicit Waits | `WebDriverWait`, `until`, `EC.visibility_of_element_located`, `EC.presence_of_element_located`, `EC.invisibility_of_element_located` | TC01 – TC05 |
| **5.2** Implicit Waits | `implicitly_wait` | TC06 – TC08 |
| **7.1** Exceptions | `TimeoutException`, `NoSuchElementException` | TC04, TC05, TC08 |
| pytest | `pytest.raises` để kiểm tra lỗi mong đợi | TC04, TC05, TC08 |

## 7. Nếu gặp lỗi

- **Không tìm thấy Python:** Cài Python, đóng/mở lại Terminal.
- **Không mở được Chrome:** Kiểm tra Chrome đã cài và cập nhật.
- **Không tải được driver hoặc website:** Kiểm tra Internet, thử mở URL bằng Chrome.
- **`TimeoutException` ở TC01/TC02/TC03:** Mạng chậm hoặc website phản hồi chậm. Chạy lại; nếu vẫn lỗi, thử tăng `THOI_GIAN_CHO` trong `test_w1.py` (ví dụ 15).
- **`NoSuchElementException`:** Trang có thể chưa tải hoặc cấu trúc HTML đã thay đổi.
- **Test FAIL:** Đọc thông báo lỗi và tìm nguyên nhân; không xóa `assert` chỉ để ép kết quả PASS.
