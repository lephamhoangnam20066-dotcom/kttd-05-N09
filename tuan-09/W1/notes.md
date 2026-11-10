# Ghi chú kiến thức – Tuần 9, W1: Sortable Data Tables

## 1. Trang `/tables` có gì?

Trang có 2 bảng chứa **cùng dữ liệu** (4 người: Smith, Bach, Doe, Conway) nhưng viết HTML khác nhau:

| | Example 1 – `#table1` | Example 2 – `#table2` |
|---|---|---|
| Class/id trên ô | **Không có** | Có: `last-name`, `first-name`, `email`, `dues`, `web-site`, `action` |
| Cách tìm ô hợp lý | XPath theo **vị trí** `td[n]` hoặc theo nội dung | CSS selector theo **class**: `#table2 tbody td.dues` |

Bấm vào tiêu đề cột (plugin jQuery tablesorter) thì bảng sắp xếp lại: bấm lần 1 tăng dần, bấm lần 2 giảm dần. Ô `th` được gắn thêm class `headerSortUp` / `headerSortDown` để thể hiện trạng thái.

## 2. `find_element` và `find_elements` (mục 4 – Locating Elements)

| | `find_element` | `find_elements` |
|---|---|---|
| Trả về | 1 `WebElement` | `list` các `WebElement` |
| Không tìm thấy | Ném `NoSuchElementException` | Trả về **list rỗng** `[]` |
| Dùng khi | Chỉ cần 1 phần tử | Đọc cả cột, cả dòng, đếm số phần tử |

Với bảng ta gần như luôn dùng `find_elements` để lấy **cả cột** rồi chuyển thành list chuỗi:

```python
cac_o = driver.find_elements(By.XPATH, "//table[@id='table1']/tbody/tr/td[1]")
gia_tri = [o.text for o in cac_o]   # ['Smith', 'Bach', 'Doe', 'Conway']
```

## 3. Ba cách định vị dùng trong bài

### 3.1 By.XPATH (mục 4.3)

```python
# Tất cả tiêu đề cột của bảng 1
"//table[@id='table1']/thead/tr/th"
# Ô tiêu đề có span chứa đúng chữ 'Due'
"//table[@id='table1']/thead//th[span[normalize-space()='Due']]"
# Cột thứ 4 (Due) – XPath đếm từ 1, không phải từ 0
"//table[@id='table1']/tbody/tr/td[4]"
# Dòng có ô đầu tiên = 'Doe' (lọc dòng theo nội dung)
"//table[@id='table1']/tbody/tr[td[1]='Doe']"
```

XPath mạnh ở chỗ **lọc theo nội dung** và **theo vị trí**, nên hợp với bảng 1 (không có class).

### 3.2 By.TAG_NAME (mục 4.5)

Tìm theo tên thẻ: `table`, `tr`, `td`, `a`. Hay dùng để **duyệt lồng nhau**: lấy các `tr`, rồi trong từng `tr` lấy các `td`.

```python
than_bang = driver.find_element(By.CSS_SELECTOR, "#table1 tbody")
for dong in than_bang.find_elements(By.TAG_NAME, "tr"):
    print([o.text for o in dong.find_elements(By.TAG_NAME, "td")])
```

Lưu ý: gọi `find_elements` trên **một WebElement** thì chỉ tìm bên trong phần tử đó, không tìm cả trang.

### 3.3 By.CSS_SELECTOR (mục 4.7)

```python
"#table2 thead span.dues"   # tiêu đề cột Due của bảng 2
"#table2 tbody td.dues"     # mọi ô của cột Due trong bảng 2
"#table1 tbody tr"          # mọi dòng dữ liệu của bảng 1
```

`#` = id, `.` = class, dấu cách = phần tử con cháu. Ngắn và dễ đọc hơn XPath khi trang có class rõ ràng.

## 4. WebElement (mục 7.20)

| Thuộc tính / hàm | Dùng trong bài |
|---|---|
| `.text` | Đọc chữ hiển thị trong ô |
| `.click()` | Bấm tiêu đề cột để sắp xếp, bấm link `edit` |
| `.get_attribute("class")` | Đọc class của `th` để biết trạng thái sắp xếp |
| `.get_attribute("id")` | Lấy id của bảng |
| `.screenshot(path)` | Chụp riêng bảng, lưu vào thư mục `anh/` |
| `.find_elements(...)` | Tìm phần tử con bên trong (ô `td` trong 1 dòng) |

