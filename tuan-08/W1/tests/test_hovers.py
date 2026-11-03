"""Tuần 8 – W1 – Chức năng: Di chuột (hover) – trang /hovers.

Cấu trúc trang (đã kiểm tra trên trang thật):
    div.figure > img
               > div.figcaption (ẩn sẵn) > h5 "name: userN"
                                         > a "View profile" (href=/users/N)
Chú thích chỉ hiện khi con trỏ chuột nằm trên ảnh.

Tài liệu: 7.2 Action Chains (move_to_element, click, perform),
          7.20 WebElement (is_displayed, text, get_attribute, find_element).
"""
import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

FIGURE = (By.CSS_SELECTOR, ".figure")
CAPTION = (By.CSS_SELECTOR, ".figcaption")
NAME = (By.TAG_NAME, "h5")
PROFILE_LINK = (By.CSS_SELECTOR, ".figcaption a")
HEADING = (By.TAG_NAME, "h3")


def open_hovers(driver, base_url):
    driver.get(base_url + "/hovers")
    return driver.find_elements(*FIGURE)


def hover(driver, element):
    """Đưa chuột vào giữa phần tử (không click)."""
    ActionChains(driver).move_to_element(element).perform()


def captions_state(figures):
    """Danh sách True/False: chú thích của từng ảnh có đang hiện không."""
    return [fig.find_element(*CAPTION).is_displayed() for fig in figures]


def test_TC_HOV_01_chu_thich_an_truoc_khi_hover(driver, base_url):
    """Trang có 3 ảnh; chưa hover thì không chú thích nào hiển thị."""
    figures = open_hovers(driver, base_url)

    assert len(figures) == 3
    assert captions_state(figures) == [False, False, False]


@pytest.mark.parametrize("index", [1, 2, 3])
def test_TC_HOV_02_hover_hien_dung_ten(driver, base_url, index):
    """Hover vào ảnh thứ N thì hiện chú thích 'name: userN'."""
    figures = open_hovers(driver, base_url)
    figure = figures[index - 1]
    caption = figure.find_element(*CAPTION)

    hover(driver, figure)
    WebDriverWait(driver, 5).until(lambda d: caption.is_displayed())

    assert caption.is_displayed()
    assert caption.find_element(*NAME).text == f"name: user{index}"


def test_TC_HOV_03_moi_lan_chi_hien_mot_chu_thich(driver, base_url):
    """Hover ảnh 1 rồi sang ảnh 2: chỉ chú thích của ảnh 2 hiển thị."""
    figures = open_hovers(driver, base_url)

    hover(driver, figures[0])
    assert captions_state(figures) == [True, False, False]

    hover(driver, figures[1])
    assert captions_state(figures) == [False, True, False]


def test_TC_HOV_04_roi_chuot_thi_chu_thich_an(driver, base_url):
    """Hover ảnh 1 rồi đưa chuột ra tiêu đề trang: chú thích ẩn lại."""
    figures = open_hovers(driver, base_url)
    caption = figures[0].find_element(*CAPTION)

    hover(driver, figures[0])
    assert caption.is_displayed()

    hover(driver, driver.find_element(*HEADING))
    WebDriverWait(driver, 5).until_not(lambda d: caption.is_displayed())
    assert not caption.is_displayed()


@pytest.mark.parametrize("index", [1, 2, 3])
def test_TC_HOV_05_view_profile_dung_duong_dan(driver, base_url, index):
    """Hover ảnh N rồi bấm 'View profile': chuyển tới đường dẫn /users/N."""
    figures = open_hovers(driver, base_url)
    figure = figures[index - 1]
    link = figure.find_element(*PROFILE_LINK)

    assert link.get_attribute("href").endswith(f"/users/{index}")

    # Mẫu trong tài liệu 7.2: move_to_element(menu).click(hidden_submenu).perform()
    ActionChains(driver).move_to_element(figure).click(link).perform()

    WebDriverWait(driver, 5).until(lambda d: d.current_url.endswith(f"/users/{index}"))
    assert driver.current_url.endswith(f"/users/{index}")
