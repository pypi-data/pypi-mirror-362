from typing import Optional

from uuid import UUID
from pydantic import Field

from pydantic_api.base import BaseModel
from .base import NotionPaginatedData, StartCursor, PageSize
from ..objects import UserObject, BotUserObject


class ListAllUsersRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/get-users"""

    start_cursor: Optional[StartCursor] = None
    page_size: Optional[PageSize] = None


ListAllUsersResponse = NotionPaginatedData[UserObject]
"""Reference: https://developers.notion.com/reference/get-users"""


class RetrieveUserRequest(BaseModel):
    user_id: UUID = Field(..., description="Identifier for a Notion user")


RetrieveUserResponse = UserObject
"""Reference: https://developers.notion.com/reference/get-user"""


class RetrieveBotUserRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/get-self"""

    pass


RetrieveBotUserResponse = BotUserObject
"""Reference: https://developers.notion.com/reference/get-self"""


__all__ = [
    "ListAllUsersRequest",
    "ListAllUsersResponse",
    "RetrieveUserRequest",
    "RetrieveUserResponse",
    "RetrieveBotUserRequest",
    "RetrieveBotUserResponse",
]
