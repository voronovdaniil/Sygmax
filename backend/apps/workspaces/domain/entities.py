from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Optional


@dataclass
class Workspace:
    id: UUID = field(default_factory=uuid4)
    name: str
    description: Optional[str] = ""
    owner_id: UUID
    is_personal: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class WorkspaceMember:
    class RoleChoices:
        ADMIN = 'admin'
        MEMBER = 'member'
        GUEST = 'guest'

    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    workspace_id: UUID
    role: str = RoleChoices.MEMBER
    joined_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class WorkspaceInvite:
    class StatusChoices:
        PENDING = 'pending'
        ACCEPTED = 'accepted'
        DECLINED = 'declined'

    id: UUID = field(default_factory=uuid4)
    workspace_id: UUID
    email: str
    invited_by_id: UUID
    role: str = WorkspaceMember.RoleChoices.MEMBER
    status: str = StatusChoices.PENDING
    expires_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
