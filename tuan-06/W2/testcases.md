# Test cases – Tuần 6, W2 (Dropdown và Checkbox)

**Môn:** Kiểm thử phần mềm  
**Công cụ:** Python, Selenium, pytest  
**Website:** https://the-internet.herokuapp.com/  
**Phân công:** T6 – W2 – Danh sách chọn & ô đánh dấu

## Điều kiện trước kiểm thử

- Máy có Python, Chrome, Internet và các thư viện trong `requirements.txt`.
- Mỗi test khởi động trình duyệt mới, không phụ thuộc kết quả test khác.
- Kết quả thực tế cần lấy từ lần chạy, **không được đánh dấu PASSED trước**.

| Mã | Chức năng | Các bước | Kết quả mong đợi | Hàm Selenium |
|---|---|---|---|---|
| **TC01** | Dropdown – chọn theo text | Mở `/dropdown`, chọn `Option 1` theo chữ hiển thị | Mục được chọn có text `Option 1` | `Select`, `select_by_visible_text`, `By.ID`, `is_enabled` |
| **TC02** | Dropdown – chọn theo value | Mở `/dropdown`, chọn value `2` | Mục được chọn có value `2`, text `Option 2` | `select_by_value`, `get_attribute` |
| **TC03** | Dropdown – chọn theo index | Mở `/dropdown`, chọn index `1` | Mục được chọn có text `Option 1` | `select_by_index`, `By.CSS_SELECTOR` |
| **TC04** | Dropdown – đọc danh sách | Mở `/dropdown`, lấy các option | Có 3 mục (gồm mục mặc định); `Option 1` và `Option 2` đúng value | `options`, `get_attribute` |
| **TC05** | Checkbox 1 – tích | Mở `/checkboxes`, tìm ô thứ nhất rồi tích | `is_selected()` của ô 1 trả về `True` | `find_elements`, `click`, `is_selected`, `is_enabled` |
| **TC06** | Checkbox 2 – bỏ tích | Mở `/checkboxes`, bỏ tích ô thứ hai | `is_selected()` của ô 2 trả về `False` | `click`, `is_selected` |
| **TC07** | Checkbox – chọn cả hai | Mở `/checkboxes`, bảo đảm cả hai ô được tích | Cả 2 ô có `is_selected()` là `True` | `By.ID`, `find_elements`, `is_selected`, `click` |

## Những điểm cần giải thích khi giảng viên hỏi

- **Index bắt đầu từ 0:** Dropdown của trang mẫu có mục đầu tiên là lời nhắc lựa chọn. Vì vậy, `index=1` tương ứng `Option 1`.
- **Trạng thái ban đầu:** Checkbox 1 mặc định chưa tích; Checkbox 2 mặc định đã tích.
- **Vì sao dùng `assert`?** So sánh thực tế với kết quả mong đợi; không khớp thì test FAILED.
- **Vì sao mỗi test mở Chrome mới?** Giảm ảnh hưởng trạng thái giữa các test.
- **Vì sao không dùng `deselect_all()`?** Dropdown mẫu chỉ chọn một giá trị; phương thức đó chỉ dùng với dropdown hỗ trợ chọn nhiều.

## Ghi nhận kết quả

- **Trước khi chạy:** Chưa có kết quả thực tế.
- **Sau khi chạy:** Xem tổng PASSED/FAILED và chi tiết tại `report.html`; ảnh tại `anh/`.
- Nếu website hoặc HTML thay đổi, có thể cần cập nhật bộ test.
