from typing import Union, List, Dict, Optional

from uuid import UUID
from pydantic import Field, model_validator

from pydantic_api.base import BaseModel
from .base import NotionPaginatedData, FilterObject, SortObject, StartCursor, PageSize
from ..objects import (
    Page,
    Database,
    RichTextObject,
    PageParentObject,
    DatabaseProperty,
    IconObject,
    CoverObject,
)


class CreateDatabaseRequest(BaseModel):
    """
    Note:(quote from: https://developers.notion.com/reference/property-object#title)

    🚧 All databases require one, and only one, title property.

    The API throws errors if you send a request to Create a database without a title property, or if you attempt to Update a database to add or remove a title property.

    📘 Title database property vs. database title

    A title database property is a type of column in a database.

    A database title defines the title of the database and is found on the database object.

    Every database requires both a database title and a title database property.

    """

    parent: PageParentObject = Field(
        ...,
        description="A page parent",
    )
    title: List[RichTextObject] = Field(
        ...,
        description="Title of database as it appears in Notion. An array of rich text objects.",
    )
    properties: Dict[str, DatabaseProperty] = Field(
        ...,
        description="Property schema of database. The keys are the names of properties as they appear in Notion and the values are property schema objects.",
    )
    icon: Optional[IconObject] = Field(
        None,
        description="The icon of the database. Not listed in the documentation but shown in the official example.",
    )
    cover: Optional[CoverObject] = Field(
        None,
        description="The cover of the database. Not listed in the documentation but shown in the official example.",
    )
    is_inline: bool | None = Field(
        None,
        description="Whether the database is shown as a full-page database or an inline database. If true, the database is shown as an inline database. If false, the database is shown as a full-page database. If omitted, the database is shown as a full-page database.",
    )

    @model_validator(mode="after")
    def validate_properties(self):
        # 1. properties must have one and only one title property
        title_property_count = 0
        for property in self.properties.values():
            if property.type == "title":
                title_property_count += 1
        if title_property_count == 0:
            raise ValueError(f"Database must have at least one title property")
        if title_property_count > 1:
            raise ValueError(
                f"Database must have only one title property, but found: {title_property_count}"
            )
        return self


CreateDatabaseResponse = Database
"""Reference: https://developers.notion.com/reference/create-a-database"""


class QueryDatabaseRequest(BaseModel):
    database_id: UUID = Field(..., description="Identifier for a Notion database.")
    filter: Optional[FilterObject] = Field(
        None,
        description="When supplied, limits which pages are returned based on the filter conditions.",
    )
    sorts: Optional[List[SortObject]] = Field(
        None,
        description="When supplied, orders the results based on the provided sort criteria.",
    )
    start_cursor: Optional[StartCursor] = None
    page_size: Optional[PageSize] = None


QueryDatabaseResponse = NotionPaginatedData[Union[Database, Page]]
"""Reference: https://developers.notion.com/reference/post-database-query"""


class RetrieveDatabaseRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/retrieve-a-database"""

    database_id: UUID = Field(..., description="An identifier for the Notion database.")


RetrieveDatabaseResponse = Database
"""Reference: https://developers.notion.com/reference/retrieve-a-database"""


class UpdateDatabaseRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/update-a-database

    Note: (quote from https://developers.notion.com/reference/update-a-database#Errors)

    > 🚧 The following database properties cannot be updated via the API:
    >
    >   - formula
    >   - select
    >   - status
    >   - Synced content
    >   - A multi_select database property's options values. An option can be removed, but not updated.

    """

    database_id: UUID = Field(
        ...,
        description="An identifier for the Notion database.",
    )
    title: List[RichTextObject] = Field(
        None,
        description="An array of rich text objects that represents the title of the database that is displayed in the Notion UI. If omitted, then the database title remains unchanged.",
    )
    description: List[RichTextObject] = Field(
        None,
        description="An array of rich text objects that represents the description of the database that is displayed in the Notion UI. If omitted, then the database description remains unchanged.",
    )
    properties: Dict[str, DatabaseProperty] = Field(
        None,
        description="The properties of a database to be changed in the request, in the form of a JSON object. If updating an existing property, then the keys are the names or IDs of the properties as they appear in Notion, and the values are property schema objects. If adding a new property, then the key is the name of the new database property and the value is a property schema object.",
    )


UpdateDatabaseResponse = Database
"""Reference: https://developers.notion.com/reference/update-a-database"""


__all__ = [
    "CreateDatabaseRequest",
    "CreateDatabaseResponse",
    "QueryDatabaseRequest",
    "QueryDatabaseResponse",
    "RetrieveDatabaseRequest",
    "RetrieveDatabaseResponse",
    "UpdateDatabaseRequest",
    "UpdateDatabaseResponse",
]
