# =======================================================================
#
#  This file is part of WebWidgets, a Python package for designing web
#  UIs.
#
#  You should have received a copy of the MIT License along with
#  WebWidgets. If not, see <https://opensource.org/license/mit>.
#
#  Copyright(C) 2025, mlaasri
#
# =======================================================================

import pytest
from .render_page import DriverInfo, render_page
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from typing import Union
import webwidgets as ww


@pytest.fixture(scope="session")
def chrome_web_driver():
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--silent")
    driver = Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def firefox_web_driver():
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = Firefox(options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def web_drivers_info(chrome_web_driver, firefox_web_driver):
    return [get_driver_info(d) for d in [chrome_web_driver,
                                         firefox_web_driver]]


def get_driver_info(driver: Union[Chrome, Firefox]) -> DriverInfo:
    """A utility function for collecting information about a web driver.

    The function measures the minimum size of the driver's window and then
    renders an empty page to measure the margin offset within it. This
    information can be used to adjust the window's size to achieve a particular
    size when rendering an image in :py:func:`render_page`.

    :param driver: The web driver to collect information about.
    :type driver: Union[Chrome, Firefox]
    :return: A DriverInfo object containing the driver and additional
        information about it.
    :rtype: DriverInfo
    """
    # Measuring the minimum size
    driver.set_window_size(1, 1)  # Trying to set a minimal size
    min_size = driver.get_window_size()
    min_size = (min_size["height"], min_size["width"])

    # Rendering an empty page to measure the margin offset
    size = (2 * min_size[0], 2 * min_size[1])
    tmp_driver_info = DriverInfo(driver=driver, min_size=size, offset=(0, 0))
    array = render_page(ww.Page(), tmp_driver_info, size)
    offset = size[0] - array.shape[0], size[1] - array.shape[1]

    # Returning the collected information
    return DriverInfo(driver=driver, min_size=min_size, offset=offset)
