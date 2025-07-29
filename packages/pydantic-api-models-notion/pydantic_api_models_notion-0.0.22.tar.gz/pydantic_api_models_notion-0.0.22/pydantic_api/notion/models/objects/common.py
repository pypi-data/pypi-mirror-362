from pydantic import AnyUrl
from datetime import datetime
from typing import Union, Literal, Optional

from .emoji import EmojiObject
from .file import ExternalFileObject, UploadedFileObject


IconObject = Union[UploadedFileObject, ExternalFileObject, EmojiObject]


class IconObjectFactory:
    @classmethod
    def from_external_file(cls, url: str, name: str | None = None):
        return ExternalFileObject.new(
            url=url,
            name=name,
        )

    @classmethod
    def from_uploaded_file(
        cls,
        url: str,
        expire_time: Optional[datetime] = None,
        name: str | None = None,
    ):
        return UploadedFileObject.new(
            url=url,
            expire_time=expire_time,
            name=name,
        )

    @classmethod
    def from_emoji(cls, emoji: str):
        """Create a new IconObject with emoji.

        Args:
            emoji: The emoji to use.
        """
        return EmojiObject(emoji=emoji)


CoverObject = Union[ExternalFileObject, UploadedFileObject]


class CoverObjectFactory:
    @classmethod
    def from_external_file(cls, url: str):
        return ExternalFileObject.from_url(url=url)

    @classmethod
    def from_uploaded_file(
        cls,
        url: str,
        expire_time: Optional[datetime] = None,
        name: str | None = None,
    ):
        return UploadedFileObject.new(
            url=url,
            expire_time=expire_time,
            name=name,
        )


ColorLiteral = Literal[
    "default",
    "gray",
    "gray_background",
    "brown",
    "brown_background",
    "orange",
    "orange_background",
    "yellow",
    "yellow_background",
    "green",
    "green_background",
    "blue",
    "blue_background",
    "purple",
    "purple_background",
    "pink",
    "pink_background",
    "red",
    "red_background",
]

CodeLanguageLiteral = Literal[
    "abap",
    "arduino",
    "bash",
    "basic",
    "c",
    "clojure",
    "coffeescript",
    "c++",
    "c#",
    "css",
    "dart",
    "diff",
    "docker",
    "elixir",
    "elm",
    "erlang",
    "flow",
    "fortran",
    "f#",
    "gherkin",
    "glsl",
    "go",
    "graphql",
    "groovy",
    "haskell",
    "html",
    "java",
    "javascript",
    "json",
    "julia",
    "kotlin",
    "latex",
    "less",
    "lisp",
    "livescript",
    "lua",
    "makefile",
    "markdown",
    "markup",
    "matlab",
    "mermaid",
    "nix",
    "objective-c",
    "ocaml",
    "pascal",
    "perl",
    "php",
    "plain text",
    "powershell",
    "prolog",
    "protobuf",
    "python",
    "r",
    "reason",
    "ruby",
    "rust",
    "sass",
    "scala",
    "scheme",
    "scss",
    "shell",
    "sql",
    "swift",
    "typescript",
    "vb.net",
    "verilog",
    "vhdl",
    "visual basic",
    "webassembly",
    "xml",
    "yaml",
    "java/c/c++/c#",
]
"""Reference: https://developers.notion.com/reference/block#code"""


__all__ = [
    "IconObject",
    "IconObjectFactory",
    "CoverObject",
    "CoverObjectFactory",
    "ColorLiteral",
    "CodeLanguageLiteral",
]
