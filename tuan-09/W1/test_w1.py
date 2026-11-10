"""
Bài thực hành Kiểm thử phần mềm – Tuần 9, W1 – Nhóm N09
Chức năng 4: Dữ liệu & trạng thái đặc biệt
Đề bài   : Bảng dữ liệu sắp xếp được (Sortable Data Tables)
Trang    : https://the-internet.herokuapp.com/tables

Kiến thức áp dụng (tài liệu selenium-python):
    4.3 By XPath, 4.5 By Tag Name, 4.7 By CSS Selector, 7.20 WebElement
    -> find_elements, By.XPATH, By.CSS_SELECTOR, By.TAG_NAME, .text, .click(), sorted()

Ý tưởng chung để kiểm thử một bảng sắp xếp được:
    1. Đọc giá trị của cột TRƯỚC khi bấm   -> list "truoc"
    2. Bấm vào tiêu đề cột (click) rồi CHỜ bảng sắp xếp xong (xem hàm bam_tieu_de)
    3. Đọc lại giá trị của cột SAU khi bấm -> list "sau"
    4. So sánh: sau == sorted(truoc)  (tăng dần)  /  sorted(truoc, reverse=True) (giảm dần)
"""
import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://the-internet.herokuapp.com/tables"
THU_MUC_ANH = Path(__file__).parent / "anh"

# 5 cột có dữ liệu để sắp xếp (cột "Action" chỉ chứa link edit/delete)
COT_DU_LIEU = ["Last Name", "First Name", "Email", "Due", "Web Site"]
TIEU_DE_DAY_DU = COT_DU_LIEU + ["Action"]

# Bảng 2 (Example 2) có class trên từng ô -> chọn bằng CSS selector rất gọn
CLASS_COT_BANG_2 = {
    "Last Name": "last-name",
    "First Name": "first-name",
    "Email": "email",
    "Due": "dues",
    "Web Site": "web-site",
}


# ----------------------------------------------------------------------------
# Fixture
# ----------------------------------------------------------------------------
@pytest.fixture(scope="module")
def driver():
    """Mở 1 trình duyệt Chrome dùng chung cho cả file test."""
    tuy_chon = Options()
    if os.getenv("HEADLESS") == "1":          # set HEADLESS=1 để chạy ẩn trình duyệt
        tuy_chon.add_argument("--headless=new")
    tuy_chon.add_argument("--window-size=1366,900")
    trinh_duyet = webdriver.Chrome(options=tuy_chon)
    trinh_duyet.implicitly_wait(5)
    yield trinh_duyet
    trinh_duyet.quit()


@pytest.fixture
def trang(driver):
    """Tải lại trang trước MỖI test để bảng trở về thứ tự ban đầu (chưa sắp xếp)."""
    driver.get(URL)
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "table1")))
    return driver


# ----------------------------------------------------------------------------
# Hàm hỗ trợ
# ----------------------------------------------------------------------------
def khoa_sap_xep(ten_cot):
    """Trả về hàm key cho sorted().
    - Cột Due là tiền: phải so sánh theo SỐ ("$51.00" < "$100.00").
    - Các cột còn lại: so sánh chữ, không phân biệt hoa/thường.
    """
    if ten_cot == "Due":
        return lambda gia_tri: float(gia_tri.replace("$", "").replace(",", ""))
    return lambda gia_tri: gia_tri.lower()


def chup_anh(driver, ten_file, id_bang=None):
    """Lưu ảnh vào thư mục anh/. Có id_bang thì chỉ chụp riêng bảng đó
    (WebElement.screenshot – mục 7.20)."""
    THU_MUC_ANH.mkdir(exist_ok=True)
    duong_dan = str(THU_MUC_ANH / f"{ten_file}.png")
    if id_bang:
        driver.find_element(By.ID, id_bang).screenshot(duong_dan)
    else:
        driver.save_screenshot(duong_dan)


def ten_anh(ten_cot):
    return ten_cot.replace(" ", "_")


def lay_tieu_de(driver, id_bang):
    """By.XPATH + find_elements: lấy tên tất cả các cột của bảng."""
    cac_th = driver.find_elements(By.XPATH, f"//table[@id='{id_bang}']/thead/tr/th")
    return [th.text.strip() for th in cac_th]


def o_tieu_de(driver, id_bang, ten_cot):
    """By.XPATH: tìm ô <th> có <span> mang đúng tên cột (bảng 1 không có class/id)."""
    return driver.find_element(
        By.XPATH, f"//table[@id='{id_bang}']/thead//th[span[normalize-space()='{ten_cot}']]"
    )


def o_tieu_de_bang_2(driver, ten_class):
    """By.CSS_SELECTOR tìm <span class="..."> trong tiêu đề bảng 2,
    rồi dùng XPath '..' để đi lên ô <th> cha (ô <th> mới là nơi đổi class khi sắp xếp)."""
    span = driver.find_element(By.CSS_SELECTOR, f"#table2 thead span.{ten_class}")
    return span.find_element(By.XPATH, "..")


