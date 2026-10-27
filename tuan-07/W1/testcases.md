# Test cases – Tuần 7, W1 (Tải nội dung động – Chờ đúng lúc)

**Môn:** Kiểm thử phần mềm  
**Công cụ:** Python, Selenium, pytest  
**Website:** https://the-internet.herokuapp.com/dynamic_loading/1 và https://the-internet.herokuapp.com/dynamic_loading/2  
**Phân công:** T7 – W1 – Tải nội dung động (nhánh tuần: `week-07`)

## Hai trang được kiểm thử

| Trang | Trước khi bấm Start | Sau khi bấm Start |
|---|---|---|
| **Ví dụ 1** `/dynamic_loading/1` | `#finish` **đã có trong DOM** nhưng bị ẩn (`display:none`) | Hiện `Loading...` khoảng 5 giây, sau đó `#finish` được **hiện ra** |
| **Ví dụ 2** `/dynamic_loading/2` | `#finish` **chưa có trong DOM** | Hiện `Loading...` khoảng 5 giây, sau đó `#finish` mới được **thêm vào** trang |

## Điều kiện trước kiểm thử

- Máy có Python, Chrome, Internet và các thư viện trong `requirements.txt`.
- Mỗi test khởi động trình duyệt mới (implicit wait mặc định = 0), không phụ thuộc kết quả test khác.
- Kết quả thực tế cần lấy từ lần chạy, **không được đánh dấu PASSED trước**.

| Mã | Chức năng | Các bước | Kết quả mong đợi | Kiến thức sử dụng |
|---|---|---|---|---|
| **TC01** | VD1 – chờ phần tử ẩn hiện ra | Mở `/dynamic_loading/1`, kiểm tra `#finish` đang ẩn, bấm Start, chờ tối đa 10 giây | `Hello World!` hiển thị; thời gian chờ thực tế < 10 giây | `WebDriverWait`, `until`, `EC.visibility_of_element_located` |
| **TC02** | VD2 – chờ phần tử được thêm vào DOM | Mở `/dynamic_loading/2`, kiểm tra chưa có `#finish`, bấm Start, chờ có mặt rồi chờ hiển thị | `#finish` có trong DOM và hiện `Hello World!` | `find_elements`, `EC.presence_of_element_located`, `EC.visibility_of_element_located` |
| **TC03** | Chờ `Loading...` biến mất | Mở `/dynamic_loading/1`, bấm Start, chờ `#loading` hiện rồi chờ nó biến mất | `#loading` có chữ `Loading`, sau đó biến mất; `#finish` hiển thị; nút Start bị ẩn | `EC.visibility_of_element_located`, `EC.invisibility_of_element_located` |
| **TC04** | Không bấm Start → hết giờ | Mở `/dynamic_loading/2`, **không** bấm Start, chờ `#finish` tối đa 2 giây | Phát sinh `TimeoutException` có thông báo `Khong thay #finish` | `WebDriverWait`, `TimeoutException`, `pytest.raises` |
| **TC05** | Chờ quá ngắn → hết giờ | Mở `/dynamic_loading/1`, bấm Start, chờ 2 giây; sau đó chờ lại 10 giây | Lần 1: `TimeoutException`. Lần 2: thấy `Hello World!` | `TimeoutException`, `pytest.raises`, `EC.visibility_of_element_located` |
| **TC06** | Implicit wait – VD2 | Đặt `implicitly_wait(10)`, mở `/dynamic_loading/2`, bấm Start, `find_element(#finish)` | `find_element` tự chờ đến khi có `#finish`; chữ là `Hello World!` | `implicitly_wait`, `find_element` |
| **TC07** | Implicit wait – VD1 (hạn chế) | Đặt `implicitly_wait(10)`, mở `/dynamic_loading/1`, bấm Start, `find_element(#finish)` ngay | Trả về **ngay** (< 3 giây) nhưng phần tử **chưa hiển thị**, `text` rỗng | `implicitly_wait`, `is_displayed`, `text` |
| **TC08** | Implicit wait hết giờ | Đặt `implicitly_wait(2)`, mở `/dynamic_loading/2`, **không** bấm Start, `find_element(#finish)` | Phát sinh `NoSuchElementException` sau khoảng 2 giây | `implicitly_wait`, `NoSuchElementException`, `pytest.raises` |

## Những điểm cần giải thích khi giảng viên hỏi

- **Presence khác Visibility:** `presence_of_element_located` chỉ cần phần tử **có trong DOM**; `visibility_of_element_located` cần phần tử **có trong DOM và đang hiển thị**. Ở Ví dụ 1, `#finish` có mặt ngay từ đầu, nên chỉ chờ presence là **sai**.
- **Vì sao TC07 vẫn PASSED?** TC07 chứng minh hạn chế của implicit wait: nó chỉ chờ phần tử **có mặt**, không chờ **hiển thị**. Test kiểm tra đúng hành vi đó (phần tử trả về ngay, `text` rỗng).
- **`invisibility_of_element_located`** trả về kết quả đúng khi phần tử bị ẩn **hoặc** không còn trong DOM. `#loading` chỉ được chèn vào sau khi bấm Start, vì vậy TC03 phải chờ nó **hiện** trước rồi mới chờ nó **biến mất**.
- **`TimeoutException` khác `NoSuchElementException`:** Explicit wait hết giờ thì báo `TimeoutException`; `find_element` hết implicit wait mà vẫn không thấy thì báo `NoSuchElementException`.
- **Vì sao dùng `pytest.raises`?** Trong TC04, TC05, TC08 lỗi là **kết quả mong đợi**. `pytest.raises` làm test PASSED khi đúng loại lỗi xảy ra, và FAILED nếu lỗi **không** xảy ra.
- **Vì sao không dùng `time.sleep(5)`?** `sleep` luôn chờ đủ thời gian, trang nhanh vẫn chờ, trang chậm hơn 5 giây thì test lỗi. `WebDriverWait` kiểm tra lại mỗi 0,5 giây và dừng ngay khi điều kiện đúng (TC01 in ra thời gian chờ thực tế).

## Ghi nhận kết quả

- **Trước khi chạy:** Chưa có kết quả thực tế.
- **Sau khi chạy:** Xem tổng PASSED/FAILED và chi tiết tại `report.html`; ảnh tại `anh/`.
- Nếu website hoặc HTML thay đổi, có thể cần cập nhật bộ test.
