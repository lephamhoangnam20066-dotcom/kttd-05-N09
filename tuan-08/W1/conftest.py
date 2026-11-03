"""Cấu hình chung cho bộ test Tuần 8 – W1.

- Fixture `driver`: mở Chrome trước mỗi test, đóng sau test (giống setUp/tearDown).
- Tuỳ chọn `--headless`: chạy Chrome không giao diện.
- Biến môi trường BASE_URL: đổi địa chỉ trang test (mặc định là the-internet).
- Báo cáo HTML (pytest-html): thêm cột "Mô tả" và ảnh màn hình cuối mỗi test.
"""
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = os.environ.get("BASE_URL", "https://the-internet.herokuapp.com").rstrip("/")


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Chạy Chrome ở chế độ không giao diện",
    )


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def driver(request):
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,768")

    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()


# ---------------------------------------------------------------------------
# Báo cáo HTML (pytest-html)
# ---------------------------------------------------------------------------

@pytest.hookimpl(optionalhook=True)
def pytest_html_report_title(report):
    report.title = "Báo cáo kiểm thử Tuần 8 – W1: Di chuột & thanh trượt"


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Mô tả</th>")


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<td>{getattr(report, 'description', '')}</td>")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    doc = item.function.__doc__ or ""
    report.description = " ".join(doc.split())

    # Chụp màn hình cuối bước test và gắn vào báo cáo HTML
    if report.when == "call":
        drv = item.funcargs.get("driver")
        try:
            from pytest_html import extras as html_extras
        except ImportError:
            html_extras = None
        if drv is not None and html_extras is not None:
            label = "Ảnh lúc lỗi" if report.failed else "Ảnh cuối bước test"
            extras = getattr(report, "extras", [])
            extras.append(html_extras.image(drv.get_screenshot_as_base64(), label))
            report.extras = extras
