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

import os
import json


# Dictionary of HTML entities (character references) from the specification's
# JSON file. Maps character references to their corresponding characters and
# code points.
# Source: https://html.spec.whatwg.org/multipage/named-characters.html
with open(os.path.join(os.path.dirname(__file__),
                       "html_entities.json"), "r") as file:
    HTML_ENTITIES = json.load(file)


# Tuple of all entity names (e.g. "amp" is the name of the entity "&amp;").
HTML_ENTITY_NAMES = tuple(k.replace('&', '').replace(';', '')
                          for k in HTML_ENTITIES)


# Maps characters to their corresponding character references. Character references
# are sorted by increasing length, so short references (preferred) come first.
HTML_ENTITIES_INVERTED = {v["characters"]: tuple(sorted((
    k for k in HTML_ENTITIES
    if HTML_ENTITIES[k]["characters"] == v["characters"]
), key=len)) for v in HTML_ENTITIES.values()}
