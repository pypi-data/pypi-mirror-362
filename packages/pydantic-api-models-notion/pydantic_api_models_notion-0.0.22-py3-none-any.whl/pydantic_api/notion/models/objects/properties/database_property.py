"""
Reference: https://developers.notion.com/reference/property-schema-object
"""

from typing import List, Optional, Literal, Union, Annotated

from uuid import UUID
from pydantic import ConfigDict, Field, model_validator

from pydantic_api.base import BaseModel
from ..common import ColorLiteral
from .common import (
    SelectOption,
    RelationTypeLiteral,
    NumberFormatLiteral,
    RollupFunctionLiteral,
    DatabasePropertyTypeLiteral,
)


class EmptyConfig(BaseModel):
    ...
    model_config = ConfigDict(extra="forbid")


class BaseDatabaseProperty(BaseModel):
    id: Optional[str] = Field(
        None,
        description='An identifier for the property, usually a short string of random letters and symbols. Some automatically generated property types have special human-readable IDs. For example, all Title properties have an id of "title".',
    )
    name: Optional[str] = Field(
        None, description="The name of the property as it appears in Notion."
    )
    description: Optional[str] = Field(
        None, description="The description of the property as it appears in Notion."
    )
    type: DatabasePropertyTypeLiteral

    @classmethod
    def define(cls):
        return cls()


# Specific Database Property Schemas
class ButtonDatabaseProperty(BaseDatabaseProperty):
    type: Literal["button"] = "button"
    button: EmptyConfig = Field(default_factory=EmptyConfig)


class CheckboxDatabaseProperty(BaseDatabaseProperty):
    type: Literal["checkbox"] = "checkbox"
    checkbox: EmptyConfig = Field(default_factory=EmptyConfig)


class CreatedByDatabaseProperty(BaseDatabaseProperty):
    type: Literal["created_by"] = "created_by"
    created_by: EmptyConfig = Field(default_factory=EmptyConfig)


class CreatedTimeDatabaseProperty(BaseDatabaseProperty):
    type: Literal["created_time"] = "created_time"
    created_time: EmptyConfig = Field(default_factory=EmptyConfig)


class DateDatabaseProperty(BaseDatabaseProperty):
    type: Literal["date"] = "date"
    date: EmptyConfig = Field(default_factory=EmptyConfig)


class EmailDatabaseProperty(BaseDatabaseProperty):
    type: Literal["email"] = "email"
    email: EmptyConfig = Field(default_factory=EmptyConfig)


class FilesDatabaseProperty(BaseDatabaseProperty):
    """
    Note: The Notion API does not yet support uploading files to Notion.

    A files database property is rendered in the Notion UI as a column that has values that are either files uploaded directly to Notion or external links to files. The files type object is empty; there is no additional configuration.
    """

    type: Literal["files"] = "files"
    files: EmptyConfig = Field(default_factory=EmptyConfig)


# formula
class FormulaPropertyConfig(BaseModel):
    expression: str = Field(
        ...,
        description="The formula that is used to compute the values for this property. Refer to https://www.notion.so/help/formulas",
    )


class FormulaDatabaseProperty(BaseDatabaseProperty):
    type: Literal["formula"] = "formula"
    formula: FormulaPropertyConfig

    @classmethod
    def define(cls, expression: str):
        return cls(formula=FormulaPropertyConfig(expression=expression))


# last_edited_by
class LastEditedByDatabaseProperty(BaseDatabaseProperty):
    type: Literal["last_edited_by"] = "last_edited_by"
    last_edited_by: EmptyConfig = Field(default_factory=EmptyConfig)


# last_edited_time
class LastEditedTimeDatabaseProperty(BaseDatabaseProperty):
    type: Literal["last_edited_time"] = "last_edited_time"
    last_edited_time: EmptyConfig = Field(default_factory=EmptyConfig)


# multi_select
class MultiSelectPropertyConfig(BaseModel):
    options: List[SelectOption] = Field(default_factory=list)


