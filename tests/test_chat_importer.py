from __future__ import annotations

import json

from schemamath_api.chat_importer import parse_chat
from schemamath_api.domain import ImportFormat


def test_parse_markdown_html_and_generic_json() -> None:
    markdown = parse_chat(
        "conversation.md",
        "text/markdown",
        b"# User\nQuestion\n\n# Assistant\nCandidate answer",
    )
    assert markdown.import_format == ImportFormat.MARKDOWN
    assert [message[0] for message in markdown.messages] == ["user", "assistant"]

    html = parse_chat(
        "conversation.html",
        "text/html",
        b"<html><body><div data-message-author-role='user'>Question</div>"
        b"<div data-message-author-role='assistant'>Answer</div></body></html>",
    )
    assert html.import_format == ImportFormat.HTML
    assert [message[1] for message in html.messages] == ["Question", "Answer"]

    payload = json.dumps(
        {
            "messages": [
                {"role": "user", "content": "Question"},
                {"role": "assistant", "content": "Answer"},
            ]
        }
    ).encode()
    parsed_json = parse_chat("conversation.json", "application/json", payload)
    assert parsed_json.import_format == ImportFormat.JSON
    assert len(parsed_json.messages) == 2


def test_parse_chatgpt_mapping_export() -> None:
    payload = {
        "mapping": {
            "1": {
                "message": {
                    "author": {"role": "user"},
                    "content": {"parts": ["Question"]},
                    "create_time": 1,
                }
            },
            "2": {
                "message": {
                    "author": {"role": "assistant"},
                    "content": {"parts": ["Answer"]},
                    "create_time": 2,
                }
            },
        }
    }
    parsed = parse_chat("chatgpt-export.json", "application/json", json.dumps(payload).encode())
    assert parsed.import_format == ImportFormat.JSON
    assert [message[0] for message in parsed.messages] == ["user", "assistant"]
