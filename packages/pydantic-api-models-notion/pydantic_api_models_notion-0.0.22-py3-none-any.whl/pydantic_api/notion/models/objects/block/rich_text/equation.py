from typing import Literal

from pydantic_api.base import BaseModel
from .base import BaseRichTextObject


class EquationObject(BaseModel):
    """Equation object type."""

    expression: str


class EquationRichTextObject(BaseRichTextObject):
    """Rich Text type: Equation."""

    type: Literal["equation"] = "equation"
    equation: EquationObject

    @classmethod
    def new(cls, expression: str):
        return cls(equation=EquationObject(expression=expression))


__all__ = [
    "EquationObject",
    "EquationRichTextObject",
]
