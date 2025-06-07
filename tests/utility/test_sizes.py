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
from webwidgets.utility.sizes import AbsoluteSize, RelativeSize, Size
import webwidgets as ww


class TestSizes:

    @pytest.mark.parametrize("value", [0, 10, 10.0, 12.33])
    def test_size(self, value):
        size = Size(value)
        assert size.value == value
        assert size.unit == "size"
        assert size.to_css() == f"{value}size"

    @pytest.mark.parametrize("class_to_test",
                             [AbsoluteSize, RelativeSize, Size])
    def test_size_helpers_not_at_top_level(self, class_to_test):
        """Tests the visibility of helper classes."""
        # Making sure the class exists in the proper sizes module
        assert hasattr(ww.utility.sizes, class_to_test.__name__)

        # Making sure it is not visible at the top level
        assert not hasattr(ww, class_to_test.__name__)

    def test_absolute_size_not_importable_at_top_level(self):
        with pytest.raises(AttributeError, match="AbsoluteSize"):
            ww.AbsoluteSize(5)

    def test_size_not_importable_at_top_level(self):
        with pytest.raises(AttributeError, match="Size"):
            ww.Size(5)

    def test_relative_size_not_importable_at_top_level(self):
        with pytest.raises(AttributeError, match="RelativeSize"):
            ww.RelativeSize(5)

    @pytest.mark.parametrize("value", [0, 10, 10.0, 82.33])
    def test_percent(self, value):
        size = ww.Percent(value)
        assert isinstance(size, RelativeSize)
        assert size.value == value
        assert size.unit == "%"
        assert size.to_css() == f"{value}%"

    @pytest.mark.parametrize("value", [0, 10, 10.0, 12.33])
    def test_px(self, value):
        size = ww.Px(value)
        assert isinstance(size, AbsoluteSize)
        assert size.value == value
        assert size.unit == "px"
        assert size.to_css() == f"{value}px"
