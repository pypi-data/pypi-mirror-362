from __future__ import annotations
from typing import Generic, TypeVar, Literal, Optional, Annotated, Union, List, Any

from uuid import UUID
from pydantic import AnyHttpUrl, Field, model_validator

from pydantic_api.base import BaseModel

TResult = TypeVar("TResult")


NotionPaginatedDataTypeLiteral = Literal[
    "block",
    "comment",
    "database",
    "page",
    "page_or_database",
    "property_item",
    "user",
]
"""Reference: https://developers.notion.com/reference/intro#pagination"""


class NotionPaginatedData(BaseModel, Generic[TResult]):
    """
    Reference:

    - https://developers.notion.com/reference/intro#pagination
    - https://developers.notion.com/reference/page-property-values#paginated-page-properties
    """

    object: Literal["list"] = "list"
    results: list[TResult]
    next_cursor: Optional[str] = None
    has_more: bool
    type: NotionPaginatedDataTypeLiteral
    request_id: UUID
    next_url: Optional[AnyHttpUrl] = Field(
        None,
        description="The URL the user can request to get the next page of results.",
        examples=[
            "http://api.notion.com/v1/pages/0e5235bf86aa4efb93aa772cce7eab71/properties/vYdV?start_cursor=LYxaUO&page_size=25"
        ],
    )


StartCursor = Annotated[
    str,
    Field(
        description="If supplied, this endpoint will return a page of results starting after the cursor provided. If not supplied, this endpoint will return the first page of results.",
    ),
]

PageSize = Annotated[
    int,
    Field(
        gt=0,
        le=100,
        description="The number of results to return. The default page size is 100, and the maximum is 100.",
    ),
]


# Sort Object.
# Reference:
# - https://developers.notion.com/reference/post-search
# - https://developers.notion.com/reference/post-database-query-sort
SortDirectionLiteral = Literal["ascending", "descending"]

SortAllowedTimestampLiteral = Literal["last_edited_time", "created_time"]


class BaseSortObject(BaseModel):
    direction: SortDirectionLiteral = Field(
        ...,
        description='The direction to sort. Possible values include "ascending" and "descending".',
    )


class PropertyValueSortObject(BaseSortObject):
    property: str = Field(
        ...,
        description="The name of the property to sort against.",
        examples=["Ingredients"],
    )


class EntryTimestampSortObject(BaseSortObject):
    timestamp: SortAllowedTimestampLiteral = Field(
        ...,
        description='The name of the timestamp to sort against. Possible values include "created_time" and "last_edited_time".',
    )


SortObject = Union[PropertyValueSortObject, EntryTimestampSortObject]


class SortObjectFactory:
    @classmethod
    def new_timestamp_sort(
        cls,
        timestamp: SortAllowedTimestampLiteral,
        direction: SortDirectionLiteral = "ascending",
    ):
        return EntryTimestampSortObject(timestamp=timestamp, direction=direction)

    @classmethod
    def new_property_sort(
        cls,
        property: str,
        direction: SortDirectionLiteral = "ascending",
    ):
        return PropertyValueSortObject(property=property, direction=direction)


# Filter Object
class BaseFilterObject(BaseModel):
    property: str = Field(
        ...,
        description="The name of the property as it appears in the database, or the property ID.",
    )


# Checkbox Filter Object: Refer to https://developers.notion.com/reference/post-database-query-filter#checkbox
class CheckboxFilterObject(BaseFilterObject):
    checkbox: dict[Literal["equals", "does_not_equal"], bool] = Field(
        ..., description="Filters for checkbox values based on equality."
    )

    @model_validator(mode="after")
    def ensure_exact_one_operand(self):
        if not len(self.checkbox) == 1:
            raise ValueError(
                f"Filter Object can only have exactly 1 operand for a property"
            )
        return self


# Date Filter Object: Refer to https://developers.notion.com/reference/post-database-query-filter#date
class DateFilterObject(BaseFilterObject):
    # TODO: clarify the `Any` here
    date: dict[
        Literal[
            "after",
            "before",
            "equals",
            "is_empty",
            "is_not_empty",
            "next_month",
            "next_week",
            "next_year",
            "on_or_after",
            "on_or_before",
            "past_month",
            "past_week",
            "past_year",
            "this_week",
        ],
        Union[str, Any],
    ]

    @model_validator(mode="after")
    def ensure_exact_one_operand(self):
        if not len(self.date) == 1:
            raise ValueError(
                f"Filter Object can only have exactly 1 operand for a property"
            )
        return self


# Files Filter Object
class FilesFilterObject(BaseFilterObject):
    files: dict[Literal["is_empty", "is_not_empty"], bool]

    @model_validator(mode="after")
    def ensure_exact_one_operand(self):
        if not len(self.files) == 1:
            raise ValueError(
                f"Filter Object can only have exactly 1 operand for a property"
            )
        return self


# Formula Filter Object
class FormulaFilterObject(BaseFilterObject):
    formula: Union[
        CheckboxFilterObject, DateFilterObject, NumberFilterObject, RichTextFilterObject
    ]

    @model_validator(mode="after")
    def ensure_exact_one_operand(self):
        if not len(self.formula) == 1:
            raise ValueError(
                f"Filter Object can only have exactly 1 operand for a property"
            )
        return self


