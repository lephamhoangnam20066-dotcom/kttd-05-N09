# Bài thực hành Kiểm thử phần mềm – Tuần 6, W2

**Nội dung:** Dropdown (danh sách chọn) và Checkbox (ô đánh dấu)  
**Công cụ:** Python, Selenium WebDriver, pytest, pytest-html, Chrome, VS Code, Git/GitHub  
**Trang được giao:**

- https://the-internet.herokuapp.com/dropdown
- https://the-internet.herokuapp.com/checkboxes

## 1. Thư mục này gồm những gì?

```text
KiemThu_Tuan6_W2/
├── test_w2.py             # 7 test case Selenium + pytest
├── testcases.md           # Bảng test case và kết quả mong đợi
├── notes.md               # Giải thích lý thuyết, hàm Selenium
├── README.md              # Hướng dẫn bạn đang đọc
├── requirements.txt       # Danh sách thư viện cần cài
├── pytest.ini             # Cấu hình pytest
├── cai_dat.bat            # Cài đặt lần đầu trên Windows
├── chay_kiem_thu.bat      # Chạy test và tạo báo cáo HTML
├── report.html            # Trang CHỜ CHẠY; sẽ được ghi đè sau khi test
├── anh/                   # Ảnh minh chứng tự tạo sau khi chạy
└── .gitignore             # Không đưa môi trường ảo lên GitHub
```

## 2. Chuẩn bị trước khi chạy

Máy Windows cần có:

1. **Python 3** (khuyến nghị Python 3.11 trở lên).
2. **Google Chrome**.
3. **VS Code** (để mở và chỉnh sửa bài).
4. **Internet** (để cài thư viện, driver và mở website thực hành).

## 3. Cách chạy dễ nhất cho người mới

**Bước 1:** Giải nén file `KiemThu_Tuan6_W2.zip`.

**Bước 2:** Mở VS Code → chọn **File → Open Folder...** → chọn thư mục `KiemThu_Tuan6_W2`.

**Bước 3:** Trong thư mục vừa giải nén, chạy file **`cai_dat.bat`** một lần để tạo `.venv` và cài thư viện. Chờ thông báo `DONE`.

**Bước 4:** Chạy **`chay_kiem_thu.bat`** để mở Chrome, thực hiện các test, tạo báo cáo.

**Bước 5:** Mở `report.html` để đọc kết quả **PASSED/FAILED**. Mở thư mục `anh/` để xem ảnh minh chứng tự động tạo ra.

> **Lưu ý:** Nếu Windows hỏi có cho phép chạy file `.bat` hay không, hãy xác nhận đó là file từ ZIP bạn vừa tải. Hai file này chỉ thực hiện các lệnh Python/pytest và cài thư viện cần thiết.

### Nếu thích chạy bằng Terminal của VS Code

Mở Terminal bằng **Ctrl + `** (phím dấu huyền), rồi nhập:

```powershell
.\cai_dat.bat
.\chay_kiem_thu.bat
```

Sau khi cài xong, có thể chạy trực tiếp:

```powershell
.\.venv\Scripts\python.exe -m pytest test_w2.py -v -s --html=report.html --self-contained-html
```

Chỉ chạy test đầu tiên để luyện tập:

```powershell
.\.venv\Scripts\python.exe -m pytest test_w2.py::test_tc01_dropdown_chon_bang_text -v -s
```

## 4. Kết quả dự kiến và minh chứng

Nếu website, Chrome và chương trình đều hoạt động đúng, kết quả **dự kiến** là `7 passed`.

**Đây KHÔNG phải kết quả đã được kiểm chứng.** Trong ZIP, `report.html` là trang thông báo **CHƯA CHẠY KIỂM THỬ**. Chỉ sau khi bạn chạy `chay_kiem_thu.bat`, file này mới được pytest-html thay thế bằng báo cáo từ lần chạy thật.

Chương trình cố gắng lưu 1 ảnh PNG vào `anh/` cho mỗi test có mở được trình duyệt, kể cả khi test FAILED. Nếu Chrome không mở được thì không thể có ảnh.

## 5. Cách đưa lên GitHub

Sau khi xem báo cáo, tại Terminal ở thư mục dự án:

```powershell
git init
git add .
git commit -m "Tuan 6 W2 - Kiem thu dropdown va checkbox"
```

Sau đó tạo **repository trống** trên GitHub rồi chạy (đổi URL thành repo của bạn):

```powershell
git branch -M main
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin main
```

` .venv/ ` được loại khỏi GitHub nhờ `.gitignore`. Nếu Git hỏi tên/email hoặc yêu cầu đăng nhập, hãy cấu hình Git và xác thực tài khoản của bạn trước.

## 6. Bám sát tài liệu giảng viên

| Mục | Kiến thức sử dụng |
|---|---|
| **3.2** | `Select`, `select_by_visible_text`, `select_by_value`, `select_by_index`, `options` |
| **4.1** | `By.ID` |
| **4.2** | `By.NAME` – ghi chú lý thuyết, không tự giả định tên trên website |
| **4.7** | `By.CSS_SELECTOR` |
| **7.20** | `find_element`, `find_elements`, `click`, `is_selected`, `is_enabled`, `is_displayed`, `get_attribute` |

`By.NAME` chỉ dùng khi HTML **thực sự có thuộc tính `name`**. Trong các phần tử mà bài test cần thao tác trên hai trang W2, ta dùng ID/CSS Selector phù hợp; phần Name có ví dụ trong `notes.md`.

## 7. Nếu gặp lỗi

- **Không tìm thấy Python:** Cài Python, đóng/mở lại Terminal.
- **Không mở được Chrome:** Kiểm tra Chrome đã cài và cập nhật.
- **Không tải được driver hoặc website:** Kiểm tra Internet, thử mở URL bằng Chrome.
- **`NoSuchElementException`:** Trang có thể chưa tải hoặc cấu trúc HTML đã thay đổi.
- **Test FAIL:** Đọc thông báo lỗi và tìm nguyên nhân; không xóa `assert` chỉ để ép kết quả PASS.

Mỗi lần cần trợ giúp, bạn có thể gửi ảnh **Terminal** hoặc nội dung lỗi để tiếp tục theo từng bước.
