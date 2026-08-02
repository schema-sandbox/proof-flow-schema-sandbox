from __future__ import annotations

import json
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from uuid import uuid4

from .domain import ChatMessageCandidate, ImportDisposition, ImportFormat

ROLE_RE = re.compile(
    r"^\s{0,3}(?:#{1,6}\s*)?(user|assistant|system|tool|human|chatgpt|model)\s*[:：-]?\s*$",
    re.IGNORECASE,
)
INLINE_ROLE_RE = re.compile(
    r"^\s*(user|assistant|system|tool|human|chatgpt|model)\s*[:：]\s*(.*)$",
    re.IGNORECASE,
)


@dataclass(frozen=True, slots=True)
class ParsedChat:
    import_format: ImportFormat
    parser_name: str
    messages: list[tuple[str, str]]


class _VisibleHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._ignored_depth = 0
        self._current_role: str | None = None
        self._current_chunks: list[str] = []
        self.messages: list[tuple[str, str]] = []
        self.fallback_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self._ignored_depth += 1
            return
        attrs_dict = {key: value or "" for key, value in attrs}
        role = attrs_dict.get("data-message-author-role") or attrs_dict.get("data-author")
        if role:
            self._flush_message()
            self._current_role = normalize_role(role)
        if tag in {"p", "div", "li", "br", "pre", "code", "h1", "h2", "h3", "h4"}:
            self._append_text("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self._ignored_depth:
            self._ignored_depth -= 1
            return
        if tag in {"article", "section"} and self._current_role:
            self._flush_message()
        if tag in {"p", "div", "li", "pre", "h1", "h2", "h3", "h4"}:
            self._append_text("\n")

    def handle_data(self, data: str) -> None:
        if self._ignored_depth:
            return
        self._append_text(data)

    def close(self) -> None:
        super().close()
        self._flush_message()

    def _append_text(self, value: str) -> None:
        if self._current_role:
            self._current_chunks.append(value)
        else:
            self.fallback_chunks.append(value)

    def _flush_message(self) -> None:
        if not self._current_role:
            return
        text = normalize_text("".join(self._current_chunks))
        if text:
            self.messages.append((self._current_role, text))
        self._current_role = None
        self._current_chunks = []


def normalize_role(role: str) -> str:
    normalized = role.strip().lower()
    if normalized in {"human", "user"}:
        return "user"
    if normalized in {"assistant", "chatgpt", "model"}:
        return "assistant"
    if normalized in {"system", "tool"}:
        return normalized
    return "unknown"


def normalize_text(value: str) -> str:
    lines = [line.rstrip() for line in value.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    compacted: list[str] = []
    blank = False
    for line in lines:
        if not line.strip():
            if compacted and not blank:
                compacted.append("")
            blank = True
            continue
        compacted.append(line)
        blank = False
    return "\n".join(compacted).strip()


def detect_import_format(filename: str, media_type: str | None, content: bytes) -> ImportFormat:
    suffix = Path(filename).suffix.lower()
    if suffix in {".md", ".markdown"} or media_type in {"text/markdown", "text/x-markdown"}:
        return ImportFormat.MARKDOWN
    if suffix in {".html", ".htm", ".mhtml"} or media_type in {
        "text/html",
        "application/xhtml+xml",
    }:
        return ImportFormat.HTML
    if suffix == ".json" or media_type == "application/json":
        return ImportFormat.JSON
    stripped = content.lstrip()
    if stripped.startswith((b"{", b"[")):
        return ImportFormat.JSON
    if (
        b"<html" in stripped[:1000].lower()
        or b"data-message-author-role" in stripped[:5000].lower()
    ):
        return ImportFormat.HTML
    return ImportFormat.PLAIN_TEXT


def parse_chat(filename: str, media_type: str | None, content: bytes) -> ParsedChat:
    import_format = detect_import_format(filename, media_type, content)
    text = content.decode("utf-8", errors="replace")
    if import_format == ImportFormat.JSON:
        return _parse_json(text)
    if import_format == ImportFormat.HTML:
        return _parse_html(text)
    if import_format == ImportFormat.MARKDOWN:
        return _parse_markdown(text)
    return _parse_plain_text(text)


def _parse_markdown(text: str) -> ParsedChat:
    messages: list[tuple[str, str]] = []
    current_role: str | None = None
    chunks: list[str] = []

    def flush() -> None:
        nonlocal chunks, current_role
        body = normalize_text("\n".join(chunks))
        if body:
            messages.append((current_role or "unknown", body))
        chunks = []

    for line in text.splitlines():
        heading = ROLE_RE.match(line)
        if heading:
            flush()
            current_role = normalize_role(heading.group(1))
            continue
        inline = INLINE_ROLE_RE.match(line)
        if inline:
            flush()
            current_role = normalize_role(inline.group(1))
            if inline.group(2):
                chunks.append(inline.group(2))
            continue
        chunks.append(line)
    flush()
    if not messages:
        messages = [("unknown", normalize_text(text))]
    return ParsedChat(ImportFormat.MARKDOWN, "markdown-role-sections-v1", messages)


def _parse_plain_text(text: str) -> ParsedChat:
    parsed = _parse_markdown(text)
    return ParsedChat(ImportFormat.PLAIN_TEXT, "plain-role-lines-v1", parsed.messages)


def _parse_html(text: str) -> ParsedChat:
    parser = _VisibleHTMLParser()
    parser.feed(text)
    parser.close()
    if parser.messages:
        return ParsedChat(ImportFormat.HTML, "html-data-author-role-v1", parser.messages)
    fallback = normalize_text("".join(parser.fallback_chunks))
    parsed = _parse_markdown(fallback)
    return ParsedChat(ImportFormat.HTML, "html-visible-text-v1", parsed.messages)


def _parse_json(text: str) -> ParsedChat:
    data = json.loads(text)
    messages = _extract_json_messages(data)
    if not messages:
        messages = [("unknown", normalize_text(json.dumps(data, ensure_ascii=False, indent=2)))]
    return ParsedChat(ImportFormat.JSON, "json-chat-structures-v1", messages)


def _extract_json_messages(data: Any) -> list[tuple[str, str]]:
    if isinstance(data, dict) and isinstance(data.get("messages"), list):
        return _extract_message_list(data["messages"])
    if isinstance(data, list):
        direct = _extract_message_list(data)
        if direct:
            return direct
        collected: list[tuple[str, str]] = []
        for item in data:
            collected.extend(_extract_json_messages(item))
        return collected
    if isinstance(data, dict) and isinstance(data.get("mapping"), dict):
        rows: list[tuple[float, str, str]] = []
        for node in data["mapping"].values():
            if not isinstance(node, dict):
                continue
            message = node.get("message")
            if not isinstance(message, dict):
                continue
            author = message.get("author") or {}
            role = normalize_role(str(author.get("role", "unknown")))
            content = message.get("content") or {}
            parts = content.get("parts") if isinstance(content, dict) else None
            text = _parts_to_text(parts)
            if not text:
                continue
            created = message.get("create_time")
            try:
                order = float(created)
            except (TypeError, ValueError):
                order = float(len(rows))
            rows.append((order, role, text))
        rows.sort(key=lambda item: item[0])
        return [(role, text) for _, role, text in rows]
    if isinstance(data, dict):
        role = normalize_role(str(data.get("role", data.get("author", "unknown"))))
        text_value = data.get("content", data.get("text", data.get("message")))
        text = _coerce_text(text_value)
        if text:
            return [(role, text)]
    return []


def _extract_message_list(items: list[Any]) -> list[tuple[str, str]]:
    messages: list[tuple[str, str]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        author = item.get("author")
        if isinstance(author, dict):
            role_value = author.get("role", "unknown")
        else:
            role_value = item.get("role", author or "unknown")
        role = normalize_role(str(role_value))
        text = _coerce_text(item.get("content", item.get("text", item.get("message"))))
        if text:
            messages.append((role, text))
    return messages


def _coerce_text(value: Any) -> str:
    if isinstance(value, str):
        return normalize_text(value)
    if isinstance(value, list):
        return _parts_to_text(value)
    if isinstance(value, dict):
        if isinstance(value.get("parts"), list):
            return _parts_to_text(value["parts"])
        if isinstance(value.get("text"), str):
            return normalize_text(value["text"])
        return normalize_text(json.dumps(value, ensure_ascii=False))
    return ""


def _parts_to_text(parts: Any) -> str:
    if not isinstance(parts, list):
        return ""
    chunks: list[str] = []
    for part in parts:
        if isinstance(part, str):
            chunks.append(part)
        elif isinstance(part, dict):
            if isinstance(part.get("text"), str):
                chunks.append(part["text"])
            else:
                chunks.append(json.dumps(part, ensure_ascii=False))
    return normalize_text("\n\n".join(chunks))


def suggested_disposition(role: str, content: str) -> ImportDisposition:
    lower = content.lower()
    if role == "user":
        return ImportDisposition.MODEL_NOTE
    if any(
        token in lower
        for token in ("counterexample", "objection", "fatal flaw", "fails when", "contradiction")
    ):
        return ImportDisposition.CHALLENGE
    if any(
        token in lower
        for token in ("bridge result", "intermediate result", "enables the next", "useful lemma")
    ):
        return ImportDisposition.BRIDGE_RESULT
    if any(
        token in lower
        for token in (
            "current target",
            "unresolved obligations",
            "next route",
            "research checkpoint",
        )
    ):
        return ImportDisposition.RESEARCH_CHECKPOINT
    if any(
        token in lower
        for token in (
            "new route",
            "alternative approach",
            "try instead",
            "different representation",
        )
    ):
        return ImportDisposition.NEW_BRANCH
    return ImportDisposition.MODEL_NOTE


def to_candidates(
    messages: list[tuple[str, str]], maximum_messages: int = 500
) -> list[ChatMessageCandidate]:
    candidates: list[ChatMessageCandidate] = []
    for sequence, (role, content) in enumerate(messages[:maximum_messages]):
        cleaned = normalize_text(content)
        if not cleaned:
            continue
        candidates.append(
            ChatMessageCandidate(
                candidate_id=uuid4(),
                sequence=sequence,
                role=normalize_role(role),
                content=cleaned,
                suggested_disposition=suggested_disposition(role, cleaned),
            )
        )
    return candidates
