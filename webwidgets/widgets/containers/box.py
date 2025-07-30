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

from .container import Container
from dataclasses import dataclass
from typing import Any, Dict, Union
from webwidgets.compilation.html.html_tags import Div
from webwidgets.utility.enums import Direction
from webwidgets.widgets.widget import Widget


class Box(Container):
    """A widget that lays out its child widgets inside a row or a column.
    """

    def __init__(self, direction: Direction):
        """Creates a new Box with the given direction.

        :param direction: The direction in which the child widgets should be
            laid out. Can be either `Direction.HORIZONTAL` or
            `Direction.VERTICAL`.
        :type direction: Direction
        """
        super().__init__()
        self.direction = direction
        self._properties: Dict[int, BoxItemProperties] = {}

    def add(self, widget: Widget, space: Union[float, int] = 1) -> None:
        """Adds a widget to the box with an optional space coefficient.

        This function overrides :py:meth:`Container.add` from the base class to
        extend its functionality and save additional properties on each widget
        added to the box.

        :param widget: The widget to add to the box.
        :type widget: Widget
        :param space: The amount of space to allocate for the widget to live
            in, specified as a positive coefficient. The coefficient represents
            the weight to give to the widget during space allocation within the
            entire box.

            For example, if widget A has a space factor of 1 and widget B has a
            space factor of 2, B will be allocated twice as much space as A,
            i.e. a total of 2/3 of the entire box if the only widgets it
            contains are A and B.

            Note that this value controls the amount of free space available
            for the widget to grow in, not the size of the widget itself.
        :type space: Union[float, int]
        """
        super().add(widget=widget)
        self._properties[id(widget)] = BoxItemProperties(space=space)

    def build(self) -> Div:
        """Builds the HTML representation of the Box.

        The box is constructed as a `<div>` element with a flexbox layout. Its
        `flex-direction` property is set to either "row" or "column" based on
        the direction parameter, and it has a `data-role` attribute of "box".

        Each child widget is wrapped inside its own `<div>` element with a
        `data-role` attribute of "box-item". The items are centered within
        their own `<div>`.

        :return: A :py:class:`Div` element representing the Box.
        :rtype: Div
        """
        # Building child nodes and retrieving their properties
        nodes = [w.build() for w in self.widgets]
        properties = [self._properties[id(w)] for w in self.widgets]

        # Building box items that wrap around child nodes
        items = [Div(
            children=[node],
            attributes={"data-role": "box-item"},
            style={
                "display": "flex",
                "flex-direction": "row",
                "align-items": "center",
                "justify-content": "center"
            } | props.to_style()) for node, props in zip(nodes, properties)]

        # Assembling the box
        flex_dir = "row" if self.direction == Direction.HORIZONTAL else "column"
        box = Div(children=items, attributes={"data-role": "box"}, style={
            "display": "flex",
            "flex-direction": flex_dir
        })
        return box


@dataclass
class BoxItemProperties:
    """A utility dataclass to store extra properties to apply to a widget
    contained in a :py:class:`Box` during compilation.
    """

    space: int

    def to_style(self) -> Dict[str, str]:
        """Converts the properties of the :py:class:`BoxItemProperties`
        instance into a dictionary of CSS properties that can be added to the
        style of an HTML node.

        :return: A dictionary of CSS properties.
        :rtype: Dict[str, str]
        """
        return {"flex-grow": str(self.space)}
