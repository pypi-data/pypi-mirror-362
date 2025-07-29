"""
Reference: https://developers.notion.com/reference/parent-object
"""

from typing import Literal, Union, Annotated

from uuid import UUID
from pydantic import Field

from pydantic_api.base import BaseModel


ParentObjectTypeLiteral = Literal["database_id", "page_id", "workspace", "block_id"]


class DatabaseParentObject(BaseModel):
    """Database as a parent."""

    type: Literal["database_id"] = "database_id"
    database_id: UUID


class PageParentObject(BaseModel):
    """Page as a parent."""

    type: Literal["page_id"] = "page_id"
    page_id: UUID


class WorkspaceParentObject(BaseModel):
    """Workspace as a parent. I.e. a root-level page in the workspace."""

    type: Literal["workspace"] = "workspace"
    workspace: Literal[True] = True


class BlockParentObject(BaseModel):
    """Block as a parent."""

    type: Literal["block_id"] = "block_id"
    block_id: UUID


ParentObject = Annotated[
    Union[
        DatabaseParentObject, PageParentObject, WorkspaceParentObject, BlockParentObject
    ],
    Field(discriminator="type"),
]


# The following classes are util classes which are not mentioned in the Notion API documentation.
class ParentObjectFactory:
    @classmethod
    def new_page_parent(cls, page_id: UUID) -> PageParentObject:
        return PageParentObject(page_id=page_id)

    @classmethod
    def new_database_parent(cls, database_id: UUID) -> DatabaseParentObject:
        return DatabaseParentObject(database_id=database_id)

    @classmethod
    def new_workspace_parent(cls) -> WorkspaceParentObject:
        return WorkspaceParentObject()

    @classmethod
    def new_block_parent(cls, block_id: UUID) -> BlockParentObject:
        return BlockParentObject(block_id=block_id)


__all__ = [
    "ParentObjectTypeLiteral",
    "DatabaseParentObject",
    "PageParentObject",
    "WorkspaceParentObject",
    "BlockParentObject",
    "ParentObject",
    "ParentObjectFactory",
]
