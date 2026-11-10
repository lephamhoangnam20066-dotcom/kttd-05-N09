# Test case – Tuần 9, W1: Bảng dữ liệu sắp xếp được (Sortable Data Tables)

- **Trang kiểm thử:** https://the-internet.herokuapp.com/tables
- **Tiền điều kiện chung:** mở Chrome, truy cập trang `/tables`, chờ bảng `#table1` hiển thị. Trước mỗi test trang được tải lại để bảng về thứ tự ban đầu.
- **Dữ liệu ban đầu của bảng (cả 2 bảng giống nhau):**

| Last Name | First Name | Email | Due | Web Site |
|---|---|---|---|---|
| Smith | John | jsmith@gmail.com | $50.00 | http://www.jsmith.com |
| Bach | Frank | fbach@yahoo.com | $51.00 | http://www.frank.com |
| Doe | Jason | jdoe@hotmail.com | $100.00 | http://www.jdoe.com |
| Conway | Tim | tconway@earthlink.net | $50.00 | http://www.timconway.com |

## Danh sách test case

| Mã | Tên test case | Các bước | Locator / kỹ thuật | Kết quả mong đợi | Hàm test |
|---|---|---|---|---|---|
| TC01 | Mở trang có 2 bảng | 1. Mở `/tables` 2. Đọc tiêu đề trang 3. Đếm số bảng | `By.CSS_SELECTOR "div.example h3"`, `find_elements(By.TAG_NAME, "table")` | Tiêu đề là "Data Tables"; có đúng 2 bảng, id lần lượt `table1`, `table2` | `test_tc01_mo_trang_co_hai_bang` |
| TC02 | Cấu trúc bảng 1 | 1. Đọc các ô `th` 2. Đọc các dòng `tr` và ô `td` | `By.XPATH //table[@id='table1']/thead/tr/th`, `By.TAG_NAME "tr"`, `"td"` | 6 cột: Last Name, First Name, Email, Due, Web Site, Action; 4 dòng, mỗi dòng 6 ô | `test_tc02_cau_truc_bang_1` |
| TC03 | Đọc 1 dòng theo Last Name | 1. Tìm dòng có Last Name = Doe 2. Đọc các ô của dòng | `By.XPATH //table[@id='table1']/tbody/tr[td[1]='Doe']` | First Name = Jason, Email = jdoe@hotmail.com, Due = $100.00, Web Site = http://www.jdoe.com | `test_tc03_doc_mot_dong_theo_last_name` |
| TC04 | Bảng 1 – bấm 1 lần sắp xếp tăng dần (5 cột) | 1. Đọc giá trị cột (truoc) 2. Bấm tiêu đề cột 3. Đọc lại (sau) | `By.XPATH .../th[span[normalize-space()='<tên cột>']]`, `td[n]`; `sorted(truoc, key=...)` | Dữ liệu ban đầu chưa có thứ tự; sau khi bấm: `sau == sorted(truoc)` | `test_tc04_bang_1_bam_1_lan_sap_xep_tang_dan[<cột>]` |
| TC05 | Bảng 1 – bấm 2 lần sắp xếp giảm dần (5 cột) | 1. Đọc cột 2. Bấm tiêu đề 2 lần 3. Đọc lại | Như TC04; `sorted(..., reverse=True)` | `sau == sorted(truoc, reverse=True)` | `test_tc05_bang_1_bam_2_lan_sap_xep_giam_dan[<cột>]` |
| TC06 | Cột Due sắp theo số, không theo chữ | 1. Bấm tiêu đề Due 2. Đọc cột Due, đổi sang `float` | `By.XPATH td[4]`; `float(x.replace("$", ""))` | Thứ tự 50, 50, 51, 100; ô cuối là $100.00; khác với cách sắp kiểu chuỗi | `test_tc06_cot_due_sap_xep_theo_so_khong_theo_chu` |
| TC07 | Bảng 2 – sắp xếp bằng CSS selector (5 cột) | 1. Đọc cột 2. Bấm tiêu đề → kiểm tra tăng 3. Bấm lại → kiểm tra giảm | `By.CSS_SELECTOR "#table2 thead span.<class>"`, `"#table2 tbody td.<class>"` | Lần 1 tăng dần, lần 2 giảm dần | `test_tc07_bang_2_sap_xep_bang_css_selector[<cột>]` |
| TC08 | Sắp xếp không làm lệch dữ liệu dòng | 1. Đọc toàn bộ bảng 2. Lần lượt bấm 5 cột 3. Mỗi lần đọc lại bảng | `By.TAG_NAME "tr"` / `"td"` | Tập hợp các dòng không đổi, chỉ đổi thứ tự (Doe vẫn đi với jdoe@hotmail.com, $100.00) | `test_tc08_sap_xep_khong_lam_lech_du_lieu_dong` |
| TC09 | Bảng 1 không ảnh hưởng bảng 2 | 1. Đọc bảng 2 2. Bấm Last Name, Due ở bảng 1 3. Đọc lại bảng 2 | `By.TAG_NAME` | Bảng 2 giữ nguyên thứ tự | `test_tc09_sap_xep_bang_1_khong_anh_huong_bang_2` |
| TC10 | Tiêu đề đổi trạng thái khi bấm | 1. Đọc `class` của `th` Email 2. Bấm 1 lần, đọc lại 3. Bấm lần 2, đọc lại | `get_attribute("class")` | Ban đầu không có `headerSort`; sau mỗi lần bấm có `headerSort`; 2 lần bấm cho 2 class khác nhau | `test_tc10_tieu_de_doi_trang_thai_sau_moi_lan_bam` |
| TC11 | Cột Action có edit/delete | 1. Mỗi dòng đếm các thẻ `a` 2. Bấm "edit" ở dòng Conway | `find_elements(By.TAG_NAME, "a")`, `By.XPATH ...tr[td[1]='Conway']//a[text()='edit']` | Mỗi dòng có đúng "edit", "delete"; sau khi bấm URL kết thúc bằng `#edit` | `test_tc11_cot_action_co_edit_delete` |

TC04, TC05, TC07 được tham số hoá bằng `@pytest.mark.parametrize` cho 5 cột → tổng cộng **23 test** khi chạy pytest.

## Kết quả mong đợi khi sắp xếp tăng dần (bảng 1)

| Cột | Thứ tự sau khi bấm 1 lần |
|---|---|
| Last Name | Bach, Conway, Doe, Smith |
| First Name | Frank, Jason, John, Tim |
| Email | fbach@yahoo.com, jdoe@hotmail.com, jsmith@gmail.com, tconway@earthlink.net |
| Due | $50.00, $50.00, $51.00, $100.00 |
| Web Site | http://www.frank.com, http://www.jdoe.com, http://www.jsmith.com, http://www.timconway.com |

Kết quả chạy thực tế (Passed/Failed, thời gian) xem trong `report.html`; ảnh chụp bảng sau khi sắp xếp nằm trong thư mục `anh/`.
