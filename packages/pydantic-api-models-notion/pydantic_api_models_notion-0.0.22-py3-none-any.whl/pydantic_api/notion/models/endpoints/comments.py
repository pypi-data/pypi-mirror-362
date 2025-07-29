from typing import List, Optional

from uuid import UUID
from pydantic import BaseModel, Field, model_validator

from ..objects import CommentObject, RichTextObject, PageParentObject
from .base import NotionPaginatedData, StartCursor, PageSize


class CreateCommentRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/create-a-comment"""

    parent: Optional[PageParentObject] = Field(
        None,
        description="A page parent. Either this or a discussion_id is required (not both)",
    )
    discussion_id: Optional[UUID] = Field(
        None,
        description="A UUID identifier for a discussion thread. Either this or a parent object is required (not both)",
    )
    rich_text: List[RichTextObject] = Field(..., description="A rich text object")

    @model_validator(mode="after")
    def either_parent_or_discussionId_must_be_provided(self):
        if not self.parent and not self.discussion_id:
            raise ValueError("Either parent or discussion_id must be provided")
        return self


CreateCommentResponse = CommentObject
"""Reference: https://developers.notion.com/reference/create-a-comment"""


class RetrieveCommentsRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/retrieve-a-comment"""

    block_id: UUID = Field(
        ...,
        description="Identifier for a Notion block or page, a uuidv4 string. Reference: https://developers.notion.com/reference/block#keys",
    )
    start_cursor: Optional[StartCursor] = None
    page_size: Optional[PageSize] = None


RetrieveCommentsResponse = NotionPaginatedData[CommentObject]
"""Reference: https://developers.notion.com/reference/retrieve-a-comment"""


__all__ = [
    "CreateCommentRequest",
    "CreateCommentResponse",
    "RetrieveCommentsRequest",
    "RetrieveCommentsResponse",
]