def bam_tieu_de(driver, th):
    """Bấm vào ô tiêu đề <th> rồi CHỜ bảng sắp xếp xong.

    Trang dùng jQuery tablesorter: lúc click nó KHÔNG sắp xếp ngay mà đẩy việc sắp xếp
    vào setTimeout(..., 1). Nếu đọc bảng liền sau .click() có thể đọc phải thứ tự CŨ
    -> test lúc đỏ lúc xanh. Việc đổi class của <th> và sắp xếp lại các dòng nằm trong
    CÙNG một lần chạy, nên chờ class của <th> đổi là chắc chắn bảng đã sắp xong.
    """
    class_cu = th.get_attribute("class")
    th.click()
    WebDriverWait(driver, 5).until(
        lambda _: th.get_attribute("class") != class_cu,
        message="Đã bấm tiêu đề nhưng bảng không sắp xếp lại",
    )


def lay_cot_xpath(driver, id_bang, ten_cot):
    """By.XPATH: lấy mọi ô của 1 cột theo vị trí td[n] (XPath đếm từ 1)."""
    vi_tri = TIEU_DE_DAY_DU.index(ten_cot) + 1
    cac_o = driver.find_elements(By.XPATH, f"//table[@id='{id_bang}']/tbody/tr/td[{vi_tri}]")
    return [o.text.strip() for o in cac_o]


def lay_cot_css(driver, ten_class):
    """By.CSS_SELECTOR: bảng 2 có class trên từng ô nên chỉ cần '#table2 tbody td.<class>'."""
    cac_o = driver.find_elements(By.CSS_SELECTOR, f"#table2 tbody td.{ten_class}")
    return [o.text.strip() for o in cac_o]


def lay_bang(driver, id_bang):
    """By.TAG_NAME: duyệt từng <tr>, trong mỗi dòng lấy các <td> -> list các dòng."""
    than_bang = driver.find_element(By.CSS_SELECTOR, f"#{id_bang} tbody")
    cac_dong = than_bang.find_elements(By.TAG_NAME, "tr")
    return [[o.text.strip() for o in dong.find_elements(By.TAG_NAME, "td")] for dong in cac_dong]


# ----------------------------------------------------------------------------
# Test case
# ----------------------------------------------------------------------------
def test_tc01_mo_trang_co_hai_bang(trang):
    """TC01 – Mở trang /tables: tiêu đề 'Data Tables' và có đúng 2 bảng table1, table2."""
    assert trang.find_element(By.CSS_SELECTOR, "div.example h3").text == "Data Tables"
    cac_bang = trang.find_elements(By.TAG_NAME, "table")
    assert len(cac_bang) == 2
    assert [b.get_attribute("id") for b in cac_bang] == ["table1", "table2"]
    chup_anh(trang, "TC01_trang_tables")


def test_tc02_cau_truc_bang_1(trang):
    """TC02 – Bảng 1 có 6 cột đúng tên, 4 dòng dữ liệu, mỗi dòng đủ 6 ô."""
    assert lay_tieu_de(trang, "table1") == TIEU_DE_DAY_DU
    bang = lay_bang(trang, "table1")
    assert len(bang) == 4
    assert all(len(dong) == 6 for dong in bang)
    chup_anh(trang, "TC02_cau_truc_bang_1", "table1")


def test_tc03_doc_mot_dong_theo_last_name(trang):
    """TC03 – Dùng XPath tìm dòng có Last Name = 'Doe' rồi kiểm tra dữ liệu dòng đó."""
    dong = trang.find_element(By.XPATH, "//table[@id='table1']/tbody/tr[td[1]='Doe']")
    cac_o = dong.find_elements(By.TAG_NAME, "td")
    assert cac_o[1].text == "Jason"
    assert cac_o[2].text == "jdoe@hotmail.com"
    assert cac_o[3].text == "$100.00"
    assert cac_o[4].text == "http://www.jdoe.com"


@pytest.mark.parametrize("ten_cot", COT_DU_LIEU)
def test_tc04_bang_1_bam_1_lan_sap_xep_tang_dan(trang, ten_cot):
    """TC04 – Bảng 1: bấm tiêu đề cột 1 lần -> cột được sắp xếp TĂNG dần."""
    key = khoa_sap_xep(ten_cot)
    truoc = lay_cot_xpath(trang, "table1", ten_cot)
    # Tiền điều kiện: dữ liệu ban đầu chưa có thứ tự, nếu không test sẽ không chứng minh được gì
    assert truoc != sorted(truoc, key=key)

    th = o_tieu_de(trang, "table1", ten_cot)
    bam_tieu_de(trang, th)

    sau = lay_cot_xpath(trang, "table1", ten_cot)
    assert sau == sorted(truoc, key=key)
    chup_anh(trang, f"TC04_tang_dan_{ten_anh(ten_cot)}", "table1")


