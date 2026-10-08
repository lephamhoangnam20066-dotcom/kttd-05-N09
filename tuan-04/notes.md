# Ghi chú tuần 04 – N09

## Mục tiêu
Thực hành ba trường hợp kiểm thử đăng nhập bằng Selenium và pytest. Bài luyện tập phỏng theo ví dụ tuần 05 trong tài liệu của giảng viên, không phải đề tuần 04 được xác nhận.

## Giải thích
- `webdriver.Chrome()`: mở Chrome để tự động thao tác.
- `driver.get(URL)`: truy cập trang đăng nhập.
- `By.ID`, `By.CSS_SELECTOR`: xác định các phần tử giao diện.
- `WebDriverWait`: chờ phần tử xuất hiện, hạn chế lỗi do trang tải chậm.
- `send_keys`: nhập dữ liệu kiểm thử.
- `click`: nhấn nút đăng nhập.
- `assert`: đối chiếu kết quả thực tế với kết quả mong đợi.
- `@pytest.fixture`: khởi tạo và đóng trình duyệt cho từng bài kiểm thử.

## Kết quả thực hành
Chưa chạy trên máy của sinh viên. Sau khi chạy, ghi lại ngày chạy, số bài PASS/FAIL, phiên bản Chrome và đường dẫn ảnh kết quả.

## AI hỗ trợ
AI hỗ trợ soạn bài kiểm thử mẫu và giải thích. Sinh viên cần tự chạy, đọc hiểu, kiểm tra và cập nhật kết quả thực tế trước khi nộp.
