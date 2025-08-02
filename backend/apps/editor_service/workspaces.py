import uuid
from datetime import datetime, timedelta
from base_object import BaseObject, Status, Role, InviteStatus
from typing import Dict, List, Optional, Any


class Workspace(BaseObject):
    def __init__(self, title: str, owner_id: str):
        super().__init__(title, owner_id)
        self.description: str = ""
        self.members: List['WorkspaceMember'] = []
        self.invites: List['WorkspaceInvite'] = []
        self.settings: Optional['WorkspaceSettings'] = None
        self.tags: List['WorkspaceTag'] = []
        self.history: List['WorkspaceHistory'] = []
        
    def generate_slug(self) -> str:
        return f"ws-{self.title.lower().replace(' ', '-')}-{self.id[:8]}"

    def get_absolute_url(self) -> str:
        return f"/workspaces/{self.slug}"

    def add_member(self, user_id: str, role: Role):
        member = WorkspaceMember(user_id=user_id, workspace=self, role=role)
        self.members.append(member)
        self._add_history(f"Added member {user_id} as {role.value}")
        return member

    def _add_history(self, action: str):
        self.history.append(WorkspaceHistory(workspace=self, user_id=self.owner_id, action=action))
        

class WorkspaceMember:
    def __init__(self, user_id: str, workspace: Workspace, role: Role):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.workspace = workspace
        self.role = role
        self.joined_at = datetime.now()


class WorkspaceInvite:
    def __init__(self, email: str, invited_by_id: str, workspace: Workspace, role: Role, days_valid: int = 7):
        self.id = str(uuid.uuid4())
        self.email = email
        self.invited_by_id = invited_by_id
        self.workspace = workspace
        self.role = role
        self.status = InviteStatus.PENDING
        self.expires_at = datetime.now() + timedelta(days=days_valid)
        self.created_at = datetime.now()

    def accept(self):
        if self.status == InviteStatus.PENDING and datetime.now() < self.expires_at:
            self.status = InviteStatus.ACCEPTED
            self.workspace.add_member(user_id="temp_user_id", role=self.role)  # Здесь должен быть реальный user_id
            return True
        return False

    def decline(self):
        self.status = InviteStatus.DECLINED
        

class WorkspaceSettings:
    def __init__(self, workspace: Workspace):
        self.id = str(uuid.uuid4())
        self.workspace = workspace
        self.is_private = False
        self.enable_notifications = True
        

class WorkspaceTag:
    def __init__(self, workspace: Workspace, tag: str):
        self.id = str(uuid.uuid4())
        self.workspace = workspace
        self.tag = tag
        

class WorkspaceHistory:
    def __init__(self, workspace: Workspace, user_id: str, action: str):
        self.id = str(uuid.uuid4())
        self.workspace = workspace
        self.user_id = user_id
        self.action = action
        self.timestamp = datetime.now()
        

class ArchivedWorkspace:
    def __init__(self, workspace: Workspace, archived_by: str, reason: str = None):
        self.id = str(uuid.uuid4())
        self.workspace_id = workspace.id
        self.archived_by = archived_by
        self.archived_at = datetime.now()
        self.reason = reason