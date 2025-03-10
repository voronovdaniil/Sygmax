from django.db import models
import uuid
from ..auth.models import User

class Workspace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='Название воркспейса')
    description = models.TextField(verbose_name='Описание воркспейса', blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_workspaces',
        verbose_name='Владелец воркспейса'
    )
    is_personal = models.BooleanField(default=False, verbose_name='Персональный воркспейс')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Рабочее пространство'
        verbose_name_plural = 'Рабочие пространства'

    def __str__(self):
        return self.name


class WorkspaceMember(models.Model):
    class RoleChoices(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        MEMBER = 'member', 'Участник'
        GUEST = 'guest', 'Гость'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workspace_memberships',
        verbose_name='Участник'
    )
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name='Рабочее пространство'
    )
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        verbose_name='Роль участника'
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Участник рабочего пространства'
        verbose_name_plural = 'Участники рабочего пространства'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'workspace'],
                name='unique_workspace_member'
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.workspace} ({self.role})"


class WorkspaceInvite(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Ожидает'
        ACCEPTED = 'accepted', 'Принято'
        DECLINED = 'declined', 'Отклонено'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='invites',
        verbose_name='Рабочее пространство'
    )
    email = models.EmailField(verbose_name='Email приглашенного')
    invited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_invites',
        verbose_name='Пригласил'
    )
    role = models.CharField(
        max_length=20,
        choices=WorkspaceMember.RoleChoices.choices,
        verbose_name='Предлагаемая роль'
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name='Статус приглашения'
    )
    expires_at = models.DateTimeField(verbose_name='Срок действия')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Приглашение'
        verbose_name_plural = 'Приглашения'
        constraints = [
            models.UniqueConstraint(
                fields=['workspace', 'email'],
                name='unique_workspace_invite'
            )
        ]

    def __str__(self):
        return f"Приглашение для {self.email} в {self.workspace}"
