import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from base_object import BaseObject, Status, Role, InviteStatus
from workspaces import Workspace


class Teamspace(BaseObject):
    def __init__(self, title: str, owner_id: str, workspace: 'Workspace'):
        super().__init__(title, owner_id)
        self.description: str = ""
        self.workspace_id = workspace.id
        self.members: List['TeamspaceMember'] = []
        self.invites: List['TeamspaceInvite'] = []
        self.settings: Optional['TeamspaceSettings'] = None
        self.tags: List['TeamspaceTag'] = []
        self.history: List['TeamspaceHistory'] = []
        self.set_parent(workspace)  # Устанавливаем родителя
        
    def generate_slug(self) -> str:
        return f"ws-{self.title.lower().replace(' ', '-')}-{self.id[:8]}"
    
    def get_absolute_url(self) -> str:
        return f"/teamspace/{self.slug}"
        
    def add_member(self, user_id: str, role: Role):
        member = TeamspaceMember(user_id=user_id, teamspace=self, role=role)
        self.members.append(member)
        self._add_history(f"Added member {user_id} as {role.value}")
        return member
    
    def _add_history(self, action: str):
        self.history.append(TeamspaceHistory(teamspace=self, user_id=self.owner_id, action=action))
        

class TeamspaceMember:
    def __init__(self, user_id: str, teamspace: Teamspace, role: Role):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.teamspace = teamspace
        self.role = role
        self.joined_at = datetime.now()
        

class TeamspaceInvite:
    def __init__(self, email: str, invited_by_id: str, teamspace: Teamspace, role: Role, days_valid: int = 7):
        self.id = str(uuid.uuid4())
        self.email = email
        self.invited_by_id = invited_by_id
        self.teamspace = teamspace
        self.role = role
        self.status = InviteStatus.PENDING
        self.expires_at = datetime.now() + timedelta(days=days_valid)
        self.created_at = datetime.now()

    def accept(self):
        if self.status == InviteStatus.PENDING and datetime.now() < self.expires_at:
            self.status = InviteStatus.ACCEPTED
            self.teamspace.add_member(user_id="temp_user_id", role=self.role)
            return True
        return False
    
    def decline(self):
        self.status = InviteStatus.DECLINED
        

class TeamspaceSettings:
    def __init__(self, teamspace: Teamspace):
        self.id = str(uuid.uuid4())
        self.teamspace = teamspace
        self.is_private = False
        self.enable_notifications = True
        

class TeamspaceTag:
    def __init__(self, teamspace: Teamspace, tag: str):
        self.id = str(uuid.uuid4())
        self.teamspace = teamspace
        self.tag = tag
        

class TeamspaceHistory:
    def __init__(self, teamspace: Teamspace, user_id: str, action: str):
        self.id = str(uuid.uuid4())
        self.teamspace = teamspace
        self.user_id = user_id
        self.action = action
        self.timestamp = datetime.now()
        

class ArchivedTeamspace:
    def __init__(self, teamspace: Teamspace, archived_by: str, reason: str = None):
        self.id = str(uuid.uuid4())
        self.teamspace_id = teamspace.id
        self.archived_by = archived_by
        self.archived_at = datetime.now()
        self.reason = reason