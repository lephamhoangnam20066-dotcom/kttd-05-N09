"""Tuần 8 – W1 – Chức năng: Thanh trượt – trang /horizontal_slider.

Cấu trúc trang (đã kiểm tra trên trang thật):
    div.sliderContainer > input[type=range] min=0.0 max=5.0 step=0.5, rộng ~129px
                        > span#range  (hiển thị giá trị hiện tại)

Hai cách điều khiển:
    - Bàn phím: click để focus, Keys.HOME về 0, Keys.ARROW_RIGHT tăng 0.5/lần.
    - Chuột: click_and_hold -> move_by_offset -> release
             hoặc drag_and_drop_by_offset (gộp 3 bước).

Tài liệu: 3.3 Drag and drop, 7.2 Action Chains, 7.4 Special Keys, 7.20 WebElement.
"""
import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

SLIDER = (By.CSS_SELECTOR, "input[type='range']")
VALUE_LABEL = (By.ID, "range")
MIN_VALUE, MAX_VALUE = 0.0, 5.0


def open_slider(driver, base_url):
    driver.get(base_url + "/horizontal_slider")
    return driver.find_element(*SLIDER)


def current_value(driver, slider):
    """Đọc giá trị thanh trượt và kiểm tra số hiển thị bên phải khớp với nó."""
    value = float(slider.get_attribute("value"))
    label = float(driver.find_element(*VALUE_LABEL).text)
    assert label == value, f"Số hiển thị ({label}) khác giá trị thanh trượt ({value})"
    return value


def press_keys(driver, slider, *keys):
    """Click để focus thanh trượt, về đầu bằng HOME rồi gửi các phím."""
    ActionChains(driver).click(slider).send_keys(Keys.HOME, *keys).perform()


def past_edge_offset(slider):
    """Offset từ tâm ra quá mép thanh một chút (tránh MoveTargetOutOfBounds)."""
    return slider.size["width"] // 2 + 5


def test_TC_SLD_01_gia_tri_ban_dau(driver, base_url):
    """Mở trang: thanh trượt hiển thị và giá trị ban đầu là 0."""
    slider = open_slider(driver, base_url)

    assert slider.is_displayed()
    assert current_value(driver, slider) == MIN_VALUE


@pytest.mark.parametrize(
    "presses, expected",
    [(1, 0.5), (5, 2.5), (9, 4.5), (10, 5.0)],
    ids=["0.5_sat_bien_duoi", "2.5_giua", "4.5_sat_bien_tren", "5.0_bien_tren"],
)
def test_TC_SLD_02_ban_phim_moi_lan_tang_0_5(driver, base_url, presses, expected):
    """HOME rồi ARROW_RIGHT n lần: giá trị = 0.5 x n (giá trị biên 0.5, 4.5, 5.0)."""
    slider = open_slider(driver, base_url)

    press_keys(driver, slider, *([Keys.ARROW_RIGHT] * presses))

    assert current_value(driver, slider) == expected


def test_TC_SLD_03_khong_vuot_qua_gia_tri_lon_nhat(driver, base_url):
    """Bấm ARROW_RIGHT 12 lần (nhiều hơn cần): giá trị dừng ở 5."""
    slider = open_slider(driver, base_url)

    press_keys(driver, slider, *([Keys.ARROW_RIGHT] * 12))

    assert current_value(driver, slider) == MAX_VALUE


def test_TC_SLD_04_khong_nho_hon_gia_tri_nho_nhat(driver, base_url):
    """Về 0 bằng HOME rồi bấm ARROW_LEFT: giá trị vẫn là 0."""
    slider = open_slider(driver, base_url)

    press_keys(driver, slider, Keys.ARROW_LEFT)

    assert current_value(driver, slider) == MIN_VALUE


def test_TC_SLD_05_nhan_giu_o_giua_thanh(driver, base_url):
    """click_and_hold tại tâm thanh rồi release: giá trị là 2.5."""
    slider = open_slider(driver, base_url)

    ActionChains(driver).click_and_hold(slider).release().perform()

    assert current_value(driver, slider) == 2.5


def test_TC_SLD_06_keo_chuot_qua_mep_phai(driver, base_url):
    """click_and_hold -> move_by_offset ra quá mép phải -> release: giá trị là 5."""
    slider = open_slider(driver, base_url)

    (ActionChains(driver)
        .click_and_hold(slider)
        .move_by_offset(past_edge_offset(slider), 0)
        .release()
        .perform())

    assert current_value(driver, slider) == MAX_VALUE


def test_TC_SLD_07_drag_and_drop_by_offset_ve_mep_trai(driver, base_url):
    """Đưa lên 5 bằng bàn phím, rồi drag_and_drop_by_offset sang trái: giá trị về 0."""
    slider = open_slider(driver, base_url)
    press_keys(driver, slider, *([Keys.ARROW_RIGHT] * 10))
    assert current_value(driver, slider) == MAX_VALUE

    ActionChains(driver).drag_and_drop_by_offset(slider, -past_edge_offset(slider), 0).perform()

    assert current_value(driver, slider) == MIN_VALUE


def test_TC_SLD_08_keo_mot_phan_tu_thanh(driver, base_url):
    """Kéo từ tâm sang phải 1/4 chiều rộng: giá trị nằm trong khoảng (2.5; 5) và đúng bước 0.5."""
    slider = open_slider(driver, base_url)

    ActionChains(driver).drag_and_drop_by_offset(slider, slider.size["width"] // 4, 0).perform()

    value = current_value(driver, slider)
    assert 2.5 < value < MAX_VALUE
    assert (value / 0.5).is_integer()
