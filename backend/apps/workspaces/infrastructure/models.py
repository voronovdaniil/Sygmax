from django.db import models
import uuid
from django.utils import timezone

# Модель воркспейса
class Workspace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='Название воркспейса')
    description = models.TextField(verbose_name='Описание воркспейса', blank=True)
    owner_id = models.UUIDField(verbose_name='Владелец воркспейса', null=True)
    is_personal = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

# Участники воркспейса
class WorkspaceMember(models.Model):
    class RoleChoices(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        MEMBER = 'member', 'Участник'
        GUEST = 'guest', 'Гость'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(verbose_name='ID пользователя')  # Без ForeignKey!
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=20, choices=RoleChoices.choices, verbose_name='Роль участника')
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user_id', 'workspace')

# Приглашения в воркспейс
class WorkspaceInvite(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Ожидает'
        ACCEPTED = 'accepted', 'Принято'
        DECLINED = 'declined', 'Отклонено'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='invites')
    email = models.EmailField(verbose_name='Email приглашенного')
    invited_by_id = models.UUIDField(verbose_name='Пригласивший')  # Без ForeignKey!
    role = models.CharField(max_length=20, choices=WorkspaceMember.RoleChoices.choices)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    expires_at = models.DateTimeField(verbose_name='Срок действия')
    created_at = models.DateTimeField(default=timezone.now)

