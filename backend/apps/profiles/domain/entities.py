from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class Language(str, Enum):
    EN = "en"
    RU = "ru"
    ES = "es"


class Theme(str, Enum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


@dataclass
class UserProfile:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    storage_path: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    language: Language = field(default=Language.EN)
    user_timezone: str = "UTC"
    theme: Theme = field(default=Theme.LIGHT)
    email_notifications: bool = True
    push_notifications: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Role:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str


@dataclass
class UserRole:
    user_id: uuid.UUID
    role_id: uuid.UUID

