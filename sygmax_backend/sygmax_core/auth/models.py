from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from ..workspaces.models import Workspace

# Везде советуют вводить этот менеджер для кастомизации модели юзера
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

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email')
    # password_hash = models.CharField(max_length=255) это поле советуется убрать
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    email_confirmed = models.BooleanField(default=False, verbose_name='Email подтверждён')
    
    default_workspace = models.ForeignKey(Workspace,
                                          on_delete=models.CASCADE,
                                          null=True,
                                          blank=True,
                                          related_name='users')
    workspace_url = models.SlugField(max_length=255, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    login_attempts = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    

class Role(models.Model):
    class RoleName(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        USER = 'user', 'Пользователь'
        EDITOR = 'editor', 'Редактор'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50,
                          choices=RoleName.choices,
                          unique=True,
                          verbose_name='Название роли')
    
    def __str__(self):
        return self.name
    
class UserRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'role'],
                name='unique_user_role'
            )
        ]
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'

class OauthAccount(models.Model):
    class Provider(models.TextChoices):
        GOOGLE = 'google', 'Google'
        GITHUB = 'github', 'GitHub'
        FACEBOOK = 'facebook', 'Facebook'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='oauth_accounts')
    
    provider = models.CharField(max_length=50, choices=Provider.choices)
    provider_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'OAuth аккаунт'
        verbose_name_plural = 'OAuth аккаунты'
    
class TokensBlacklist(models.Model):
    token = models.TextField(primary_key=True, max_length=500, verbose_name='Токен')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(verbose_name='Дата истечения токена')
    
    class Meta:
        verbose_name = 'Чёрный список токенов'
        verbose_name_plural = 'Чёрный список токенов'
    
class UserSecurity(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='security_settings')
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=255, blank=True, null=True)
    
