from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Optional, List


@dataclass
class User:
    id: UUID = field(default_factory=uuid4)
    email: str
    full_name: str
    email_confirmed: bool = False
    default_workspace_id: Optional[UUID] = None
    workspace_url: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    login_attempts: int = 0
    is_active: bool = True
    is_staff: bool = False
    roles: List['Role'] = field(default_factory=list)


@dataclass
class Role:
    id: UUID = field(default_factory=uuid4)
    name: str


@dataclass
class UserRole:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    role_id: UUID


@dataclass
class OauthAccount:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    provider: str
    provider_id: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class TokensBlacklist:
    token: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime


@dataclass
class UserSecurity:
    user_id: UUID
    two_factor_enabled: bool = False
    two_factor_secret: Optional[str] = None