## 5. `sorted()` – cách kiểm tra bảng đã được sắp xếp đúng

```python
truoc = lay_cot(...)            # đọc trước khi bấm
tieu_de.click()
sau = lay_cot(...)              # đọc sau khi bấm
assert sau == sorted(truoc)                 # tăng dần
assert sau == sorted(truoc, reverse=True)   # giảm dần (bấm lần 2)
```

So với `sorted(truoc)` chứ không phải `sorted(sau)` để chắc rằng **không mất / thêm** giá trị nào sau khi sắp xếp.

### Bẫy 1 – cột tiền tệ phải so sánh theo số

So sánh chuỗi thì `'$100.00' < '$50.00'` (vì ký tự `'1' < '5'`) → sai. Phải đổi sang số:

```python
sorted(truoc, key=lambda x: float(x.replace("$", "")))
```

### Bẫy 2 – hoa/thường

So sánh chuỗi phân biệt hoa thường (`'Z' < 'a'`). Dùng `key=str.lower` cho chắc.

### Bẫy 3 – dữ liệu ban đầu đã có thứ tự sẵn

Nếu cột vốn đã tăng dần thì test "bấm → tăng dần" luôn đúng dù chức năng sắp xếp hỏng. Vì vậy TC04 kiểm tra thêm tiền điều kiện `truoc != sorted(truoc)`.

### Bẫy 4 – giá trị trùng nhau

Cột Due có 2 giá trị `$50.00`. Thứ tự giữa 2 dòng trùng giá trị có thể khác nhau, nên chỉ so sánh **danh sách giá trị** của cột, không so sánh thứ tự từng dòng.

### Bẫy 5 – trang sắp xếp bất đồng bộ (lỗi "lúc xanh lúc đỏ")

Trang dùng jQuery tablesorter. Khi bấm tiêu đề, nó **không sắp xếp ngay** mà đẩy việc sắp xếp vào `setTimeout(..., 1)`. Nếu đọc bảng ngay sau `.click()`, Selenium có thể đọc phải thứ tự **cũ** → mỗi lần chạy lại đỏ ở một test khác nhau.

Lần chạy đầu của nhóm gặp đúng lỗi này: 7 failed, ví dụ TC07 bấm lần 2 mà vẫn đọc ra thứ tự tăng dần.

Cách sửa: sau khi bấm thì **chờ tường minh** (explicit wait) bằng `WebDriverWait`. Tablesorter đổi class của `<th>` và sắp lại các dòng trong cùng một lần chạy, nên chờ class đổi là chắc chắn bảng đã sắp xong:

```python
def bam_tieu_de(driver, th):
    class_cu = th.get_attribute("class")
    th.click()
    WebDriverWait(driver, 5).until(lambda _: th.get_attribute("class") != class_cu)
```

Không dùng `time.sleep()`: chờ cố định thì hoặc thừa thời gian, hoặc vẫn thiếu khi máy chậm.

## 6. Ngoài sắp xếp còn kiểm tra gì?

- **Toàn vẹn dòng (TC08):** sắp xếp chỉ đổi thứ tự dòng, không được làm lệch dữ liệu giữa các cột.
- **Độc lập giữa 2 bảng (TC09):** sắp xếp bảng 1 không làm thay đổi bảng 2.
- **Trạng thái tiêu đề (TC10):** class của `th` thay đổi sau mỗi lần bấm.
- **Cột Action (TC11):** mỗi dòng có link `edit`, `delete`; bấm `edit` → URL có `#edit`.

## Tài liệu tham khảo

- 4.3 Locating by XPath – https://selenium-python.readthedocs.io/locating-elements.html#locating-by-xpath
- 4.5 Locating Elements by Tag Name – https://selenium-python.readthedocs.io/locating-elements.html#locating-elements-by-tag-name
- 4.7 Locating Elements by CSS Selectors – https://selenium-python.readthedocs.io/locating-elements.html#locating-elements-by-css-selectors
- 7.20 WebElement – https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webelement
