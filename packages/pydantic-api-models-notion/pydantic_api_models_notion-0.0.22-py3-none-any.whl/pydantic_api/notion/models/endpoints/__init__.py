"""

Module: `pydantic_api.notion.models.endpoints`

Contains all data classes defined in the Notion API documentation, the *ENDPOINTS* section.

I.e. all Request and Response data models for the Notion API endpoints.

- Authentication: `pydantic_api.notion.models.endpoints.authentication`  (Not implemented)
- Blocks: `pydantic_api.notion.models.endpoints.blocks`  (Not implemented)
- Pages: `pydantic_api.notion.models.endpoints.pages`
- Databases: `pydantic_api.notion.models.endpoints.databases`
- Users: `pydantic_api.notion.models.endpoints.users`
- Comments: `pydantic_api.notion.models.endpoints.comments`
- Search: `pydantic_api.notion.models.endpoints.search`

"""

from .base import (
    PageSize,
    StartCursor,
    SortObject,
    SortObjectFactory,
    NotionPaginatedData,
    NotionPaginatedDataTypeLiteral,
    CheckboxFilterObject,
    DateFilterObject,
    FilesFilterObject,
    FormulaFilterObject,
    MultiSelectFilterObject,
    NumberFilterObject,
    PeopleFilterObject,
    RelationFilterObject,
    RichTextFilterObject,
    RollupFilterObject,
    SelectFilterObject,
    StatusFilterObject,
    TimestampFilterObject,
    UniqueIDFilterObject,
    FilterObject,
)
from .pages import (
    CreatePageRequest,
    CreatePageResponse,
    RetrievePageRequest,
    RetrievePageResponse,
    RetrievePagePropertyItemRequest,
    RetrievePagePropertyItemResponse,
    UpdatePagePropertiesRequest,
    UpdatePagePropertiesResponse,
)
from .users import (
    ListAllUsersRequest,
    ListAllUsersResponse,
    RetrieveUserRequest,
    RetrieveUserResponse,
    RetrieveBotUserRequest,
    RetrieveBotUserResponse,
)
from .blocks import (
    AppendBlockChildrenRequest,
    AppendBlockChildrenResponse,
    RetrieveBlockRequest,
    RetrieveBlockResponse,
    RetrieveBlockChildrenRequest,
    RetrieveBlockChildrenResponse,
    # UpdateBlockRequest,
    UpdateBlockResponse,
    DeleteBlockRequest,
    DeleteBlockResponse,
)
from .databases import (
    CreateDatabaseRequest,
    CreateDatabaseResponse,
    QueryDatabaseRequest,
    QueryDatabaseResponse,
    RetrieveDatabaseRequest,
    RetrieveDatabaseResponse,
    UpdateDatabaseRequest,
    UpdateDatabaseResponse,
)
from .comments import (
    CreateCommentRequest,
    CreateCommentResponse,
    RetrieveCommentsRequest,
    RetrieveCommentsResponse,
)
from .search import (
    SearchByTitleRequest,
    SearchByTitleResponse,
    SearchByTitleFilterObject,
)


__all__ = [
    # base
    "PageSize",
    "StartCursor",
    "NotionPaginatedDataTypeLiteral",
    "NotionPaginatedData",
    "SortObject",
    "SortObjectFactory",
    "CheckboxFilterObject",
    "DateFilterObject",
    "FilesFilterObject",
    "FormulaFilterObject",
    "MultiSelectFilterObject",
    "NumberFilterObject",
    "PeopleFilterObject",
    "RelationFilterObject",
    "RichTextFilterObject",
    "RollupFilterObject",
    "SelectFilterObject",
    "StatusFilterObject",
    "TimestampFilterObject",
    "UniqueIDFilterObject",
    "FilterObject",
    # pages
    "CreatePageRequest",
    "CreatePageResponse",
    "RetrievePageRequest",
    "RetrievePageResponse",
    "RetrievePagePropertyItemRequest",
    "RetrievePagePropertyItemResponse",
    "UpdatePagePropertiesRequest",
    "UpdatePagePropertiesResponse",
    # users
    "ListAllUsersRequest",
    "ListAllUsersResponse",
    "RetrieveUserRequest",
    "RetrieveUserResponse",
    "RetrieveBotUserRequest",
    "RetrieveBotUserResponse",
    # blocks
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
    # databases
    "CreateDatabaseRequest",
    "CreateDatabaseResponse",
    "QueryDatabaseRequest",
    "QueryDatabaseResponse",
    "RetrieveDatabaseRequest",
    "RetrieveDatabaseResponse",
    "UpdateDatabaseRequest",
    "UpdateDatabaseResponse",
    # comments
    "CreateCommentRequest",
    "CreateCommentResponse",
    "RetrieveCommentsRequest",
    "RetrieveCommentsResponse",
    # search
    "SearchByTitleFilterObject",
    "SearchByTitleRequest",
    "SearchByTitleResponse",
]