# Multi-select Filter Object
class MultiSelectFilterObject(BaseFilterObject):
    # TODO: clarify the `Any` here
    multi_select: dict[
        Literal["contains", "does_not_contain", "is_empty", "is_not_empty"],
        Any,
    ]

    @model_validator(mode="after")
    def ensure_exact_one_operand(self):
        if not len(self.multi_select) == 1:
            raise ValueError(
                f"Filter Object can only have exactly 1 operand for a property"
            )
        return self


# Number Filter Object
class NumberFilterObject(BaseFilterObject):
    # TODO: clarify the `Any` here
    number: dict[
        Literal[
            "equals",
            "does_not_equal",
            "greater_than",
            "greater_than_or_equal_to",
            "less_than",
            "less_than_or_equal_to",
            "is_empty",
            "is_not_empty",
        ],
        Union[bool, float],
    ]

    @model_validator(mode="after")
    def ensure_exact_one_operand(self):
        if not len(self.number) == 1:
            raise ValueError(
                f"Filter Object can only have exactly 1 operand for a property"
            )
        return self


# People Filter Object
class PeopleFilterObject(BaseFilterObject):
    people: dict[
        Literal["contains", "does_not_contain", "is_empty", "is_not_empty"],
        Union[str, bool],
    ]

    @model_validator(mode="after")
    def ensure_exact_one_operand(self):
        if not len(self.people) == 1:
            raise ValueError(
                f"Filter Object can only have exactly 1 operand for a property"
            )
        return self


# Relation Filter Object
class RelationFilterObject(BaseFilterObject):
    relation: dict[
        Literal["contains", "does_not_contain", "is_empty", "is_not_empty"],
        Union[str, bool],
    ]

    @model_validator(mode="after")
    def ensure_exact_one_operand(self):
        if not len(self.relation) == 1:
            raise ValueError(
                f"Filter Object can only have exactly 1 operand for a property"
            )
        return self


# Rich Text Filter Object
class RichTextFilterObject(BaseFilterObject):
    rich_text: dict[
        Literal[
            "equals",
            "does_not_equal",
            "contains",
            "does_not_contain",
            "starts_with",
            "ends_with",
            "is_empty",
            "is_not_empty",
        ],
        Union[str, bool],
    ]

    @model_validator(mode="after")
    def ensure_exact_one_operand(self):
        if not len(self.rich_text) == 1:
            raise ValueError(
                f"Filter Object can only have exactly 1 operand for a property"
            )
        return self


# Rollup Filter Object
class RollupFilterObject(BaseFilterObject):
    # TODO: clarify the `Any` here
    rollup: dict[
        Literal["any", "every", "none"],
        Any,
    ]

    @model_validator(mode="after")
    def ensure_exact_one_operand(self):
        if not len(self.rollup) == 1:
            raise ValueError(
                f"Filter Object can only have exactly 1 operand for a property"
            )
        return self


# Select Filter Object
class SelectFilterObject(BaseFilterObject):
    select: dict[
        Literal["equals", "does_not_equal", "is_empty", "is_not_empty"],
        Union[str, bool],
    ]

    @model_validator(mode="after")
    def ensure_exact_one_operand(self):
        if not len(self.select) == 1:
            raise ValueError(
                f"Filter Object can only have exactly 1 operand for a property"
            )
        return self


# Status Filter Object
class StatusFilterObject(BaseFilterObject):
    status: dict[
        Literal["equals", "does_not_equal", "is_empty", "is_not_empty"],
        Union[str, bool],
    ]

    @model_validator(mode="after")
    def ensure_exact_one_operand(self):
        if not len(self.status) == 1:
            raise ValueError(
                f"Filter Object can only have exactly 1 operand for a property"
            )
        return self


# Timestamp Filter Object
class BaseTimestampFilterObject(BaseModel):
    timestamp: Literal["created_time", "last_edited_time"]


class CreatedTimeTimestampFilterObject(BaseTimestampFilterObject):
    timestamp: Literal["created_time"] = "created_time"
    created_time: DateFilterObject

    @model_validator(mode="after")
    def ensure_exact_one_operand(self):
        if not len(self.created_time) == 1:
            raise ValueError(
                f"Filter Object can only have exactly 1 operand for a property"
            )
        return self


class LastEditedTimeTimestampFilterObject(BaseTimestampFilterObject):
    timestamp: Literal["last_edited_time"] = "last_edited_time"
    last_edited_time: DateFilterObject

    @model_validator(mode="after")
    def ensure_exact_one_operand(self):
        if not len(self.last_edited_time) == 1:
            raise ValueError(
                f"Filter Object can only have exactly 1 operand for a property"
            )
        return self


TimestampFilterObject = Annotated[
    Union[CreatedTimeTimestampFilterObject, LastEditedTimeTimestampFilterObject],
    Field(discriminator="timestamp"),
]


# Unique ID Filter Object
class UniqueIDFilterObject(BaseFilterObject):
    unique_id: dict[
        Literal[
            "does_not_equal",
            "equals",
            "greater_than",
            "greater_than_or_equal_to",
            "less_than",
            "less_than_or_equal_to",
        ],
        int,
    ]

    @model_validator(mode="after")
    def ensure_exact_one_operand(self):
        if not len(self.unique_id) == 1:
            raise ValueError(
                f"Filter Object can only have exactly 1 operand for a property"
            )
        return self


FilterObject = Union[
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
]


__all__ = [
    # Pagination Related
    "NotionPaginatedDataTypeLiteral",
    "NotionPaginatedData",
    "StartCursor",
    "PageSize",
    # Sort Object
    "SortObject",
    "SortObjectFactory",
    # Filter Object
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
]
