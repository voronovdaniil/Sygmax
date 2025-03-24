from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class WorkspaceRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"

class InviteStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    EXPIRED = "expired"
    REVOKED = "revoked"

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
class ArchivedWorkspace:

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    workspace_id: uuid.UUID
    archived_by: uuid.UUID
    archived_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    reason: Optional[str] = None

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

@dataclass
class WorkspaceSettings:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    workspace_id: uuid.UUID
    is_private: bool = False
    enable_notifications: bool = True
    
@dataclass
class WorkspaceTag:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    workspace_id: uuid.UUID
    tag: str
    
@dataclass
class WorkspaceHistory:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    workspace_id: uuid.UUID
    user_id: uuid.UUID
    action: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

  

@dataclass
class Teamspace:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    workspace_id: uuid.UUID
    name: str
    description: Optional[str] = None
    status: str
    owner_id: uuid.UUID
    is_personal: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class ArchivedTeamspace:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    teamspace_id: uuid.UUID
    archived_by: uuid.UUID
    archived_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    reason: Optional[str] = None


@dataclass
class TeamspaceMember:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    teamspace_id: uuid.UUID
    role: WorkspaceRole
    joined_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
  

@dataclass
class TeampaceSettings:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    teamspace_id: uuid.UUID
    is_private: bool = False
    enable_notifications: bool = True

@dataclass
class TeamspaceTag:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    teamspace_id: uuid.UUID
    tag: str
  

@dataclass
class TeamspaceInvite:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    teamspace_id: uuid.UUID
    email: str
    invited_by_id: uuid.UUID
    role: WorkspaceRole
    status: str = "pending"
    expires_at: datetime
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class TeamspaceHistory:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    teamspace_id: uuid.UUID
    user_id: uuid.UUID
    action: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
