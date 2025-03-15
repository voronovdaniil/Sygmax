from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class WorkspaceRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"


@dataclass
class Workspace:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str
    description: Optional[str] = None
    owner_id: uuid.UUID
    is_personal: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class WorkspaceMember:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    workspace_id: uuid.UUID
    role: WorkspaceRole
    joined_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class WorkspaceInvite:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    workspace_id: uuid.UUID
    email: str
    invited_by_id: uuid.UUID
    role: WorkspaceRole
    status: str = "pending"
    expires_at: datetime
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

