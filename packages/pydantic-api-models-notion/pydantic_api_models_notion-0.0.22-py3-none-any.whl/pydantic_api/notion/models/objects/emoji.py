"""
Reference: https://developers.notion.com/reference/emoji-object
"""

from typing import Literal

import emoji
from pydantic import field_validator, Field

from pydantic_api.base import BaseModel


class EmojiObject(BaseModel):
    """Reference: https://developers.notion.com/reference/emoji-object"""

    type: Literal["emoji"] = "emoji"
    emoji: str = Field(..., description="The emoji character.", examples=["😻"])

    @field_validator("emoji")
    @classmethod
    def ensure_valid_emoji_character(cls, v: str):
        # if len(v) > 1:
        # raise ValueError("Emoji must be a single character.")
        if not emoji.is_emoji(v):
            raise ValueError("Invalid emoji character: {v}")
        return v


__all__ = [
    "EmojiObject",
]
