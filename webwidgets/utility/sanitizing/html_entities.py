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


# Maps characters to their corresponding character references. If a character can be
# represented by multiple entities, the preferred one is placed first in the tuple.
# Preference is given to the shortest one with a semicolon, in lowercase if possible
# (e.g. "&amp;").
HTML_ENTITIES_INVERTED = {v["characters"]: sorted([
    k for k in HTML_ENTITIES
    if HTML_ENTITIES[k]["characters"] == v["characters"]
], key=len) for v in HTML_ENTITIES.values()}
for _, entities in HTML_ENTITIES_INVERTED.items():
    e = next((e for e in entities if ';' in e), entities[0])
    i = entities.index(e.lower() if e.lower() in entities else e)
    entities[i], entities[0] = entities[0], entities[i]
HTML_ENTITIES_INVERTED = {k: tuple(v)
                          for k, v in HTML_ENTITIES_INVERTED.items()}
