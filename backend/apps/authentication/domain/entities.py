from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List


class OAuthProvider(str, Enum):
    GOOGLE = "google"
    GITHUB = "github"
    FACEBOOK = "facebook"


@dataclass
class User:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    email: str
    full_name: str
    email_confirmed: bool = field(default=False)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = None
    login_attempts: int = 0
    is_active: bool = True
    is_staff: bool = False
    groups: List[str] = field(default_factory=list)  # Группы пользователя
    permissions: List[str] = field(default_factory=list)  # Разрешения пользователя


@dataclass
class OAuthAccount:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    provider: OAuthProvider
    provider_id: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class TokenBlacklist:
    token: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime


@dataclass
class UserSecurity:
    user_id: uuid.UUID
    two_factor_enabled: bool = False
    two_factor_secret: Optional[str] = None
