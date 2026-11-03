# Tuần 8 – W1: Di chuột & thanh trượt

Kiểm thử tự động bằng Selenium Python + pytest cho hai trang của
[the-internet](https://the-internet.herokuapp.com):

- `/hovers`: chú thích chỉ hiện khi rê chuột lên ảnh
- `/horizontal_slider`: thanh trượt 0 → 5, bước 0.5

Mục tài liệu selenium-python: 3.3 Drag and drop, 7.2 Action Chains,
7.4 Special Keys, 7.20 WebElement.

## Cấu trúc

```
week-08/
├── conftest.py                    # fixture driver, tuỳ chọn --headless, cấu hình báo cáo HTML
├── pytest.ini                     # mặc định xuất reports/week08_report.html
├── requirements.txt
└── tests/
    ├── test_hovers.py             # TC_HOV_01 → TC_HOV_05 (9 test)
    └── test_horizontal_slider.py  # TC_SLD_01 → TC_SLD_08 (11 test)
```

## Cài đặt

Cần Python 3.9+ và Google Chrome. Selenium 4.6 trở lên tự tải chromedriver, không cần cài tay.

```bash
python -m venv venv
venv\Scripts\activate          # Windows  (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
```

## Chạy test

```bash
pytest                         # mở Chrome có giao diện, xem được từng thao tác
pytest --headless              # chạy ẩn, nhanh và ổn định hơn
pytest tests/test_hovers.py    # chỉ chạy một file
```

Báo cáo HTML nằm ở `reports/week08_report.html`, mở bằng trình duyệt.
Báo cáo có cột "Mô tả" cho từng test và ảnh màn hình cuối mỗi test (bấm vào dòng để xem).

Khi chạy có giao diện, đừng rê chuột thật vào cửa sổ Chrome, vì chuột thật cũng làm đổi
trạng thái hover và có thể làm test hover sai.

## Danh sách test case

| ID | Mô tả | Kỹ thuật |
|---|---|---|
| TC_HOV_01 | 3 ảnh, chưa hover thì chú thích ẩn | Kiểm tra trạng thái ban đầu |
| TC_HOV_02 | Hover ảnh N hiện "name: userN" (N = 1, 2, 3) | Phân vùng tương đương |
| TC_HOV_03 | Mỗi lần chỉ hiện một chú thích | Chuyển trạng thái |
| TC_HOV_04 | Rời chuột thì chú thích ẩn | Chuyển trạng thái |
| TC_HOV_05 | "View profile" dẫn tới /users/N | Kiểm tra liên kết |
| TC_SLD_01 | Giá trị ban đầu là 0 | Giá trị biên dưới |
| TC_SLD_02 | HOME + ARROW_RIGHT x n → 0.5, 2.5, 4.5, 5.0 | Giá trị biên |
| TC_SLD_03 | Bấm quá nhiều vẫn dừng ở 5 | Vượt biên trên |
| TC_SLD_04 | Ở 0 bấm ARROW_LEFT vẫn là 0 | Vượt biên dưới |
| TC_SLD_05 | click_and_hold tại tâm → 2.5 | Chuột |
| TC_SLD_06 | Kéo qua mép phải → 5 | Chuột, vượt biên |
| TC_SLD_07 | drag_and_drop_by_offset sang trái → 0 | Chuột, vượt biên |
| TC_SLD_08 | Kéo 1/4 chiều rộng → giá trị trong (2.5; 5) | Chuột, kiểm tra theo khoảng |

Mọi test thanh trượt đều kiểm tra thêm: số hiển thị bên phải (`#range`) khớp với giá trị thật
của thanh (`get_attribute("value")`).

## Đưa lên nhánh week-08

Chép thư mục này vào repo của nhóm rồi:

```bash
git checkout -b week-08
git add .
git commit -m "Tuan 8 - W1: hovers, horizontal slider, bao cao HTML"
git push -u origin week-08
```

Nên thêm `reports/` và `venv/` vào `.gitignore` nếu nhóm không muốn đẩy báo cáo lên repo.
