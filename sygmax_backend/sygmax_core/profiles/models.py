from django.db import models
import uuid
from ..auth.models import User
from django.conf import settings
from django.core.validators import FileExtensionValidator

class LanguageChoices(models.TextChoices):
    EN = 'en', 'English'
    RU = 'ru', 'Русский'
    ES = 'es', 'Español'
    
class ThemeChoices(models.TextChoices):
    LIGHT = 'light', 'Light Theme'
    DARK = 'dark', 'Dark Theme'
    SYSTEM = 'system', 'System Default'

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name='profile'
    )
    storage_path = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Путь к папке пользователя в S3'
    )
    full_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Полное имя'
    )
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/%d/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        verbose_name='Аватар пользователя'
    )
    bio = models.TextField(blank=True, max_length=500, verbose_name='biography')
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
        default=LanguageChoices.EN,
        verbose_name='Язык интерфейса'
    )
    timezone = models.CharField(
        max_length=50,
        verbose_name='Часовой пояс'
    )
    theme = models.CharField(
        max_length=10,
        choices=ThemeChoices.choices,
        default=ThemeChoices.LIGHT,
        verbose_name='Тема интерфейса'
    )
    email_notifications = models.BooleanField(
        default=True,
        verbose_name='Получение уведомлений по email'
    )
    push_notifications = models.BooleanField(
        default=True,
        verbose_name='Получение push-уведомлений'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['-created_at']

    def __str__(self):
        return f"Профиль пользователя {self.user.email}"

    @property
    def avatar_url(self):
        return self.avatar.url if self.avatar else None
