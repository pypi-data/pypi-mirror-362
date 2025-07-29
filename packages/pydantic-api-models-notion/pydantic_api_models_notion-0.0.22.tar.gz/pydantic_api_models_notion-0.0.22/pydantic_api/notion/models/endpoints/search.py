from typing import Union, Optional, Literal

from pydantic import Field

from pydantic_api.base import BaseModel
from .base import NotionPaginatedData, StartCursor, PageSize, SortObject
from ..objects import Page, Database


class SearchByTitleFilterObject(BaseModel):
    property: Literal["object"] = "object"
    value: Literal["page", "database"]


class SearchByTitleRequest(BaseModel):
    query: str = Field(
        ...,
        description="The text that the API compares page and database titles against.",
    )
    sort: Optional[SortObject] = Field(
        None,
        description='A set of criteria, direction and timestamp keys, that orders the results. The only supported timestamp value is "last_edited_time". Supported direction values are "ascending" and "descending". If sort is not provided, then the most recently edited results are returned first.',
    )
    filter: Optional[SearchByTitleFilterObject] = Field(
        None,
        description='A set of criteria, value and property keys, that limits the results to either only pages or only databases. Possible value values are "page" or "database". The only supported property value is "object".',
    )
    start_cursor: Optional[StartCursor] = None
    page_size: Optional[PageSize] = None


SearchByTitleResponse = Union[
    NotionPaginatedData[Union[Page, Database]],
    NotionPaginatedData[Page],
    NotionPaginatedData[Database],
]
"""Reference: https://developers.notion.com/reference/post-search"""


__all__ = [
    "SearchByTitleFilterObject",
    "SearchByTitleRequest",
    "SearchByTitleResponse",
]
