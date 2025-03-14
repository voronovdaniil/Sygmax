from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import Group, Permission

# Менеджер пользователей
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Основная модель пользователя
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    email_confirmed = models.BooleanField(default=False, verbose_name='Email подтверждён')
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(auto_now=True)
    login_attempts = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions_set", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# OAuth-аккаунты
class OauthAccount(models.Model):
    class Provider(models.TextChoices):
        GOOGLE = 'google', 'Google'
        GITHUB = 'github', 'GitHub'
        FACEBOOK = 'facebook', 'Facebook'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='oauth_accounts')
    provider = models.CharField(max_length=50, choices=Provider.choices)
    provider_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

# Чёрный список токенов
class TokensBlacklist(models.Model):
    token = models.TextField(primary_key=True, max_length=500, verbose_name='Токен')
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(verbose_name='Дата истечения токена')

# Настройки безопасности пользователя
class UserSecurity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='security_settings')
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=255, blank=True, null=True)

