from typing import Literal, Optional

from pydantic import AnyUrl, Field
from pydantic_api.base import BaseModel

from .base import BaseRichTextObject, TextAnnotations
from pydantic_api.notion.models.objects.common import ColorLiteral


class TextObjectLink(BaseModel):
    url: AnyUrl


class TextObject(BaseModel):
    """Text object type."""

    content: str
    link: TextObjectLink | None = Field(None, description="Link object or null")

    @classmethod
    def new(cls, content: str, link_url: str | None = None):
        """Creates a new TextObject."""
        link = None
        if link_url:
            link = TextObjectLink(url=AnyUrl(link_url))
        return cls(content=content, link=link)


class TextRichTextObject(BaseRichTextObject):
    """Rich Text type: Text."""

    type: Literal["text"] = "text"
    text: TextObject

    @classmethod
    def new(
        cls,
        content: str,
        link_url: str | None = None,
        bold: bool | None = None,
        italic: bool | None = None,
        strikethrough: bool | None = None,
        underline: bool | None = None,
        code: bool | None = None,
        color: ColorLiteral | None = None,
    ):
        annotations = None
        if any([bold, italic, strikethrough, underline, code, color]):
            annotations = TextAnnotations(
                bold=bold or False,
                italic=italic or False,
                strikethrough=strikethrough or False,
                underline=underline or False,
                code=code or False,
                color=color or "default",
            )
        return cls(
            text=TextObject.new(content=content, link_url=link_url),
            annotations=annotations,
        )


__all__ = [
    "TextObject",
    "TextRichTextObject",
]
