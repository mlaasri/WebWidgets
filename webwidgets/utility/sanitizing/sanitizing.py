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


# Regular expression mathing all isolated '&' characters that are not part of an
# HTML entity.
_REGEX_AMP = re.compile(f"&(?!({'|'.join(HTML_ENTITY_NAMES)});?)")


# Regular expression matching all isolated ';' characters that are not part of an
# HTML entity. The expression essentially concatenates one lookbehind per entity.
_REGEXP_SEMI = re.compile(
    ''.join(f"(?<!&{e})" for e in HTML_ENTITY_NAMES) + ';')


# Entities that are always replaced during sanitization. These are: &, <, >, /,
# according to rule 13.1.2.6 of the HTML5 specification, and new line characters
# '\n'.
# Source: https://html.spec.whatwg.org/multipage/syntax.html#cdata-rcdata-restrictions
_ALWAYS_SANITIZED = ("\u0026", "\u003C", "\u003E", "\u002F", "\n")


# Entities other than the semicolon (which requires special treatment) that are
# replaced by default during sanitization but can also be skipped for speed. This
# set of entities consists of all remaining entities but the semicolon.
_OPTIONALLY_SANITIZED_BUT_SEMI = tuple(
    set(HTML_ENTITIES_INVERTED.keys()) - set(_ALWAYS_SANITIZED) - set(';'))


def sanitize_html_text(text: str, replace_all_entities: bool = True) -> str:
    """Sanitizes raw HTML text by replacing certain characters with HTML-friendly equivalents.

    Sanitization affects the following characters:
    - '<', '/', and '>', replaced with their corresponding HTML entities
        ("&lt;", "&gt;", "&sol;") according to rule 13.1.2.6 of the HTML5
        specification (see source:
        https://html.spec.whatwg.org/multipage/syntax.html#cdata-rcdata-restrictions)
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
    if replace_all_entities:

        # Replacing '&' ONLY when not part of an HTML entity itself
        text = _REGEX_AMP.sub('&amp;', text)

    # Then we replace '<', '/', and '>' with their corresponding HTML entities.
    text = text.replace('<', '&lt;').replace(
        '>', '&gt;').replace("\u002F", '&sol;')

    # If requested, we then replace all remaining HTML entities
    if replace_all_entities:

        # Replacing ';' ONLY when not part of an HTML entity itself
        text = _REGEXP_SEMI.sub('&semi;', text)

        # Replacing the remaining HTML entities
        for characters in _OPTIONALLY_SANITIZED_BUT_SEMI:

            # Retrieving the HTML entity(s) for these characters
            entities = HTML_ENTITIES_INVERTED[characters]

            # Preferred format is shortest, lowercase with semicolon (e.g. "&amp;").
            # Entities are sorted by increasing length in HTML_ENTITIES_INVERTED, so
            # we can just use next() to retrieved the preferred entity.
            e = next((e for e in entities if ';' in e), entities[0])
            if e.lower() in entities:
                e = e.lower()

            # Replacing the characters with the preferred HTML entity
            text = text.replace(characters, e)

    # Finally we replace every new line with <br>
    text = text.replace('\n', '<br>')

    return text
