from __future__ import annotations

import pyrogram
from pyrogram.parser.markdown import Markdown


def test_markdown_unparse_bold():
    expected = "**bold**"
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

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_italic():
    expected = "__italic__"
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

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_strike():
    expected = "~~strike~~"
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

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_spoiler():
    expected = "||spoiler||"
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

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_url():
    expected = "[URL](https://pyrogram.org/)"
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

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_code():
    expected = "`code`"
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

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_pre():
    expected = """```python
for i in range(10):
    print(i)
```"""

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

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_blockquote():
    expected = """> Hello
> from

> pyrogram!"""

    text = """Hello\nfrom\n\npyrogram!"""

    entities = pyrogram.types.List(
        [
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.BLOCKQUOTE,
                offset=0,
                length=10,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.BLOCKQUOTE,
                offset=12,
                length=9,
            ),
        ],
    )

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_mixed():
    expected = "**aaaaaaa__aaabbb**__~~dddddddd||ddeee~~||||eeeeeeefff||ffff`fffggggggg`ggghhhhhhhhhh"
    text = "aaaaaaaaaabbbddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhh"
    entities = pyrogram.types.List(
        [
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.BOLD,
                offset=0,
                length=13,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.ITALIC,
                offset=7,
                length=6,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.STRIKETHROUGH,
                offset=13,
                length=13,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.SPOILER,
                offset=21,
                length=5,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.SPOILER,
                offset=26,
                length=10,
            ),
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.CODE,
                offset=40,
                length=10,
            ),
        ],
    )

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_no_entities():
    expected = "text"
    text = "text"
    entities = []

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_html():
    expected = "__This works, it's ok__ <b>This shouldn't</b>"
    text = "This works, it's ok <b>This shouldn't</b>"
    entities = pyrogram.types.List(
        [
            pyrogram.types.MessageEntity(
                type=pyrogram.enums.MessageEntityType.ITALIC,
                offset=0,
                length=19,
            ),
        ],
    )

    assert Markdown.unparse(text=text, entities=entities) == expected
