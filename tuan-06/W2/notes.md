# Ghi chú học tập – Selenium Python Tuần 6 / W2

## Kiến thức theo tài liệu giảng viên

| Mục | Nội dung | Ví dụ |
|---|---|---|
| **3.2** | Filling in forms | `Select`, `select_by_index`, `select_by_visible_text`, `select_by_value`, `options` |
| **4.1** | Locating by ID | `driver.find_element(By.ID, "dropdown")` |
| **4.2** | Locating by Name | `driver.find_element(By.NAME, "username")` nếu HTML có `name="username"` |
| **4.7** | CSS Selector | `driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")` |
| **7.20** | WebElement | `click`, `find_element`, `find_elements`, `get_attribute`, `is_selected`, `is_enabled`, `is_displayed` |

## Các khái niệm nền tảng

- **Dropdown:** Danh sách chọn, thường là phần tử `<select>` và các thẻ `<option>` bên trong.
- **Checkbox:** Ô tích chọn hoặc bỏ tích; `click()` thay đổi trạng thái hiện tại.
- **WebElement:** Đối tượng Selenium đại diện cho phần tử HTML đã tìm thấy.
- **Locator:** Cách tìm phần tử bằng ID, Name, CSS Selector...
- **Assertion:** Lệnh `assert` để kiểm tra kết quả thực tế so với mong đợi.
- **Pytest fixture:** Trong bài này là hàm `driver`, tạo Chrome trước mỗi test, chụp ảnh và đóng Chrome sau test.

## Ví dụ nhanh

```python
# 4.1 – Tìm theo id="dropdown"
driver.find_element(By.ID, "dropdown")

# 4.2 – Tìm theo name="username" nếu THỰC SỰ có thuộc tính này
driver.find_element(By.NAME, "username")

# 4.7 – Tìm tất cả thẻ input checkbox
driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")

# 7.20 – Đọc trạng thái, thao tác
checkbox.is_selected()  # True hoặc False
checkbox.is_enabled()   # True hoặc False
checkbox.get_attribute("type")  # "checkbox"
checkbox.click()
```

**Lưu ý về By.NAME:** Trong hai trang demo W2, những phần tử ta kiểm thử không cần locator `By.NAME`. Không tự đặt giá trị Name trong code nếu HTML không có thuộc tính đó. Ví dụ trên chỉ minh họa lý thuyết ở mục 4.2.

## Tìm phần tử và kiểm tra

- `find_element()` trả về **một** WebElement, không tìm thấy sẽ có `NoSuchElementException`.
- `find_elements()` trả về **danh sách**; nếu không có phần tử sẽ trả về danh sách rỗng.
- `is_selected()` dùng kiểm tra trạng thái ô chọn; `is_enabled()` kiểm tra có thể tương tác.
- `get_attribute("value")` lấy giá trị thuộc tính/property của option.
- Khi muốn **tích** một checkbox, nên kiểm tra `if not checkbox.is_selected(): checkbox.click()` để tránh vô tình bỏ tích ô đã chọn.
- `Select.deselect_all()` chỉ dùng khi dropdown cho phép chọn nhiều mục (`multiple`).
- `assert` sai làm pytest đánh dấu test là **FAILED**.
- Ảnh và báo cáo cần đến từ lần chạy thật, không tự ghi trước kết quả PASSED.