class MultiSelectDatabaseProperty(BaseDatabaseProperty):
    type: Literal["multi_select"] = "multi_select"
    multi_select: MultiSelectPropertyConfig

    @classmethod
    def define(cls, options: List[SelectOption]):
        return cls(multi_select=MultiSelectPropertyConfig(options=options))


# number
class NumberPropertyConfig(BaseModel):
    format: Optional[NumberFormatLiteral] = Field(None)


class NumberDatabaseProperty(BaseDatabaseProperty):
    type: Literal["number"] = "number"
    number: NumberPropertyConfig = Field(default_factory=NumberPropertyConfig)

    @classmethod
    def define(cls, format: Optional[NumberFormatLiteral] = None):
        return cls(number=NumberPropertyConfig(format=format))


# people
class PeopleDatabaseProperty(BaseDatabaseProperty):
    type: Literal["people"] = "people"
    people: EmptyConfig = Field(default_factory=EmptyConfig)


# phone_number
class PhoneNumberDatabaseProperty(BaseDatabaseProperty):
    type: Literal["phone_number"] = "phone_number"
    phone_number: EmptyConfig = Field(default_factory=EmptyConfig)


# relation
class SinglePropertyData(BaseModel):
    pass


class SinglePropertyRelationData(BaseModel):
    type: Literal["single_property"] = "single_property"
    database_id: UUID = Field(
        ...,
        description="The database that the relation property refers to. The corresponding linked page values must belong to the database in order to be valid.",
    )
    single_property: SinglePropertyData = Field(
        default_factory=SinglePropertyData,
        description="The configuration for a single property relation.",
    )


class SinglePropertyRelationDatabaseProperty(BaseModel):
    type: Literal["relation"] = "relation"
    relation: SinglePropertyRelationData


class DualPropertyData(BaseModel):
    pass


class DualPropertyData(BaseModel):
    type: Literal["dual_property"] = "dual_property"
    database_id: UUID = Field(
        ...,
        description="The database that the relation property refers to. The corresponding linked page values must belong to the database in order to be valid.",
    )
    dual_property: DualPropertyData = Field(
        default_factory=DualPropertyData,
        description="The configuration for a dual property relation.",
    )


class DualPropertyRelationDatabaseProperty(BaseModel):
    type: Literal["relation"] = "relation"
    relation: DualPropertyData


RelationDatabaseProperty = Union[
    SinglePropertyRelationDatabaseProperty, DualPropertyRelationDatabaseProperty
]


# rich_text
class RichTextDatabaseProperty(BaseDatabaseProperty):
    type: Literal["rich_text"] = "rich_text"
    rich_text: EmptyConfig = Field(default_factory=EmptyConfig)


# rollup
class RollupPropertyConfig(BaseModel):
    relation_property_name: Optional[str] = None
    relation_property_id: Optional[str] = None
    rollup_property_name: Optional[str] = None
    rollup_property_id: Optional[str] = None
    function: RollupFunctionLiteral

    @model_validator(mode="after")
    def ensure_either_name_or_id_is_provided(self):
        if self.relation_property_name is None and self.relation_property_id is None:
            raise ValueError(
                "Either relation_property_name or relation_property_id is required."
            )
        if self.rollup_property_name is None and self.rollup_property_id is None:
            raise ValueError(
                "Either rollup_property_name or rollup_property_id is required."
            )
        return self


class RollupDatabaseProperty(BaseDatabaseProperty):
    type: Literal["rollup"] = "rollup"
    rollup: RollupPropertyConfig

    @classmethod
    def define(
        cls,
        function: RollupFunctionLiteral,
        relation_property_name: Optional[str] = None,
        relation_property_id: Optional[str] = None,
        rollup_property_name: Optional[str] = None,
        rollup_property_id: Optional[str] = None,
    ):
        return cls(
            rollup=RollupPropertyConfig(
                function=function,
                relation_property_name=relation_property_name,
                relation_property_id=relation_property_id,
                rollup_property_name=rollup_property_name,
                rollup_property_id=rollup_property_id,
            )
        )


