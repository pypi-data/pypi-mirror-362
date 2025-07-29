"""
Module: pydantic_api.notion.models.objects

Contains all data models defined in the Notion API documentation, the *OBJECTS* section.

- Block: `pydantic_api.notion.models.objects.block`
- Page: `pydantic_api.notion.models.objects.page`
- Database: `pydantic_api.notion.models.objects.database`
- Parent: `pydantic_api.notion.models.objects.parent`
- User: `pydantic_api.notion.models.objects.user`
- Comment: `pydantic_api.notion.models.objects.comment`
- Unfurl attribute(Link Previews): `pydantic_api.notion.models.objects.link_preview`
- File: `pydantic_api.notion.models.objects.file`
- Emoji: `pydantic_api.notion.models.objects.emoji`

"""

from .common import *
from .user import *
from .file import *
from .page import *
from .emoji import *
from .block import *
from .parent import *
from .comment import *
from .database import *
from .properties import *
from .link_preview import *
