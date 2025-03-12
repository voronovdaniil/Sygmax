from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Optional


@dataclass(frozen=True)
class LanguageChoices:
    EN: str = "en"
    RU: str = "ru"
    ES: str = "es"


@dataclass(frozen=True)
class ThemeChoices:
    LIGHT: str = "light"
    DARK: str = "dark"
    SYSTEM: str = "system"


@dataclass
class UserProfile:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    storage_path: Optional[str] = ""
    full_name: Optional[str] = ""
    avatar_path: Optional[str] = None  # Путь к файлу в S3
    bio: Optional[str] = ""
    language: str = LanguageChoices.EN
    timezone: str = "UTC"
    theme: str = ThemeChoices.LIGHT
    email_notifications: bool = True
    push_notifications: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def avatar_url(self) -> Optional[str]:
        """Возвращает URL для аватара, если он загружен"""
        return f"{self.storage_path}/{self.avatar_path}" if self.avatar_path else None
