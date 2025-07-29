from typing import Literal, Optional

from pydantic import Field, model_validator

from pydantic_api.base import BaseModel
from ..common import ColorLiteral


class SelectOption(BaseModel):
    """
    Selection Option Object.

    Reference:

    - https://developers.notion.com/reference/property-schema#select
    - https://developers.notion.com/reference/page-property-values#select
    """

    color: Optional[ColorLiteral] = Field(None)
    id: Optional[str] = None
    name: Optional[str] = None

    @model_validator(mode="after")
    def either_id_or_name_is_provided(self):
        if self.id is None and self.name is None:
            raise ValueError(f"Either id or name must be provided")
        return self

    @classmethod
    def new(cls, name: str, color: ColorLiteral | None = None):
        """Constructor used when creating a new SelectOption object."""
        return cls(name=name, color=color)

    @classmethod
    def refer(cls, name: str):
        """Constructor used when referring to an existing SelectOption object."""
        return cls(name=name)


class StatusOption(BaseModel):
    color: Optional[ColorLiteral] = Field(None)
    id: Optional[str] = None
    name: Optional[str] = None

    @model_validator(mode="after")
    def either_id_or_name_should_be_provided(self):
        if self.id is None and self.name is None:
            raise ValueError(f"Either name or id must be provided")
        return self

    @classmethod
    def new(cls, name: str, color: ColorLiteral | None = None):
        """Constructor used when creating a new StatusObject."""
        return cls(name=name, color=color)

    @classmethod
    def refer(cls, name: str):
        """Constructor used when referring to an existing StatusObject."""
        return cls(name=name)


DatabasePropertyTypeLiteral = Literal[
    "button",
    "checkbox",
    "created_by",
    "created_time",
    "date",
    "email",
    "files",
    "formula",
    "last_edited_by",
    "last_edited_time",
    "multi_select",
    "number",
    "people",
    "phone_number",
    "relation",
    "rich_text",
    "rollup",
    "select",
    "status",
    "title",
    "url",
    "unique_id",
]
"""
Database Property Type Enum(typed as Literal in this implementation).

Reference: https://developers.notion.com/reference/property-object
"""

PagePropertyTypeLiteral = Literal[
    "button",
    "checkbox",
    "created_by",
    "created_time",
    "date",
    "email",
    "files",
    "formula",
    "last_edited_by",
    "last_edited_time",
    "multi_select",
    "number",
    "people",
    "phone_number",
    "relation",
    "rich_text",
    "rollup",
    "select",
    "status",
    "title",
    "url",
    "unique_id",
    "verification",
]
"""
Page Property Type Enum(typed as Literal in this implementation).

Reference: https://developers.notion.com/reference/page-property-values
"""


FormulaValueTypeLiteral = Literal["boolean", "date", "number", "string"]
"""Reference: https://developers.notion.com/reference/page-property-values#formula"""

RelationTypeLiteral = Literal["single_property", "dual_property"]
"""Reference: https://developers.notion.com/reference/page-property-values#relation"""

RollupFunctionLiteral = Literal[
    "count_all",
    "count_values",
    "count_unique_values",
    "count_empty",
    "count_not_empty",
    "percent_empty",
    "percent_not_empty",
    "sum",
    "average",
    "median",
    "min",
    "max",
    "range",
    "show_original",
]
"""Reference: https://developers.notion.com/reference/page-property-values#rollup"""

RollupTypeLiteral = Literal["array", "date", "incomplete", "number", "unsupported"]
"""Reference: https://developers.notion.com/reference/page-property-values#rollup"""

NumberFormatLiteral = Literal[
    "number",
    "number_with_commas",
    "percent",
    "dollar",
    "canadian_dollar",
    "euro",
    "pound",
    "yen",
    "ruble",
    "rupee",
    "won",
    "yuan",
    "real",
    "lira",
    "rupiah",
    "franc",
    "hong_kong_dollar",
    "new_zealand_dollar",
    "krona",
    "norwegian_krone",
    "mexican_peso",
    "rand",
    "new_taiwan_dollar",
    "danish_krone",
    "zloty",
    "baht",
    "forint",
    "koruna",
    "shekel",
    "chilean_peso",
    "philippine_peso",
    "dirham",
    "colombian_peso",
    "riyal",
    "ringgit",
    "leu",
    "argentine_peso",
    "uruguayan_peso",
    "singapore_dollar",
]
"""Reference: https://developers.notion.com/reference/page-property-values#number"""

VerificationStateLiteral = Literal["verified", "unvirified"]
"""Reference: https://developers.notion.com/reference/page-property-values#verification"""

__all__ = [
    "SelectOption",
    "StatusOption",
    "FormulaValueTypeLiteral",
    "RelationTypeLiteral",
    "RollupFunctionLiteral",
    "RollupTypeLiteral",
    "NumberFormatLiteral",
    "VerificationStateLiteral",
    "PagePropertyTypeLiteral",
    "DatabasePropertyTypeLiteral",
]
