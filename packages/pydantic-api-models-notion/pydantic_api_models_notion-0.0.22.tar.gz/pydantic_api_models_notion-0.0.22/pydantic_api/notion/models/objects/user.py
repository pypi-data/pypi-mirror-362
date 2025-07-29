"""
Reference: https://developers.notion.com/reference/user
"""

from typing import Optional, Literal, Union, Annotated
from uuid import UUID
from pydantic import AnyHttpUrl, Field, EmailStr

from pydantic_api.base import BaseModel


UserObjectTypeLiteral = Literal["person", "bot"]


class PartialUser(BaseModel):
    """Partial user object.

    PartialUser is not mentioned in https://developers.notion.com/reference/user, but mentioned in the following pages(maybe include more):

    - https://developers.notion.com/reference/page
    - https://developers.notion.com/reference/database

    PartialUser is usually used as `created_by`, `last_edited_by`, `owner`, etc.
    """

    object: Literal["user"] = "user"
    id: UUID = Field(..., description="Unique identifier for this user.")


class _BaseUserObject(PartialUser):
    """Base class for all User objects."""

    type: Optional[UserObjectTypeLiteral] = Field(
        None, description='Type of the user. Possible values are "person" and "bot".'
    )
    name: Optional[str] = Field(
        None, description="User's name, as displayed in Notion."
    )
    avatar_url: Optional[AnyHttpUrl] = Field(None, description="Chosen avatar image.")


class _PersonData(BaseModel):
    """The `person` field of a `PersonUser` object."""

    email: Optional[EmailStr] = None
    """I set email to Optional because: https://developers.notion.com/reference/page-property-values#last_edited_by and https://developers.notion.com/reference/page-property-values#created_by"""


class PersonUserObject(_BaseUserObject):
    """A person user object."""

    type: Literal["person"] = "person"
    person: _PersonData = Field(default_factory=_PersonData)

    @classmethod
    def new(cls, email: EmailStr):
        """Constructor used when creating a new PersonUser object."""
        return cls(person=_PersonData(email=email))


BotOwnerTypeLiteral = Literal["workspace", "user"]


class _BotWorkspaceOwner(BaseModel):
    """The `owner` field for a workspace-owned bot."""

    type: Literal["workspace"] = "workspace"
    workspace: Literal[True] = True


class _BotUserOwner(BaseModel):
    """The `owner` field for a user-owned bot."""

    type: Literal["user"] = "user"


_BotOwner = Union[_BotWorkspaceOwner, _BotUserOwner]
"""The owner of the bot. Either a `workspace` or a `user`."""


class _BotData(BaseModel):
    """The `bot` field of a `BotUser` object."""

    # owner: _BotOwner
    owner: Optional[_BotOwner] = Field(
        None,
        description="The owner of the bot. Now I set it optional as a workaround, since I found sometimes `bot` might be an empty object in practice, which is not documented in the official API reference.",
    )
    workspace_name: Optional[str] = Field(
        None,
        description='If the owner.type is "workspace", then workspace.name identifies the name of the workspace that owns the bot. If the owner.type is "user", then workspace.name is null.',
    )


class BotUserObject(_BaseUserObject):
    """A bot user object."""

    type: Literal["bot"] = "bot"
    bot: _BotData = Field(
        default_factory=_BotData,
        description="Additional data about the bot, including owner information.",
    )


class DeletedUserObject(PartialUser):
    """A deleted user object."""
    pass


UserObject = Annotated[
    Union[PersonUserObject, BotUserObject], Field(discriminator="type")
]
"""
Union of all User objects: `PersonUser` and `BotUser`.
Reference: https://developers.notion.com/reference/user
"""


class UserObjectFactory:
    @classmethod
    def new_person_user(cls, email: EmailStr):
        """Create a new PersonUser object."""
        return PersonUserObject.new(email)


__all__ = [
    "UserObjectTypeLiteral",
    "PersonUserObject",
    "BotUserObject",
    "UserObject",
    "PartialUser",
    "UserObjectFactory",
]
