"""Tuan 7 - W1: Tai noi dung dong (Dynamic Loading) bang Selenium + pytest.

Kien thuc theo tai lieu giang vien:
    5.1 Explicit Waits  - WebDriverWait, until, expected_conditions (EC)
    5.2 Implicit Waits  - implicitly_wait
    7.1 Exceptions      - TimeoutException, NoSuchElementException (bat bang pytest.raises)

Website:
    https://the-internet.herokuapp.com/dynamic_loading/1  (phan tu CO SAN nhung bi AN)
    https://the-internet.herokuapp.com/dynamic_loading/2  (phan tu CHUA CO, duoc THEM VAO sau)

Chay: python -m pytest test_w1.py -v -s --html=report.html --self-contained-html
"""

import time
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


BASE_URL = "https://the-internet.herokuapp.com"
SCREENSHOT_DIR = Path(__file__).resolve().parent / "anh"

# Trang mau: bam Start -> hien "Loading..." khoang 5 giay -> hien "Hello World!"
THOI_GIAN_CHO = 10  # giay: du lon hon 5 giay tai cua trang
THOI_GIAN_CHO_NGAN = 2  # giay: co tinh ngan hon 5 giay de tao ra loi

# Locator dung chung (lay tu HTML that cua trang)
START_BUTTON = (By.CSS_SELECTOR, "#start button")
LOADING = (By.ID, "loading")  # chi duoc chen vao DOM sau khi bam Start
FINISH = (By.ID, "finish")
FINISH_TEXT = (By.CSS_SELECTOR, "#finish h4")


@pytest.fixture
def driver(request):
    """Moi test co 1 Chrome rieng; tu chup anh sau khi test chay xong.
    Mac dinh implicit wait = 0 (theo 5.2); test nao can se tu dat.
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


# ---------------- PHAN A: EXPLICIT WAIT (5.1) ----------------


def test_tc01_vd1_cho_phan_tu_an_hien_ra(driver):
    """TC01: Vi du 1 - #finish co san nhung bi an; cho den khi HIEN THI (5.1)."""
    driver.get(f"{BASE_URL}/dynamic_loading/1")

    finish = driver.find_element(*FINISH)  # Tim thay ngay vi da co trong DOM
    assert not finish.is_displayed()  # ...nhung dang bi an (display:none)

    driver.find_element(*START_BUTTON).click()
    bat_dau = time.monotonic()

    wait = WebDriverWait(driver, THOI_GIAN_CHO)
    hello = wait.until(EC.visibility_of_element_located(FINISH_TEXT))
    thoi_gian = time.monotonic() - bat_dau
    print(f"\n[THOI GIAN CHO THUC TE] {thoi_gian:.1f} giay")

    assert hello.is_displayed()
    assert hello.text == "Hello World!"
    # Explicit wait chi cho "vua du", khong phai luc nao cung het 10 giay
    assert thoi_gian < THOI_GIAN_CHO


def test_tc02_vd2_cho_phan_tu_duoc_them_vao_dom(driver):
    """TC02: Vi du 2 - #finish chua co; cho co trong DOM roi cho hien thi (5.1)."""
    driver.get(f"{BASE_URL}/dynamic_loading/2")

    # find_elements tra ve danh sach rong khi chua co phan tu (khong bao loi)
    assert driver.find_elements(*FINISH) == []

    driver.find_element(*START_BUTTON).click()

    wait = WebDriverWait(driver, THOI_GIAN_CHO)
    finish = wait.until(EC.presence_of_element_located(FINISH))  # da co trong DOM
    hello = wait.until(EC.visibility_of_element_located(FINISH_TEXT))  # da hien thi

    assert finish.get_attribute("id") == "finish"
    assert hello.text == "Hello World!"


def test_tc03_cho_loading_bien_mat(driver):
    """TC03: Cho thanh "Loading..." xuat hien roi BIEN MAT (5.1)."""
    driver.get(f"{BASE_URL}/dynamic_loading/1")
    driver.find_element(*START_BUTTON).click()

    wait = WebDriverWait(driver, THOI_GIAN_CHO)
    loading = wait.until(EC.visibility_of_element_located(LOADING))
    assert "Loading" in loading.text

    # invisibility_of_element_located: dung khi phan tu bi an HOAC khong con trong DOM
    assert wait.until(EC.invisibility_of_element_located(LOADING))

    assert driver.find_element(*FINISH).is_displayed()
    assert not driver.find_element(*START_BUTTON).is_displayed()  # Nut Start da bi an


