"""Ba trường hợp kiểm thử đăng nhập trang demo The Internet."""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://the-internet.herokuapp.com/login"


@pytest.fixture
def driver():
    # Selenium Manager tự tìm/cài driver phù hợp nếu môi trường hỗ trợ.
    browser = webdriver.Chrome()
    browser.set_window_size(1280, 900)
    yield browser
    browser.quit()


def login(driver, username, password):
    # Mở trang và chờ biểu mẫu sẵn sàng trước khi nhập.
    driver.get(URL)
    wait = WebDriverWait(driver, 15)
    user = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    user.send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    return wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text


def test_login_thanh_cong(driver):
    # Đăng nhập hợp lệ phải chuyển tới trang bảo mật.
    message = login(driver, "tomsmith", "SuperSecretPassword!")
    assert "You logged into a secure area!" in message
    assert "/secure" in driver.current_url


def test_login_sai_mat_khau(driver):
    # Mật khẩu không hợp lệ phải xuất hiện thông báo lỗi.
    message = login(driver, "tomsmith", "wrong-password")
    assert "Your password is invalid!" in message
    assert "/login" in driver.current_url


def test_login_sai_ten_dang_nhap(driver):
    # Tên đăng nhập không hợp lệ phải xuất hiện thông báo lỗi.
    message = login(driver, "wrong-user", "SuperSecretPassword!")
    assert "Your username is invalid!" in message
    assert "/login" in driver.current_url
