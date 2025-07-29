from typing import Union, Dict, List, Any, Optional

from uuid import UUID
from pydantic import BaseModel, Field

from .base import NotionPaginatedData, StartCursor, PageSize
from ..objects import (
    PageParentObject,
    DatabaseParentObject,
    IconObject,
    CoverObject,
    Page,
    PageProperty,
    CheckboxProperty,
    CreatedByProperty,
    CreatedTimeProperty,
    DateProperty,
    EmailProperty,
    FilesProperty,
    LastEditedByProperty,
    LastEditedTimeProperty,
    MultiSelectProperty,
    NumberProperty,
    PhoneNumberProperty,
    SelectProperty,
    StatusProperty,
    URLProperty,
    TitleProperty,
    RichTextProperty,
    PeopleProperty,
    RelationProperty,
    RollupProperty,
    UniqueIDProperty,
    FormulaProperty,
    VerificationProperty,
)


class CreatePageRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/post-page"""

    parent: Union[PageParentObject, DatabaseParentObject] = Field(
        ...,
        description="The parent page or database where the new page is inserted, represented as a JSON object with a page_id or database_id key, and the corresponding ID.",
    )
    properties: Dict[str, PageProperty] = Field(
        ...,
        description="The values of the page’s properties. If the parent is a database, then the schema must match the parent database's properties. If the parent is a page, then the only valid object key is title.",
    )
    # FIXME: implement block types
    children: List[Any] = Field(
        default_factory=list,
        description="The content to be rendered on the new page, represented as an array of block objects.",
    )
    icon: Optional[IconObject] = Field(
        None,
        description="The icon of the new page. Either an emoji object or an external file object.",
    )
    cover: Optional[CoverObject] = Field(
        None,
        description="The cover image of the new page, represented as a file object.",
    )


CreatePageResponse = Page
"""Reference: https://developers.notion.com/reference/post-page"""


class RetrievePageRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/retrieve-a-page"""

    page_id: UUID = Field(
        ...,
        description="Identifier for a Notion page, a uuidv4 string. Reference: https://developers.notion.com/reference/page#keys",
    )
    filter_properties: Optional[List[str]] = Field(
        None,
        description="A list of page property value IDs associated with the page. Use this param to limit the response to a specific page property value or values. To retrieve multiple properties, specify each page property ID. For example: ?filter_properties=iAk8&filter_properties=b7dh.",
        examples=["iAk8", "b7dh"],
    )


RetrievePageResponse = Page
"""Reference: https://developers.notion.com/reference/retrieve-a-page"""

SimplePageProperty = Union[
    CheckboxProperty,
    CreatedByProperty,
    CreatedTimeProperty,
    DateProperty,
    EmailProperty,
    FilesProperty,
    LastEditedByProperty,
    LastEditedTimeProperty,
    MultiSelectProperty,
    NumberProperty,
    PhoneNumberProperty,
    SelectProperty,
    StatusProperty,
    URLProperty,
    RollupProperty,
    UniqueIDProperty,
    FormulaProperty,
    VerificationProperty,
]
"""Reference: https://developers.notion.com/reference/retrieve-a-page-property#simple-properties"""

PaginatedPageProperty = Union[
    TitleProperty,
    RichTextProperty,
    PeopleProperty,
    RelationProperty,
]
"""Reference: https://developers.notion.com/reference/retrieve-a-page-property#paginated-properties"""


class RetrievePagePropertyItemRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/retrieve-a-page-property"""

    page_id: UUID = Field(
        ...,
        description="Identifier for a Notion page",
    )
    property_id: str = Field(
        ...,
        description="Identifier for a page property.",
    )
    start_cursor: Optional[StartCursor] = None
    page_size: Optional[PageSize] = None


RetrievePagePropertyItemResponse = Union[
    SimplePageProperty, NotionPaginatedData[PaginatedPageProperty]
]
"""Reference: https://developers.notion.com/reference/retrieve-a-page-property"""


class UpdatePagePropertiesRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/patch-page"""

    page_id: UUID = Field(
        ...,
        description="The identifier for the Notion page to be updated.",
    )
    properties: Optional[Dict[str, PageProperty]] = Field(
        None,
        description="The property values to update for the page. The keys are the names or IDs of the property and the values are property values. If a page property ID is not included, then it is not changed.",
    )
    archived: Optional[bool] = Field(
        None,
        description="If true, the page is archived. If false, the page is unarchived.",
    )
    icon: Optional[IconObject] = Field(
        None,
        description="A page icon for the page. Supported types are external file object or emoji object.",
    )
    cover: Optional[CoverObject] = Field(
        None,
        description="A cover image for the page. Supported types are external file object.",
    )


UpdatePagePropertiesResponse = Page
"""Reference: https://developers.notion.com/reference/patch-page"""


__all__ = [
    "CreatePageRequest",
    "CreatePageResponse",
    "RetrievePageRequest",
    "RetrievePageResponse",
    "RetrievePagePropertyItemRequest",
    "RetrievePagePropertyItemResponse",
    "UpdatePagePropertiesRequest",
    "UpdatePagePropertiesResponse",
]
