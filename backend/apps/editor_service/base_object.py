from abc import ABC, abstractmethod
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any


class Status(Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class Role(Enum):
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"


class InviteStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"


class BaseObject(ABC):
    """
    Abstract base class for all entities in system
    """
    def __init__(self, title: str, owner_id: str):
        self.id = str(uuid.uuid4())
        self.title = title
        self.object_type = self.__class__.__name__.lower()
        self.owner_id = owner_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.is_deleted = False
        self.slug = self.generate_slug()
        self.parent: Optional[BaseObject] = None
        self.status = Status.ACTIVE
        
    @abstractmethod
    def generate_slug(self) -> str:
        """Abstract method generating slug"""
        return f"{self.object_type}-{self.title.lower().replace(' ', '-')}-{self.id[:8]}"
    
    @abstractmethod
    def get_absolute_url(self) -> str:
        """Abstract method getting URL"""
        return f"/{self.object_type}/{self.slug}"
    
    @abstractmethod
    def save(self):
        """Abstract method for saving object"""
        pass
    
    def update(self, **kwargs):
        """Update attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
        
    def delete(self):
        """Mark as deleted"""
        self.is_deleted = True
        self.updated_at = datetime.now()
        
    def archive(self, archived_by: str, reason: str = None):
        self.status = Status.ARCHIVED
        self.archived_at = datetime.now()
        self.archived_by = archived_by
        self.archive_reason = reason
        self.updated_at = datetime.now()
        
    def restore(self):
        if self.status == Status.ARCHIVED:
            self.status = Status.ACTIVE
            self.updated_at = datetime.now()
            
    def set_parent(self, parent: 'BaseObject'):
        if not isinstance(parent, BaseObject):
            raise ValueError("Parent must be a BaseObject")
        self.parent = parent
    
    def get_ancestors(self, include_self=False) -> List['BaseObject']:
        ancestors = []
        current = self if include_self else self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors
    
    def get_root(self) -> 'BaseObject':
        current = self
        while current.parent:
            current = current.parent
        return current
    
    def __str__(self):
        return f"{self.title} ({self.object_type}, {self.status.value})"
        
    