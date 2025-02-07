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

from .html_entities import HTML_ENTITIES_INVERTED, HTML_ENTITY_NAMES
import re
from typing import Tuple


# Regular expression mathing all isolated '&' characters that are not part of an
# HTML entity.
_REGEX_AMP = re.compile(f"&(?!({'|'.join(HTML_ENTITY_NAMES)});?)")


# Regular expression matching all isolated ';' characters that are not part of an
# HTML entity. The expression essentially concatenates one lookbehind per entity.
_REGEXP_SEMI = re.compile(
    ''.join(f"(?<!&{e})" for e in HTML_ENTITY_NAMES) + ';')


# Entities that are always replaced during sanitization. These are: <, >, /,
# according to rule 13.1.2.6 of the HTML5 specification, as well as single quotes
# ', double quotes ", and new line characters '\n'.
# Source: https://html.spec.whatwg.org/multipage/syntax.html#cdata-rcdata-restrictions
_ALWAYS_SANITIZED = ("\u003C", "\u003E", "\u002F", "'", "\"", "\n")


# Entities other than new line characters '\n' (which requires special treatment)
# that are always replaced during sanitization.
_ALWAYS_SANITIZED_BUT_NEW_LINES = tuple(
    e for e in _ALWAYS_SANITIZED if e != '\n')


# Entities other than the ampersand and semicolon (which require special treatment
# because they are part of other entities) that are replaced by default during
# sanitization but can also be skipped for speed. This set of entities consists of
# all remaining entities but the ampersand and semicolon.
_OPTIONALLY_SANITIZED_BUT_AMP_SEMI = tuple(
    set(HTML_ENTITIES_INVERTED.keys()) - set(_ALWAYS_SANITIZED) - set({'&', ';'}))


def replace_html_entities(text: str, characters: Tuple[str]) -> str:
    """Replaces characters with their corresponding HTML entities in the given text.

    If a character can be represented by multiple entities, preference is given to
    the shortest one that contains a semicolon, in lowercase if possible.

    :param text: The input text containing HTML entities.
    :type text: str
    :param characters: The characters to be replaced by their HTML entity. Usually
        each item in the tuple is a single character, but some entities span
        multiple characters.
    :type characters: Tuple[str]
    :return: The text with HTML entities replaced.
    :rtype: str
    """
    for c in characters:
        entity = HTML_ENTITIES_INVERTED[c][0]  # Preferred is first
        text = text.replace(c, entity)
    return text


def sanitize_html_text(text: str, replace_all_entities: bool = True) -> str:
    """Sanitizes raw HTML text by replacing certain characters with HTML-friendly equivalents.

    Sanitization affects the following characters:
    - `<`, `/`, and `>`, replaced with their corresponding HTML entities
        ("&lt;", "&gt;", "&sol;") according to rule 13.1.2.6 of the HTML5
        specification (see source:
        https://html.spec.whatwg.org/multipage/syntax.html#cdata-rcdata-restrictions)
    - single quotes `'` and double quotes `"`, replaced with their corresponding
        HTML entities ("&apos;" and "&quot;")
    - new line characters '\\n', replaced with `br` tags
    - if `replace_all_entities` is True, every character that can be represented by
        an HTML entity is replaced with that entity. If a character can be
        represented by multiple entities, preference is given to the shortest one
        that contains a semicolon, in lowercase if possible.

    See https://html.spec.whatwg.org/multipage/named-characters.html for a list of
    all supported entities.

    :param text: The raw HTML text that needs sanitization.
    :type text: str
    :param replace_all_entities: Whether to replace every character that can be
        represented by an HTML entity. Use False to skip non-mandatory characters
        and increase speed. Default is True.
    :type replace_all_entities: bool
    :return: The sanitized HTML text.
    :rtype: str
    """
    # We start with all optional HTML entities, which enables us to replace all '&'
    # and ';' before subsequently introducing more of them.
    if replace_all_entities:

        # Replacing '&' ONLY when not part of an HTML entity itself
        text = _REGEX_AMP.sub('&amp;', text)

        # Replacing ';' ONLY when not part of an HTML entity itself
        text = _REGEXP_SEMI.sub('&semi;', text)

        # Replacing the remaining HTML entities
        text = replace_html_entities(text, _OPTIONALLY_SANITIZED_BUT_AMP_SEMI)

    # Then we replace all mandatory HTML entities
    text = replace_html_entities(text, _ALWAYS_SANITIZED_BUT_NEW_LINES)
    text = text.replace('\n', '<br>')  # Has to be last because of < and >

    return text
