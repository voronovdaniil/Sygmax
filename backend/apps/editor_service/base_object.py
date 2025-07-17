from abc import ABC, abstractmethod
import uuid
import datetime

class BaseObject(ABC):
    """
    Abstract base class for all entities in system
    """
    def __init__(self, title: str, owner):
        self.id = uuid.uuid4()
        self.title = title
        self.object_type = self.__class__.__name__.lower()
        self.owner = owner
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.is_deleted = False
        self.slug = self.generate_slug()
        self.parent = None
        
    @abstractmethod
    def generate_slug(self) -> str:
        """Abstract method generating slug"""
        pass
    
    @abstractmethod
    def get_absolute_url(self) -> str:
        """Abstract method getting URL"""
        pass
    
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
    
    def set_parent(self, parent):
        """Set parent object"""
        self.parent = parent
    
    def __str__(self):
        return f"{self.title} ({self.object_type})"
        
    