"""
Reference: https://developers.notion.com/reference/property-object
"""

from datetime import datetime
from typing import List, Optional, Literal, Dict, Any

from uuid import UUID
from pydantic import AnyHttpUrl, Field

from pydantic_api.base import BaseModel
from .user import PartialUser
from .block import RichTextObject
from .parent import PageParentObject, BlockParentObject
from .properties import DatabaseProperty
from .common import IconObject, CoverObject


# Database Parent Types
ParentOfDatabase = PageParentObject | BlockParentObject
"""
The type of the parent of a database. It could be a `PageParentObject`, `WorkspaceParent` or `BlockParent`. (Reference: https://developers.notion.com/reference/parent-object)

Note: But for now, the API only support `PageParentObject` as database's parent. (Reference: https://developers.notion.com/reference/create-a-database it says: 'Currently, the parent of a new database must be a Notion page or a wiki database.', note that 'wiki database' is also a page object.)
"""


class Database(BaseModel):
    """Reference: https://developers.notion.com/reference/database"""

    object: Literal["database"] = "database"
    id: UUID
    created_time: datetime
    created_by: PartialUser
    last_edited_time: datetime
    last_edited_by: PartialUser
    title: List[RichTextObject] = Field(default_factory=list)
    description: List[Dict[str, Any]] = Field(default_factory=list)
    icon: Optional[IconObject] = Field(None)
    cover: Optional[CoverObject] = Field(None)
    properties: dict[str, DatabaseProperty]
    parent: ParentOfDatabase
    archived: bool
    url: AnyHttpUrl

    @property
    def plain_text_title(self) -> str:
        return "".join([t.plain_text for t in self.title if t.plain_text])


__all__ = [
    # Database Parent Types
    "ParentOfDatabase",
    # Database
    "Database",
]
