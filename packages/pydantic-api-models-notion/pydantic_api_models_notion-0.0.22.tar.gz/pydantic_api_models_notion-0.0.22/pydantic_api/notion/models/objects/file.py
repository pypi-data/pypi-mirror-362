"""
Reference: 

- https://developers.notion.com/reference/file-object
- https://developers.notion.com/reference/page-property-values#files
"""

from datetime import datetime
from typing import Literal, Optional, Annotated, Union

from pydantic import AnyUrl, Field
from pydantic_api.base import BaseModel


FileObjectTypeLiteral = Literal["file", "external"]
"""Reference: https://developers.notion.com/reference/file-object"""


class _FileExternal(BaseModel):
    """The `external` field of a `ExternalFileObject`."""

    url: AnyUrl


class _FileUploaded(BaseModel):
    """The `file` field of a `UploadedFileObject`."""

    url: AnyUrl
    expiry_time: Optional[datetime] = None


class _BaseFileObject(BaseModel):
    type: FileObjectTypeLiteral
    name: Optional[str] = Field(
        None, description="The name of the file to discriminate it."
    )
    """`name` field is not mentioned in https://developers.notion.com/reference/file-object, but mentioned in: https://developers.notion.com/reference/page-property-values#files"""


class ExternalFileObject(_BaseFileObject):
    """A file object corresponding to an external file that has been linked to in Notion"""

    type: Literal["external"] = "external"
    external: _FileExternal

    @classmethod
    def new(cls, url: str, name: str | None = None):
        """
        Args:
            url (str): The URL of the external file.

        Returns:
            ExternalFileObject: An instance of ExternalFileObject.
        """
        return cls(external=_FileExternal(url=AnyUrl(url)), name=name)


class UploadedFileObject(_BaseFileObject):
    """A file object corresponding to a file that has been uploaded to Notion"""

    type: Literal["file"] = "file"
    file: _FileUploaded

    @classmethod
    def new(
        cls,
        url: str,
        expire_time: Optional[datetime] = None,
        name: str | None = None,
    ):
        """
        Args:
            url (str): The URL of the uploaded file.
            expire_time (datetime, optional): The time at which the file will expire. Defaults to None.

        Returns:
            UploadedFileObject: An instance of UploadedFileObject
        """
        return cls(file=_FileUploaded(url=AnyUrl(url), expiry_time=expire_time), name=name)


FileObject = Annotated[
    Union[ExternalFileObject, UploadedFileObject], Field(discriminator="type")
]
"""FileObject. Reference: https://developers.notion.com/reference/file-object"""


class FileObjectFactory:
    @classmethod
    def new_external(cls, url: str, name: str | None = None) -> ExternalFileObject:
        """
        Create a new External File Object

        Args:
            url (str): The URL of the external file.
            name (str, optional): The name of the file to discriminate it. Defaults to None.

        Returns:
            ExternalFileObject: An instance of ExternalFileObject.
        """
        return ExternalFileObject.new(url=url, name=name)

    @classmethod
    def new_uploaded(
        cls,
        url: str,
        expire_time: Optional[datetime] = None,
        name: str | None = None,
    ) -> UploadedFileObject:
        """
        Create a new Uploaded File Object

        Args:
            url (str): The URL of the uploaded file.
            expire_time (datetime, optional): The time at which the file will expire. Defaults to None.
            name (str, optional): The name of the file to discriminate it. Defaults to None.

        Returns:
            UploadedFileObject: An instance of UploadedFileObject
        """
        return UploadedFileObject.new(url=url, expire_time=expire_time, name=name)


__all__ = [
    "FileObjectTypeLiteral",
    "ExternalFileObject",
    "UploadedFileObject",
    "FileObject",
    "FileObjectFactory",
    "_BaseFileObject",
    "_FileExternal",
    "_FileUploaded",
]
