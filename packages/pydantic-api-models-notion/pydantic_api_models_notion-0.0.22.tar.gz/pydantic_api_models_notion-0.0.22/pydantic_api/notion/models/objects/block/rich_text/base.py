from typing import Literal, Optional

from pydantic import AnyHttpUrl, Field

from pydantic_api.base import BaseModel

from pydantic_api.notion.models.objects.common import ColorLiteral


class TextAnnotations(BaseModel):
    """Text style annotations for rich text."""

    bold: bool
    italic: bool
    strikethrough: bool
    underline: bool
    code: bool
    color: ColorLiteral


RichTextTypeLiteral = Literal["text", "mention", "equation"]


class BaseRichTextObject(BaseModel):
    """Base model for Rich Text."""

    type: RichTextTypeLiteral
    annotations: Optional[TextAnnotations] = Field(
        None, description="Formatting style for the text"
    )
    plain_text: Optional[str] = Field(None)
    href: Optional[AnyHttpUrl] = Field(None, description="Hyperlink for the text")


__all__ = [
    "TextAnnotations",
    "RichTextTypeLiteral",
    "BaseRichTextObject",
]
