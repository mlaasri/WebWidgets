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

from dataclasses import dataclass
import numpy as np
import os
from PIL import Image
from selenium.webdriver import Chrome, Firefox
import tempfile
from typing import Tuple, Union
import webwidgets as ww


@dataclass
class DriverInfo:
    """A wrapper object containing a web driver and additional information
    about it.
    """
    driver: Union[Chrome, Firefox]
    min_size: Tuple[int, int]
    offset: Tuple[int, int]


def render_page(page: ww.Page, driver_info: DriverInfo,
                size: Tuple[int, int]) -> np.ndarray:
    """Renders a page with the given web driver and returns a numpy array of
    the rendered image.

    :param page: The page to render.
    :type page: Page
    :param driver_info: The DriverInfo object containing the web driver and
        additional information about it to use for rendering.
    :type driver_info: DriverInfo
    :param size: The size of the web driver's window as (width, height). This
        parameter influences the size of the rendered image, but it it does not
        enforce it.
    :type size: Tuple[int, int]
    :return: A numpy array of the rendered image.
    :rtype: np.ndarray
    """
    # Using the web driver's info to check and adjust the requested size
    if np.any(np.less(size, driver_info.min_size)):
        raise ValueError(f"Size must be bigger than {driver_info.min_size} "
                         f"but got: {size}")  # Must be above driver's minimum
    size = (size[0] + driver_info.offset[0], size[1] + driver_info.offset[1])

    # Compiling a website with the given page only
    website = ww.Website(pages=[page])
    compiled = website.compile()

    # Rendering within a temporary directory
    with tempfile.TemporaryDirectory() as tmp:

        # Exporting HTML and CSS code
        html_file_path = os.path.join(tmp, "index.html")
        css_file_path = os.path.join(tmp, "styles.css")
        with open(html_file_path, "w") as f:
            f.write(compiled.html_content[0])
        with open(css_file_path, "w") as f:
            f.write(compiled.css_content)

        # Rendering the page
        render_path = os.path.join(tmp, "render.png")
        driver_info.driver.get("file://" + html_file_path)
        driver_info.driver.set_window_size(*size)
        driver_info.driver.save_screenshot(render_path)

        # Reading the image data
        array = np.array(Image.open(render_path))

    # Returning the image data
    return array
