# Ghi chú học tập – Selenium Python Tuần 7 / W1

## Kiến thức theo tài liệu giảng viên

| Mục | Nội dung | Ví dụ |
|---|---|---|
| **5.1** | Explicit Waits | `WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "finish")))` |
| **5.2** | Implicit Waits | `driver.implicitly_wait(10)` rồi `driver.find_element(By.ID, "finish")` |
| **7.1** | Exceptions | `TimeoutException`, `NoSuchElementException` |
| pytest | Kiểm tra lỗi mong đợi | `with pytest.raises(TimeoutException): ...` |

## Các khái niệm nền tảng

- **Nội dung động (dynamic loading):** Trang không tải lại, nhưng JavaScript ẩn/hiện hoặc thêm phần tử sau một khoảng thời gian.
- **DOM:** Cây HTML hiện tại của trang. Phần tử có thể **có trong DOM nhưng bị ẩn**.
- **Explicit wait (chờ tường minh):** Chờ **một điều kiện cụ thể** tại **một chỗ cụ thể** trong code. Mặc định kiểm tra lại mỗi 500 ms; hết giờ thì báo `TimeoutException`.
- **Implicit wait (chờ ngầm định):** Đặt **một lần** cho driver; mọi lệnh `find_element`/`find_elements` sẽ thử lại đến hết thời gian nếu chưa tìm thấy. Mặc định là 0 và có hiệu lực suốt đời driver.
- **Expected Condition (EC):** Điều kiện có sẵn trong `selenium.webdriver.support.expected_conditions`.

## Ba điều kiện dùng trong bài

| Điều kiện | Đúng khi nào | Trả về |
|---|---|---|
| `EC.presence_of_element_located(locator)` | Phần tử **có trong DOM** (ẩn hay hiện đều được) | WebElement |
| `EC.visibility_of_element_located(locator)` | Phần tử có trong DOM **và đang hiển thị** (kích thước > 0) | WebElement |
| `EC.invisibility_of_element_located(locator)` | Phần tử **bị ẩn** hoặc **không còn trong DOM** | WebElement hoặc `True` |

## Ví dụ nhanh

```python
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 5.1 – Chờ tối đa 10 giây đến khi "Hello World!" hiển thị
wait = WebDriverWait(driver, 10)
hello = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish h4")))

# 5.1 – Chờ "Loading..." biến mất
wait.until(EC.invisibility_of_element_located((By.ID, "loading")))

# 5.2 – Implicit wait: đặt 1 lần cho cả driver
driver.implicitly_wait(10)
finish = driver.find_element(By.ID, "finish")

# 7.1 + pytest – Hết giờ là kết quả mong đợi
with pytest.raises(TimeoutException):
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "finish")))
```

## So sánh Explicit Wait và Implicit Wait

| | Explicit Wait (5.1) | Implicit Wait (5.2) |
|---|---|---|
| Cách đặt | Tạo `WebDriverWait` tại chỗ cần chờ | `driver.implicitly_wait(giây)` một lần |
| Chờ điều gì | Bất kỳ điều kiện nào: hiển thị, biến mất, click được... | Chỉ chờ phần tử **có mặt** trong DOM |
| Hết giờ | `TimeoutException` | `NoSuchElementException` |
| Dùng tốt cho | Ví dụ 1 (phần tử ẩn) **và** Ví dụ 2 | Ví dụ 2 (phần tử được thêm vào). **Không** đủ cho Ví dụ 1 |

## Lưu ý quan trọng

- **Không dùng `time.sleep()` để chờ trang.** Tài liệu 5.1 gọi đây là trường hợp cực đoan: luôn chờ cứng một khoảng thời gian, chậm và dễ lỗi.
- **Không trộn implicit wait và explicit wait trên cùng một driver.** Tài liệu Selenium khuyến cáo việc trộn có thể làm thời gian chờ khó đoán. Trong bài, mỗi test có Chrome riêng: Phần A chỉ dùng explicit wait, Phần B chỉ dùng implicit wait.
- **Selenium chỉ đọc chữ đang hiển thị:** phần tử bị ẩn có `element.text == ""` (TC07).
- **Thông báo lỗi tự viết:** `wait.until(điều_kiện, message="...")` giúp đọc lỗi dễ hơn khi test FAILED (TC04).
- `assert` sai thì pytest đánh dấu test là **FAILED**; `pytest.raises` không thấy lỗi xảy ra cũng làm test **FAILED**.
- Ảnh và báo cáo cần đến từ lần chạy thật, không tự ghi trước kết quả PASSED.