@pytest.mark.parametrize("ten_cot", COT_DU_LIEU)
def test_tc05_bang_1_bam_2_lan_sap_xep_giam_dan(trang, ten_cot):
    """TC05 – Bảng 1: bấm tiêu đề cột 2 lần -> cột được sắp xếp GIẢM dần."""
    key = khoa_sap_xep(ten_cot)
    truoc = lay_cot_xpath(trang, "table1", ten_cot)

    bam_tieu_de(trang, o_tieu_de(trang, "table1", ten_cot))
    bam_tieu_de(trang, o_tieu_de(trang, "table1", ten_cot))

    sau = lay_cot_xpath(trang, "table1", ten_cot)
    assert sau == sorted(truoc, key=key, reverse=True)
    chup_anh(trang, f"TC05_giam_dan_{ten_anh(ten_cot)}", "table1")


def test_tc06_cot_due_sap_xep_theo_so_khong_theo_chu(trang):
    """TC06 – Cột Due phải sắp theo GIÁ TRỊ SỐ: $51.00 đứng trước $100.00.
    Nếu so sánh kiểu chuỗi thì '$100.00' < '$50.00' (sai) -> phải đổi sang float."""
    bam_tieu_de(trang, o_tieu_de(trang, "table1", "Due"))
    sau = lay_cot_xpath(trang, "table1", "Due")

    cac_so = [float(x.replace("$", "")) for x in sau]
    assert cac_so == sorted(cac_so)
    assert sau[-1] == "$100.00"
    # Chứng minh cái bẫy: sắp xếp kiểu chuỗi sẽ cho thứ tự khác với trang web
    assert sau != sorted(sau)
    chup_anh(trang, "TC06_due_theo_so", "table1")


@pytest.mark.parametrize("ten_cot", COT_DU_LIEU)
def test_tc07_bang_2_sap_xep_bang_css_selector(trang, ten_cot):
    """TC07 – Bảng 2: chọn tiêu đề và ô bằng CSS selector theo class.
    Bấm lần 1 -> tăng dần, bấm lần 2 -> giảm dần."""
    ten_class = CLASS_COT_BANG_2[ten_cot]
    key = khoa_sap_xep(ten_cot)
    tieu_de = o_tieu_de_bang_2(trang, ten_class)
    truoc = lay_cot_css(trang, ten_class)

    bam_tieu_de(trang, tieu_de)
    assert lay_cot_css(trang, ten_class) == sorted(truoc, key=key)

    bam_tieu_de(trang, tieu_de)
    assert lay_cot_css(trang, ten_class) == sorted(truoc, key=key, reverse=True)
    chup_anh(trang, f"TC07_bang_2_{ten_anh(ten_cot)}", "table2")


def test_tc08_sap_xep_khong_lam_lech_du_lieu_dong(trang):
    """TC08 – Sắp xếp chỉ đổi THỨ TỰ dòng; dữ liệu trong từng dòng phải giữ nguyên.
    (vd: sau khi sắp theo Due, 'Doe' vẫn đi cùng 'jdoe@hotmail.com' và '$100.00')"""
    truoc = lay_bang(trang, "table1")
    for ten_cot in COT_DU_LIEU:
        bam_tieu_de(trang, o_tieu_de(trang, "table1", ten_cot))
        sau = lay_bang(trang, "table1")
        assert sorted(sau) == sorted(truoc), f"Dữ liệu dòng bị lệch sau khi sắp theo {ten_cot}"


def test_tc09_sap_xep_bang_1_khong_anh_huong_bang_2(trang):
    """TC09 – Sắp xếp bảng 1 không được làm thay đổi thứ tự của bảng 2."""
    bang_2_truoc = lay_bang(trang, "table2")
    bam_tieu_de(trang, o_tieu_de(trang, "table1", "Last Name"))
    bam_tieu_de(trang, o_tieu_de(trang, "table1", "Due"))
    assert lay_bang(trang, "table2") == bang_2_truoc


def test_tc10_tieu_de_doi_trang_thai_sau_moi_lan_bam(trang):
    """TC10 – Ô tiêu đề đổi class (trạng thái tăng/giảm) sau mỗi lần bấm."""
    th = o_tieu_de(trang, "table1", "Email")
    class_ban_dau = th.get_attribute("class")
    bam_tieu_de(trang, th)
    class_lan_1 = th.get_attribute("class")
    bam_tieu_de(trang, th)
    class_lan_2 = th.get_attribute("class")

    assert "headerSort" not in class_ban_dau            # chưa sắp xếp
    assert "headerSort" in class_lan_1                   # đã sắp xếp (1 chiều)
    assert "headerSort" in class_lan_2                   # đã sắp xếp (chiều ngược lại)
    assert class_lan_1 != class_lan_2                    # 2 trạng thái phải khác nhau


def test_tc11_cot_action_co_edit_delete(trang):
    """TC11 – Mỗi dòng có 2 link 'edit', 'delete'; bấm 'edit' của dòng Conway -> URL có #edit."""
    for dong in trang.find_elements(By.CSS_SELECTOR, "#table1 tbody tr"):
        cac_link = dong.find_elements(By.TAG_NAME, "a")
        assert [a.text for a in cac_link] == ["edit", "delete"]

    trang.find_element(
        By.XPATH, "//table[@id='table1']/tbody/tr[td[1]='Conway']//a[text()='edit']"
    ).click()
    assert trang.current_url.endswith("#edit")
