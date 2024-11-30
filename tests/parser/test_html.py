from __future__ import annotations

import pyrogram
from pyrogram.parser.html import HTML


def test_html_unparse_bold() -> None:
    expected = "<b>bold</b>"
    text = "bold"
    entities = pyrogram.types.List(
        [
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.BOLD,
                offset=0,
                length=4,
            ),
        ],
    )

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_italic() -> None:
    expected = "<i>italic</i>"
    text = "italic"
    entities = pyrogram.types.List(
        [
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.ITALIC,
                offset=0,
                length=6,
            ),
        ],
    )

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_underline() -> None:
    expected = "<u>underline</u>"
    text = "underline"
    entities = pyrogram.types.List(
        [
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.UNDERLINE,
                offset=0,
                length=9,
            ),
        ],
    )

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_strike() -> None:
    expected = "<s>strike</s>"
    text = "strike"
    entities = pyrogram.types.List(
        [
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.STRIKETHROUGH,
                offset=0,
                length=6,
            ),
        ],
    )

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_spoiler() -> None:
    expected = "<spoiler>spoiler</spoiler>"
    text = "spoiler"
    entities = pyrogram.types.List(
        [
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.SPOILER,
                offset=0,
                length=7,
            ),
        ],
    )

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_url() -> None:
    expected = '<a href="https://pyrogram.org/">URL</a>'
    text = "URL"
    entities = pyrogram.types.List(
        [
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.TEXT_LINK,
                offset=0,
                length=3,
                url="https://pyrogram.org/",
            ),
        ],
    )

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_code() -> None:
    expected = "<code>code</code>"
    text = "code"
    entities = pyrogram.types.List(
        [
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.CODE,
                offset=0,
                length=4,
            ),
        ],
    )

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_pre() -> None:
    expected = """<pre language="python">for i in range(10):
    print(i)</pre>"""

    text = """for i in range(10):
    print(i)"""

    entities = pyrogram.types.List(
        [
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.PRE,
                offset=0,
                length=32,
                language="python",
            ),
        ],
    )

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_mixed() -> None:
    expected = (
        "<b>aaaaaaa<i>aaa<u>bbbb</u></i></b><u><i>bbbbbbccc</i></u><u>ccccccc<s>ddd</s></u><s>ddddd<spoiler>dd"
        "eee</spoiler></s><spoiler>eeeeeeefff</spoiler>ffff<code>fffggggggg</code>ggghhhhhhhhhh"
    )
    text = "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhh"
    entities = pyrogram.types.List(
        [
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.BOLD,
                offset=0,
                length=14,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.ITALIC,
                offset=7,
                length=7,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.UNDERLINE,
                offset=10,
                length=4,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.UNDERLINE,
                offset=14,
                length=9,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.ITALIC,
                offset=14,
                length=9,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.UNDERLINE,
                offset=23,
                length=10,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.STRIKETHROUGH,
                offset=30,
                length=3,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.STRIKETHROUGH,
                offset=33,
                length=10,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.SPOILER,
                offset=38,
                length=5,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.SPOILER,
                offset=43,
                length=10,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.CODE,
                offset=57,
                length=10,
            ),
        ],
    )

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_escaped() -> None:
    expected = "<b>&lt;b&gt;bold&lt;/b&gt;</b>"
    text = "<b>bold</b>"
    entities = pyrogram.types.List(
        [
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.BOLD,
                offset=0,
                length=11,
            ),
        ],
    )

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_escaped_nested() -> None:
    expected = (
        "<b>&lt;b&gt;bold <u>&lt;u&gt;underline&lt;/u&gt;</u> bold&lt;/b&gt;</b>"
    )
    text = "<b>bold <u>underline</u> bold</b>"
    entities = pyrogram.types.List(
        [
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.BOLD,
                offset=0,
                length=33,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.UNDERLINE,
                offset=8,
                length=16,
            ),
        ],
    )

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_no_entities() -> None:
    expected = "text"
    text = "text"
    entities = []

    assert HTML.unparse(text=text, entities=entities) == expected
