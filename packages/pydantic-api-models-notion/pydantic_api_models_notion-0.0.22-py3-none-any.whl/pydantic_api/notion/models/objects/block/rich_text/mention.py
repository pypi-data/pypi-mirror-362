from datetime import datetime
from typing import Literal, Union, Annotated, Optional

from uuid import UUID
from pydantic import AnyUrl, Field

from pydantic_api.base import BaseModel
from .base import BaseRichTextObject

MentionTypeLiteral = Literal[
    "database",
    "date",
    "link_preview",
    "page",
    "template_mention",
    "user",
]


class _BaseMentionObject(BaseModel):
    """Base model for Mention Object."""

    type: MentionTypeLiteral


# 1. Database mention
class DatabaseMentionBody(BaseModel):
    id: UUID = Field(..., description=f"The id of the mentioned database")


class DatabaseMentionObject(_BaseMentionObject):
    """Mention type: Database."""

    type: Literal["database"] = "database"
    database: DatabaseMentionBody


# 2. Date mention
class DateMentionBody(BaseModel):
    start: datetime
    end: Optional[datetime] = None
    time_zone: Optional[str] = Field(
        None,
        description="An enum value from IANA database based on Moment.js",
    )


class DateMentionObject(_BaseMentionObject):
    """Mention type: Date."""

    type: Literal["date"] = "date"
    date: DateMentionBody


# 3. LinkPreview mention
class LinkPreviewMentionBody(BaseModel):
    url: AnyUrl


class LinkPreviewMentionObject(_BaseMentionObject):
    """Mention type: Link Preview."""

    type: Literal["link_preview"] = "link_preview"
    link_preview: LinkPreviewMentionBody


# 4. Page mention
class PageMentionBody(BaseModel):
    id: UUID = Field(..., description=f"The id of the mentioned page")


class PageMentionObject(_BaseMentionObject):
    """Mention type: Page."""

    type: Literal["page"] = "page"
    page: PageMentionBody


# 5. Tempalte mention
TemplateMentionTypeLiteral = Literal["template_mention_date", "template_mention_user"]


TemplateMentionDateValueLiteral = Literal["today", "now"]


TemplateMentionUserValueLiteral = Literal["me"]


class _BaseTemplateMentionBody(BaseModel):
    type: TemplateMentionTypeLiteral


class _TemplateMentionDate(_BaseTemplateMentionBody):
    type: Literal["template_mention_date"] = "template_mention_date"

    template_mention_date: TemplateMentionDateValueLiteral


class _TemplateMentionUser(_BaseTemplateMentionBody):
    type: Literal["template_mention_user"] = "template_mention_user"

    template_mention_user: TemplateMentionUserValueLiteral


TemplateMentionBody = Annotated[
    Union[_TemplateMentionDate, _TemplateMentionUser], Field(discriminator="type")
]


class TemplateMentionObject(_BaseMentionObject):
    """Mention type: Template Mention."""

    type: Literal["template_mention"] = "template_mention"
    template_mention: TemplateMentionBody


# 6. User mention
class UserMentionBody(BaseModel):
    object: Literal["user"] = "user"
    id: UUID = Field(..., description="The id of the mentioned user")


class UserMentionObject(_BaseMentionObject):
    """Mention type: User."""

    type: Literal["user"] = "user"
    user: UserMentionBody


MentionObject = Annotated[
    Union[
        DatabaseMentionObject,
        DateMentionObject,
        LinkPreviewMentionObject,
        PageMentionObject,
        TemplateMentionObject,
        UserMentionObject,
    ],
    Field(discriminator="type"),
]


class MentionRichTextObject(BaseRichTextObject):
    """Rich Text type: Mention."""

    type: Literal["mention"] = "mention"
    mention: MentionObject


__all__ = [
    "MentionTypeLiteral",
    "DatabaseMentionBody",
    "DatabaseMentionObject",
    "DateMentionBody",
    "DateMentionObject",
    "LinkPreviewMentionBody",
    "LinkPreviewMentionObject",
    "PageMentionBody",
    "PageMentionObject",
    "TemplateMentionBody",
    "TemplateMentionObject",
    "TemplateMentionTypeLiteral",
    "TemplateMentionDateValueLiteral",
    "TemplateMentionUserValueLiteral",
    "UserMentionBody",
    "UserMentionObject",
    "MentionObject",
    "MentionRichTextObject",
]
