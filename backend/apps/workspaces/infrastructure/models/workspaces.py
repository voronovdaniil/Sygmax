from django.db import models
import uuid
from django.utils import timezone
from django.conf import settings

# 1. Основная сущность Workspace
class Workspace(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name="Название Workspace")
    description = models.TextField(blank=True, null=True, verbose_name="Описание Workspace")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name="Статус")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="owned_workspaces"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Workspace"
        verbose_name_plural = "Workspaces"

    def __str__(self):
        return self.name


# 2. Архивированные Workspaces
class ArchivedWorkspace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.OneToOneField(Workspace, on_delete=models.CASCADE, related_name="archived_info")
    archived_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    archived_at = models.DateTimeField(default=timezone.now)
    reason = models.TextField(blank=True, null=True, verbose_name="Причина архивирования")

    class Meta:
        verbose_name = "Архивированный Workspace"
        verbose_name_plural = "Архивированные Workspaces"


# 3. Связь пользователей с Workspace (WorkspaceMember)
class WorkspaceMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="workspace_memberships")
    role = models.ForeignKey("WorkspaceRole", on_delete=models.CASCADE, related_name="members")
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('workspace', 'user')
        verbose_name = "Участник Workspace"
        verbose_name_plural = "Участники Workspaces"


# 4. Роли в Workspace (WorkspaceRole)
class WorkspaceRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True, verbose_name="Название роли")

    class Meta:
        verbose_name = "Роль Workspace"
        verbose_name_plural = "Роли Workspaces"

    def __str__(self):
        return self.name


# 5. Настройки Workspace (WorkspaceSettings)
class WorkspaceSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.OneToOneField(Workspace, on_delete=models.CASCADE, related_name="settings")
    is_private = models.BooleanField(default=False, verbose_name="Приватность")
    enable_notifications = models.BooleanField(default=True, verbose_name="Включены ли уведомления")

    class Meta:
        verbose_name = "Настройки Workspace"
        verbose_name_plural = "Настройки Workspaces"


# 6. Теги Workspace (WorkspaceTag)
class WorkspaceTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="tags")
    tag = models.CharField(max_length=100, unique=True, verbose_name="Тег Workspace")

    class Meta:
        verbose_name = "Тег Workspace"
        verbose_name_plural = "Теги Workspaces"


# 7. Приглашения в Workspace (WorkspaceInvite)
class WorkspaceInvite(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="invites")
    email = models.EmailField(verbose_name="Email приглашенного")
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_invites")
    role = models.ForeignKey(WorkspaceRole, on_delete=models.CASCADE, related_name="invitees")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending", verbose_name="Статус приглашения")
    expires_at = models.DateTimeField(verbose_name="Срок действия")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('workspace', 'email')
        verbose_name = "Приглашение в Workspace"
        verbose_name_plural = "Приглашения в Workspaces"


# 8. История действий в Workspace (WorkspaceHistory)
class WorkspaceHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="history")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="workspace_actions")
    action = models.CharField(max_length=255, verbose_name="Описание действия")
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "История Workspace"
        verbose_name_plural = "История Workspaces"
 