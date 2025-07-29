"""
Reference: https://developers.notion.com/reference/comment-object
"""

from typing import Literal, List, Union
from datetime import datetime

from uuid import UUID

from pydantic_api.base import BaseModel
from .user import PartialUser
from .block import RichTextObject
from .parent import BlockParentObject, PageParentObject


ParentOfComment = Union[BlockParentObject, PageParentObject]
"""Reference: https://developers.notion.com/reference/comment-object#all-comments"""


class CommentObject(BaseModel):
    """Comment Object

    Reference: https://developers.notion.com/reference/comment-object
    """

    object: Literal["comment"] = "comment"
    id: UUID
    parent: ParentOfComment
    discussion_id: UUID
    created_time: datetime
    last_edited_time: datetime
    created_by: PartialUser
    rich_text: List[RichTextObject]


__all__ = [
    "ParentOfComment",
    "CommentObject",
]
