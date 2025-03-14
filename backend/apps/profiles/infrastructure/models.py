from django.db import models
import uuid
from django.utils import timezone

# Языки интерфейса
class LanguageChoices(models.TextChoices):
    EN = 'en', 'English'
    RU = 'ru', 'Русский'
    ES = 'es', 'Español'

# Темы интерфейса
class ThemeChoices(models.TextChoices):
    LIGHT = 'light', 'Light Theme'
    DARK = 'dark', 'Dark Theme'
    SYSTEM = 'system', 'System Default'

# Профиль пользователя
class UserProfile(models.Model):
    user_id = models.UUIDField(unique=True)
    storage_path = models.CharField(max_length=255, blank=True, verbose_name='Путь к папке пользователя в S3')
    full_name = models.CharField(max_length=150, blank=True, verbose_name='Полное имя')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', blank=True, null=True)
    bio = models.TextField(blank=True, max_length=500, verbose_name='Биография')
    language = models.CharField(max_length=2, choices=LanguageChoices.choices, default=LanguageChoices.EN)
    user_timezone = models.CharField(max_length=50, verbose_name='Часовой пояс')
    theme = models.CharField(max_length=10, choices=ThemeChoices.choices, default=ThemeChoices.LIGHT)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

# Роли пользователей
class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Привязка пользователей к ролям
class UserRole(models.Model):
    user_id = models.UUIDField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'role')

