from typing import List, Optional

from pydantic import BaseModel, Field

from ..objects import BlockObject
from .base import NotionPaginatedData, StartCursor, PageSize


class AppendBlockChildrenRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/patch-block-children"""

    block_id: str = Field(
        ..., description="Identifier for a block. Also accepts a page ID."
    )
    children: List[BlockObject] = Field(
        ...,
        description="Child content to append to a container block as an array of block objects",
    )
    after: Optional[str] = Field(
        None,
        description="The ID of the existing block that the new block should be appended after.",
    )


AppendBlockChildrenResponse = NotionPaginatedData[BlockObject]
"""Returns a paginated list of newly created first level children block objects. Refer to https://developers.notion.com/reference/patch-block-children"""


class RetrieveBlockRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/retrieve-a-block"""

    block_id: str = Field(..., description="Identifier for a Notion block")


RetrieveBlockResponse = BlockObject
"""Reference: https://developers.notion.com/reference/retrieve-a-block"""


class RetrieveBlockChildrenRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/get-block-children"""

    block_id: str = Field(
        ..., description="Identifier for a Notion block, also accepts a page ID."
    )
    start_cursor: Optional[StartCursor] = None
    page_size: Optional[PageSize] = None


RetrieveBlockChildrenResponse = NotionPaginatedData[BlockObject]
"""Reference: https://developers.notion.com/reference/get-block-children"""

# TODO: UpdateBlockRequest

UpdateBlockResponse = BlockObject
"""Reference: https://developers.notion.com/reference/update-a-block"""


class DeleteBlockRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/delete-a-block"""

    block_id: str = Field(..., description="Identifier for a Notion block")


DeleteBlockResponse = BlockObject
"""Reference: https://developers.notion.com/reference/delete-a-block"""


__all__ = [
    "AppendBlockChildrenRequest",
    "AppendBlockChildrenResponse",
    "RetrieveBlockRequest",
    "RetrieveBlockResponse",
    "RetrieveBlockChildrenRequest",
    "RetrieveBlockChildrenResponse",
    # "UpdateBlockRequest",
    "UpdateBlockResponse",
    "DeleteBlockRequest",
    "DeleteBlockResponse",
]
