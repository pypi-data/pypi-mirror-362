from typing import Annotated, Union

from pydantic import AnyUrl, Field

from .base import TextAnnotations
from .text import TextRichTextObject
from .mention import MentionRichTextObject
from .equation import EquationRichTextObject
from pydantic_api.notion.models.objects.common import ColorLiteral

RichTextObject = Annotated[
    Union[TextRichTextObject, MentionRichTextObject, EquationRichTextObject],
    Field(discriminator="type"),
]


# Factory class for Devlopers
class RichTextObjectFactory:
    @classmethod
    def new_text(
        cls,
        content: str,
        link_url: str | None = None,
        bold: bool | None = None,
        italic: bool | None = None,
        strikethrough: bool | None = None,
        underline: bool | None = None,
        code: bool | None = None,
        color: ColorLiteral | None = None,
        max_segment_len: int = 2000,
        separater: str = " ",
    ) -> list[RichTextObject]:
        """
        Create one or multiple TextRichTextObject instances based on content length.

        Args:
            content: The text content to convert.
            link_url: Hyperlink associated with the text.
            bold, italic, strikethrough, underline, code, color: Styling options.
            max_segment_len: Maximum length for each rich text object.
            separater: Word separator for splitting long text.

        Returns:
            A list of RichTextObject instances.
        """
        if link_url is not None and len(content) > max_segment_len:
            raise ValueError(
                f"Text length exceeds the maximum segment length of {max_segment_len} when a link is provided."
            )

        if not content:
            return []

        words = content.split(separater)
        segments = []
        current_segment = []
        current_length = 0

        for word in words:
            word_length = len(word)
            # If adding this word exceeds the max length, flush the current segment
            if current_length + word_length + len(separater) > max_segment_len:
                if current_segment:
                    segments.append(separater.join(current_segment))
                    current_segment = []
                    current_length = 0

            # If the word itself is too long, split it into smaller segments
            while word_length > max_segment_len:
                segments.append(word[:max_segment_len])
                word = word[max_segment_len:]
                word_length = len(word)

            # Add the remaining word to the current segment
            current_segment.append(word)
            current_length += word_length + len(separater)

        # Flush the last segment
        if current_segment:
            segments.append(separater.join(current_segment))

        # Convert segments to RichTextObject instances
        rich_text_objects = [
            TextRichTextObject.new(
                content=segment,
                link_url=link_url,
                bold=bold,
                italic=italic,
                strikethrough=strikethrough,
                underline=underline,
                code=code,
                color=color,
            )
            for segment in segments
        ]
        return rich_text_objects

    @classmethod
    def new_equation(cls, expression: str):
        return EquationRichTextObject.new(expression=expression)

    @classmethod
    def new_mention(cls):
        raise NotImplementedError(
            f"Factory method for Mention object is not implemented yet."
        )


__all__ = [
    "RichTextObject",
    "RichTextObjectFactory",
]
