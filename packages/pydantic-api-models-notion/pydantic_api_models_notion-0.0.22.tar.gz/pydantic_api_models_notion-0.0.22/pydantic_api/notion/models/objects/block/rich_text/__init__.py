"""
Reference: https://developers.notion.com/reference/rich-text
"""

from .base import TextAnnotations, RichTextTypeLiteral
from .text import TextObject, TextRichTextObject
from .equation import EquationObject, EquationRichTextObject
from .mention import (
    MentionTypeLiteral,
    DatabaseMentionBody,
    DatabaseMentionObject,
    DateMentionBody,
    DateMentionObject,
    LinkPreviewMentionBody,
    LinkPreviewMentionObject,
    PageMentionBody,
    PageMentionObject,
    TemplateMentionBody,
    TemplateMentionObject,
    TemplateMentionTypeLiteral,
    TemplateMentionDateValueLiteral,
    TemplateMentionUserValueLiteral,
    UserMentionBody,
    UserMentionObject,
    MentionObject,
    MentionRichTextObject,
)
from .rich_text import RichTextObject, RichTextObjectFactory


__all__ = [
    # Base
    "TextAnnotations",
    "RichTextTypeLiteral",
    # Text
    "TextObject",
    "TextRichTextObject",
    # Equation
    "EquationObject",
    "EquationRichTextObject",
    # Mention
    "MentionTypeLiteral",
    "DatabaseMentionBody",
    "DatabaseMentionObject",
    "DateMentionBody",
    "DateMentionObject",
    "LinkPreviewMentionBody",
    "LinkPreviewMentionObject",
    "PageMentionBody",
    "PageMentionObject",
    "TemplateMentionBody",
    "TemplateMentionObject",
    "TemplateMentionTypeLiteral",
    "TemplateMentionDateValueLiteral",
    "TemplateMentionUserValueLiteral",
    "UserMentionBody",
    "UserMentionObject",
    "MentionObject",
    "MentionRichTextObject",
    # Rich Text
    "RichTextObject",
    "RichTextObjectFactory",
]
