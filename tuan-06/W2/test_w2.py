"""Tuan 6 - W2: Kiem thu Dropdown va Checkbox bang Selenium + pytest.

Website: https://the-internet.herokuapp.com/
Chay: python -m pytest test_w2.py -v -s --html=report.html --self-contained-html
"""

from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


BASE_URL = "https://the-internet.herokuapp.com"
SCREENSHOT_DIR = Path(__file__).resolve().parent / "anh"


@pytest.fixture
def driver(request):
    """Moi test co 1 Chrome rieng; tu chup anh sau khi test chay xong.
    Anh duoc luu vao thu muc anh/ (ke ca khi test FAIL).
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1280,900")
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(30)

    try:
        yield browser
    finally:
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        file_path = SCREENSHOT_DIR / f"{request.node.name}.png"
        try:
            if browser.window_handles:
                browser.save_screenshot(str(file_path))
                print(f"\n[ANH MINH CHUNG] {file_path}")
        except Exception as exc:
            print(f"\n[CANH BAO] Khong chup duoc anh: {exc}")
        browser.quit()


# ---------------- PHAN A: DROPDOWN ----------------


def test_tc01_dropdown_chon_bang_text(driver):
    """TC01: Chon Option 1 theo chu hien thi (3.2, 4.1)."""
    driver.get(f"{BASE_URL}/dropdown")
    dropdown_element = driver.find_element(By.ID, "dropdown")
    assert dropdown_element.is_displayed()
    assert dropdown_element.is_enabled()

    dropdown = Select(dropdown_element)
    dropdown.select_by_visible_text("Option 1")
    assert dropdown.first_selected_option.text == "Option 1"


def test_tc02_dropdown_chon_bang_value(driver):
    """TC02: Chon Option 2 theo value (3.2)."""
    driver.get(f"{BASE_URL}/dropdown")
    dropdown = Select(driver.find_element(By.ID, "dropdown"))

    dropdown.select_by_value("2")
    assert dropdown.first_selected_option.get_attribute("value") == "2"
    assert dropdown.first_selected_option.text == "Option 2"


def test_tc03_dropdown_chon_bang_index(driver):
    """TC03: Chon Option 1 theo vi tri index=1 (3.2)."""
    driver.get(f"{BASE_URL}/dropdown")
    dropdown = Select(driver.find_element(By.CSS_SELECTOR, "select#dropdown"))

    dropdown.select_by_index(1)
    assert dropdown.first_selected_option.text == "Option 1"


def test_tc04_dropdown_kiem_tra_danh_sach(driver):
    """TC04: Lay cac option va kiem tra gia tri (3.2, 7.20)."""
    driver.get(f"{BASE_URL}/dropdown")
    dropdown = Select(driver.find_element(By.ID, "dropdown"))
    option_texts = [option.text for option in dropdown.options]
    option_values = [option.get_attribute("value") for option in dropdown.options]

    assert len(dropdown.options) == 3
    assert option_texts[1:] == ["Option 1", "Option 2"]
    assert option_values[1:] == ["1", "2"]


# ---------------- PHAN B: CHECKBOX ----------------


def test_tc05_checkbox_1_tich_chon(driver):
    """TC05: Checkbox 1 chua chon -> tich chon (4.7, 7.20)."""
    driver.get(f"{BASE_URL}/checkboxes")
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "#checkboxes input[type='checkbox']")

    assert len(checkboxes) == 2
    checkbox_1 = checkboxes[0]
    assert checkbox_1.is_displayed()
    assert checkbox_1.is_enabled()
    assert checkbox_1.get_attribute("type") == "checkbox"
    assert not checkbox_1.is_selected()  # Trang mau: checkbox 1 mac dinh bo chon

    checkbox_1.click()
    assert checkbox_1.is_selected()


def test_tc06_checkbox_2_bo_chon(driver):
    """TC06: Checkbox 2 dang chon -> bo chon (7.20)."""
    driver.get(f"{BASE_URL}/checkboxes")
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "#checkboxes input[type='checkbox']")

    assert len(checkboxes) == 2
    checkbox_2 = checkboxes[1]
    assert checkbox_2.is_enabled()
    assert checkbox_2.is_selected()  # Trang mau: checkbox 2 mac dinh duoc chon

    checkbox_2.click()
    assert not checkbox_2.is_selected()


def test_tc07_checkbox_tich_ca_hai(driver):
    """TC07: Tich ca 2 checkbox, khong lam bo chon o da tich."""
    driver.get(f"{BASE_URL}/checkboxes")
    form = driver.find_element(By.ID, "checkboxes")
    checkboxes = form.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")

    assert len(checkboxes) == 2
    for checkbox in checkboxes:
        if not checkbox.is_selected():
            checkbox.click()

    assert all(checkbox.is_selected() for checkbox in checkboxes)