def test_tc04_timeout_khi_khong_bam_start(driver):
    """TC04: Khong bam Start -> #finish khong bao gio xuat hien -> TimeoutException (7.1)."""
    driver.get(f"{BASE_URL}/dynamic_loading/2")

    wait = WebDriverWait(driver, THOI_GIAN_CHO_NGAN)
    with pytest.raises(TimeoutException) as loi:
        wait.until(
            EC.presence_of_element_located(FINISH),
            message="Khong thay #finish vi chua bam Start",
        )

    assert "Khong thay #finish" in str(loi.value)


def test_tc05_timeout_khi_cho_qua_ngan(driver):
    """TC05: Cho 2 giay < 5 giay tai -> TimeoutException; cho 10 giay -> thanh cong (5.1, 7.1)."""
    driver.get(f"{BASE_URL}/dynamic_loading/1")
    driver.find_element(*START_BUTTON).click()

    with pytest.raises(TimeoutException):
        WebDriverWait(driver, THOI_GIAN_CHO_NGAN).until(
            EC.visibility_of_element_located(FINISH_TEXT)
        )

    # Trang KHONG loi - chi la cho qua ngan. Cho du lau thi van thay ket qua.
    hello = WebDriverWait(driver, THOI_GIAN_CHO).until(
        EC.visibility_of_element_located(FINISH_TEXT)
    )
    assert hello.text == "Hello World!"


# ---------------- PHAN B: IMPLICIT WAIT (5.2) ----------------


def test_tc06_implicit_wait_vd2_tim_thay_phan_tu_moi(driver):
    """TC06: Vi du 2 - implicitly_wait giup find_element cho phan tu duoc them vao (5.2)."""
    driver.implicitly_wait(THOI_GIAN_CHO)  # ap dung cho moi lan find_element cua driver nay
    driver.get(f"{BASE_URL}/dynamic_loading/2")
    driver.find_element(*START_BUTTON).click()

    finish = driver.find_element(*FINISH)  # Tu dong cho toi da 10 giay den khi co trong DOM

    assert finish.is_displayed()
    assert finish.text == "Hello World!"


def test_tc07_implicit_wait_khong_cho_phan_tu_an(driver):
    """TC07: Vi du 1 - implicit wait chi cho phan tu CO MAT, khong cho HIEN THI (5.2)."""
    driver.implicitly_wait(THOI_GIAN_CHO)
    driver.get(f"{BASE_URL}/dynamic_loading/1")
    driver.find_element(*START_BUTTON).click()

    bat_dau = time.monotonic()
    finish = driver.find_element(*FINISH)  # Tra ve NGAY vi #finish co san (chi bi an)
    thoi_gian = time.monotonic() - bat_dau

    assert thoi_gian < 3  # Khong he cho 10 giay
    assert not finish.is_displayed()  # Van dang "Loading..."
    assert finish.text == ""  # Selenium chi doc chu dang HIEN THI
    # => Voi phan tu bi an phai dung Explicit Wait + visibility (xem TC01)


def test_tc08_implicit_wait_het_gio_nosuchelement(driver):
    """TC08: Implicit wait het gio -> NoSuchElementException (5.2, 7.1)."""
    driver.implicitly_wait(THOI_GIAN_CHO_NGAN)
    driver.get(f"{BASE_URL}/dynamic_loading/2")  # Khong bam Start

    bat_dau = time.monotonic()
    with pytest.raises(NoSuchElementException):
        driver.find_element(*FINISH)
    thoi_gian = time.monotonic() - bat_dau
    print(f"\n[THOI GIAN CHO TRUOC KHI BAO LOI] {thoi_gian:.1f} giay")

    # Selenium da cho het implicit wait (khoang 2 giay) roi moi bao loi
    assert thoi_gian >= THOI_GIAN_CHO_NGAN - 0.5
