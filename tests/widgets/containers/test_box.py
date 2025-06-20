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

import numpy as np
import pytest
from typing import Tuple
import webwidgets as ww
from webwidgets.compilation.html import Div


class TestBox:

    # A simple color widget
    class Color(ww.Widget):
        def __init__(self, color: Tuple[int, int, int]):
            super().__init__()
            self.color = color

        def build(self):
            hex_color = "#%02x%02x%02x" % self.color
            return Div(style={"background-color": hex_color,
                              "height": "100%",
                              "width": "100%"})

    # A Box that fills the entire viewport
    class FullViewportBox(ww.Box):
        def build(self, *args, **kwargs):
            node = super().build(*args, **kwargs)
            node.style["width"] = "100vw"
            node.style["height"] = "100vh"
            return node

    # A Box that expands to 100% of its available space
    class FullyExpandedBox(ww.Box):
        def build(self, *args, **kwargs):
            node = super().build(*args, **kwargs)
            node.style["width"] = "100%"
            node.style["height"] = "100%"
            return node

    @pytest.mark.parametrize("colors", [
        [(255, 0, 0)],
        [(255, 0, 0), (0, 255, 0)],
        [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    ])
    def test_horizontal_box(self, colors, render_page, web_drivers):
        """Tests the even distribution of multiple colored widgets by a Box."""
        # Creating a page with one box containing widgets with the given colors
        box = TestBox.FullViewportBox(direction=ww.Direction.HORIZONTAL)
        for color in colors:
            box.add(TestBox.Color(color=color))
        page = ww.Page([box])

        for web_driver in web_drivers:

            # Rendering the page with the box
            array = render_page(page, web_driver)

            # Computing the regions where to search for each color. If the
            # colors cannot spread evenly (which happens when the image size is
            # not divisible by the number of colors), we exclude all edges
            # where one color stops and another starts.
            all_indices = np.arange(array.shape[1])
            edges = np.linspace(0, array.shape[1], len(colors) + 1)[1:-1]
            edges = np.floor(edges).astype(np.int32)
            regions = np.split(all_indices, edges)
            if array.shape[1] % len(colors) != 0:
                regions = [r[~np.isin(r, edges)] for r in regions]

            assert len(regions) == len(colors)  # One region per color
            for color, region in zip(colors, regions):
                assert np.all(array[:, region, 0] == color[0])
                assert np.all(array[:, region, 1] == color[1])
                assert np.all(array[:, region, 2] == color[2])

    @pytest.mark.parametrize("colors", [
        [(255, 0, 0)],
        [(255, 0, 0), (0, 255, 0)],
        [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    ])
    def test_vertical_box(self, colors, render_page, web_drivers):
        """Tests the even distribution of multiple colored widgets by a Box."""
        # Creating a page with one box containing widgets with the given colors
        box = TestBox.FullViewportBox(direction=ww.Direction.VERTICAL)
        for color in colors:
            box.add(TestBox.Color(color=color))
        page = ww.Page([box])

        for web_driver in web_drivers:

            # Rendering the page with the box
            array = render_page(page, web_driver)

            # Computing the regions where to search for each color. If the
            # colors cannot spread evenly (which happens when the image size is
            # not divisible by the number of colors), we exclude all edges
            # where one color stops and another starts.
            all_indices = np.arange(array.shape[0])
            edges = np.linspace(0, array.shape[0], len(colors) + 1)[1:-1]
            edges = np.floor(edges).astype(np.int32)
            regions = np.split(all_indices, edges)
            if array.shape[0] % len(colors) != 0:
                regions = [r[~np.isin(r, edges)] for r in regions]

            assert len(regions) == len(colors)  # One region per color
            for color, region in zip(colors, regions):
                assert np.all(array[region, :, 0] == color[0])
                assert np.all(array[region, :, 1] == color[1])
                assert np.all(array[region, :, 2] == color[2])

    def test_nested_boxes(self, render_page, web_drivers):
        """Tests that two nested boxes with orthogonal directions render
        correctly.
        """
        top_box = TestBox.FullyExpandedBox(direction=ww.Direction.HORIZONTAL)
        top_box.add(TestBox.Color(color=(255, 0, 0)))
        top_box.add(TestBox.Color(color=(0, 255, 0)))
        out_box = TestBox.FullViewportBox(direction=ww.Direction.VERTICAL)
        out_box.add(top_box)
        out_box.add(TestBox.Color(color=(0, 0, 255)))
        page = ww.Page([out_box])

        for web_driver in web_drivers:
            a = render_page(page, web_driver)
            for i, c in enumerate((255, 0, 0)):
                assert np.all(a[:a.shape[0] // 2, :a.shape[1] // 2, i] == c)
            edge_col = a.shape[1] // 2 + (0 if a.shape[1] % 2 == 0 else 1)
            for i, c in enumerate((0, 255, 0)):
                assert np.all(a[:a.shape[0] // 2, edge_col:, i] == c)
            edge_row = a.shape[0] // 2 + (0 if a.shape[0] % 2 == 0 else 1)
            for i, c in enumerate((0, 0, 255)):
                assert np.all(a[edge_row:, :, i] == c)

    @pytest.mark.parametrize("green_space", [
        2, 3, 4,  # as int
        2.0, 3.0, 4.0  # as float
    ])
    @pytest.mark.parametrize("explicit_default", [True, False])
    def test_horizontal_box_spacing_two_colors(self, green_space,
                                               explicit_default, render_page,
                                               web_drivers):
        # Creating a page with one box containing Color widgets
        box = TestBox.FullViewportBox(direction=ww.Direction.HORIZONTAL)
        if explicit_default:
            box.add(TestBox.Color(color=(255, 0, 0)), space=1)
        else:
            box.add(TestBox.Color(color=(255, 0, 0)))
        box.add(TestBox.Color(color=(0, 255, 0)), space=green_space)
        page = ww.Page([box])

        for web_driver in web_drivers:

            # Rendering the page with the box
            array = render_page(page, web_driver)

            # Computing the expected red and green regions, avoiding the edge
            # if colors cannot spread evenly
            all_indices = np.arange(array.shape[1])
            edge = array.shape[1] // (int(green_space) + 1)
            red, green = np.split(all_indices, [edge])
            if array.shape[1] % (int(green_space) + 1) != 0:
                green = green[green != edge]

            # Testing than first region is red and second region is green
            assert np.all(array[:, red, 0] == 255)
            assert np.all(array[:, red, 1] == 0)
            assert np.all(array[:, red, 2] == 0)
            assert np.all(array[:, green, 0] == 0)
            assert np.all(array[:, green, 1] == 255)
            assert np.all(array[:, green, 2] == 0)

    @pytest.mark.parametrize("green_space", [
        2, 3, 4,  # as int
        2.0, 3.0, 4.0  # as float
    ])
    @pytest.mark.parametrize("explicit_default", [True, False])
    def test_vertical_box_spacing_two_colors(self, green_space,
                                             explicit_default, render_page,
                                             web_drivers):
        # Creating a page with one box containing Color widgets
        box = TestBox.FullViewportBox(direction=ww.Direction.VERTICAL)
        if explicit_default:
            box.add(TestBox.Color(color=(255, 0, 0)), space=1)
        else:
            box.add(TestBox.Color(color=(255, 0, 0)))
        box.add(TestBox.Color(color=(0, 255, 0)), space=green_space)
        page = ww.Page([box])

        for web_driver in web_drivers:

            # Rendering the page with the box
            array = render_page(page, web_driver)

            # Computing the expected red and green regions, avoiding the edge
            # if colors cannot spread evenly
            all_indices = np.arange(array.shape[0])
            edge = array.shape[0] // (int(green_space) + 1)
            red, green = np.split(all_indices, [edge])
            if array.shape[0] % (int(green_space) + 1) != 0:
                green = green[green != edge]

            # Testing than first region is red and second region is green
            assert np.all(array[red, :, 0] == 255)
            assert np.all(array[red, :, 1] == 0)
            assert np.all(array[red, :, 2] == 0)
            assert np.all(array[green, :, 0] == 0)
            assert np.all(array[green, :, 1] == 255)
            assert np.all(array[green, :, 2] == 0)

    @pytest.mark.parametrize("spaces", [
        (2, 2, 2, 2), (1, 2, 3, 4),
        (1, 2, 2, 0.5), (1, 0.25, 0.75, 3)  # Mixed types
    ])
    def test_horizontal_box_spacing_more_colors(self, spaces, render_page,
                                                web_drivers):
        spaces = np.array(spaces)

        # Creating a page with one box containing Color widgets
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)
        ]
        box = TestBox.FullViewportBox(direction=ww.Direction.HORIZONTAL)
        for color, space in zip(colors, spaces):
            box.add(TestBox.Color(color=color), space=space)
        page = ww.Page([box])

        for web_driver in web_drivers:

            # Rendering the page with the box
            array = render_page(page, web_driver)

            # Computing the expected colored regions, avoiding all edges even
            # if colors spread evenly
            all_indices = np.arange(array.shape[1])
            edges = array.shape[1] * (spaces.cumsum() / spaces.sum())[:-1]
            edges = np.floor(edges).astype(np.int32)
            regions = np.split(all_indices, edges)
            regions = [r[~np.isin(r, edges)] for r in regions]

            # Testing each region
            for color, region in zip(colors, regions):
                assert np.all(array[:, region, 0] == color[0])
                assert np.all(array[:, region, 1] == color[1])
                assert np.all(array[:, region, 2] == color[2])

    @pytest.mark.parametrize("spaces", [
        (2, 2, 2, 2), (1, 2, 3, 4),
        (1, 2, 2, 0.5), (1, 0.25, 0.75, 3)  # Mixed types
    ])
    def test_vertical_box_spacing_more_colors(self, spaces, render_page,
                                              web_drivers):
        spaces = np.array(spaces)

        # Creating a page with one box containing Color widgets
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)
        ]
        box = TestBox.FullViewportBox(direction=ww.Direction.VERTICAL)
        for color, space in zip(colors, spaces):
            box.add(TestBox.Color(color=color), space=space)
        page = ww.Page([box])

        for web_driver in web_drivers:

            # Rendering the page with the box
            array = render_page(page, web_driver)

            # Computing the expected colored regions, avoiding all edges even
            # if colors spread evenly
            all_indices = np.arange(array.shape[0])
            edges = array.shape[0] * (spaces.cumsum() / spaces.sum())[:-1]
            edges = np.floor(edges).astype(np.int32)
            regions = np.split(all_indices, edges)
            regions = [r[~np.isin(r, edges)] for r in regions]

            # Testing each region
            for color, region in zip(colors, regions):
                assert np.all(array[region, :, 0] == color[0])
                assert np.all(array[region, :, 1] == color[1])
                assert np.all(array[region, :, 2] == color[2])

    def test_nested_boxes_with_spacing(self, render_page, web_drivers):
        """Tests that two nested boxes with orthogonal directions and uneven
        spacing rules render correctly.
        """
        top_box = TestBox.FullyExpandedBox(direction=ww.Direction.HORIZONTAL)
        top_box.add(TestBox.Color(color=(255, 0, 0)))
        top_box.add(TestBox.Color(color=(0, 255, 0)), space=3)
        out_box = TestBox.FullViewportBox(direction=ww.Direction.VERTICAL)
        out_box.add(top_box, space=0.5)
        out_box.add(TestBox.Color(color=(0, 0, 255)))
        page = ww.Page([out_box])

        for web_driver in web_drivers:
            a = render_page(page, web_driver)
            for i, c in enumerate((255, 0, 0)):
                assert np.all(a[:a.shape[0] // 3, :a.shape[1] // 4, i] == c)
            edge_col = a.shape[1] // 4 + (0 if a.shape[1] % 4 == 0 else 1)
            for i, c in enumerate((0, 255, 0)):
                assert np.all(a[:a.shape[0] // 3, edge_col:, i] == c)
            edge_row = a.shape[0] // 3 + (0 if a.shape[0] % 3 == 0 else 1)
            for i, c in enumerate((0, 0, 255)):
                assert np.all(a[edge_row:, :, i] == c)