# select
class SelectPropertyConfig(BaseModel):
    options: List[SelectOption] = Field(default_factory=list)


class SelectDatabaseProperty(BaseDatabaseProperty):
    type: Literal["select"] = "select"
    select: SelectPropertyConfig = Field(default_factory=SelectPropertyConfig)

    @classmethod
    def define(cls, options: List[SelectOption]):
        return cls(select=SelectPropertyConfig(options=options))


# status
class StatusOption(BaseModel):
    color: Optional[ColorLiteral] = Field(None)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)


class StatusGroup(BaseModel):
    color: Optional[ColorLiteral] = Field(None)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    option_ids: Optional[List[str]] = Field(
        None,
        description="A sorted list of ids of all of the options that belong to a group.",
    )


class StatusPropertyConfig(BaseModel):
    options: List[StatusOption] = Field(default_factory=list)
    group: Optional[List[StatusGroup]] = Field(default_factory=list)


class StatusDatabaseProperty(BaseDatabaseProperty):
    """
    Note: It is not possible to update a status database property's name or options values via the API.
    """

    type: Literal["status"] = "status"
    status: StatusPropertyConfig


# title
class TitleDatabaseProperty(BaseDatabaseProperty):
    type: Literal["title"] = "title"
    title: EmptyConfig = Field(default_factory=EmptyConfig)


# url
class URLDatabaseProperty(BaseDatabaseProperty):
    type: Literal["url"] = "url"
    url: EmptyConfig = Field(default_factory=EmptyConfig)


# unique id
class UniqueIdPropertyConfig(EmptyConfig):
    """
    The configuration for a unique ID property.
    """

    prefix: str | None = None


class UniqueIdDatabaseProperty(BaseDatabaseProperty):
    type: Literal["unique_id"] = "unique_id"
    unique_id: UniqueIdPropertyConfig

    @classmethod
    def define(cls, prefix: str | None = None):
        return cls(unique_id=UniqueIdPropertyConfig(prefix=prefix))


# Union for all Database Schema Properties
DatabaseProperty = Union[
    ButtonDatabaseProperty,
    CheckboxDatabaseProperty,
    CreatedByDatabaseProperty,
    CreatedTimeDatabaseProperty,
    DateDatabaseProperty,
    EmailDatabaseProperty,
    FilesDatabaseProperty,
    FormulaDatabaseProperty,
    LastEditedByDatabaseProperty,
    LastEditedTimeDatabaseProperty,
    MultiSelectDatabaseProperty,
    NumberDatabaseProperty,
    PeopleDatabaseProperty,
    PhoneNumberDatabaseProperty,
    RelationDatabaseProperty,
    RichTextDatabaseProperty,
    RollupDatabaseProperty,
    SelectDatabaseProperty,
    StatusDatabaseProperty,
    TitleDatabaseProperty,
    URLDatabaseProperty,
    UniqueIdDatabaseProperty,
]


__all__ = [
    "ButtonDatabaseProperty",
    "CheckboxDatabaseProperty",
    "CreatedByDatabaseProperty",
    "CreatedTimeDatabaseProperty",
    "DateDatabaseProperty",
    "EmailDatabaseProperty",
    "FilesDatabaseProperty",
    "FormulaDatabaseProperty",
    "LastEditedByDatabaseProperty",
    "LastEditedTimeDatabaseProperty",
    "MultiSelectDatabaseProperty",
    "NumberDatabaseProperty",
    "PeopleDatabaseProperty",
    "PhoneNumberDatabaseProperty",
    "RelationDatabaseProperty",
    "RichTextDatabaseProperty",
    "RollupDatabaseProperty",
    "SelectDatabaseProperty",
    "StatusDatabaseProperty",
    "TitleDatabaseProperty",
    "URLDatabaseProperty",
    "UniqueIdDatabaseProperty",
    # Union Type
    "DatabaseProperty",
    # Base Type
    "BaseDatabaseProperty",
    # Some config objects
    "SelectPropertyConfig",
    "MultiSelectPropertyConfig",
]
