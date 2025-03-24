from django.db import models

import uuid

from django.utils import timezone

  

# Модель тимспейса

class Teamspace(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active'
        ARCHIVED = 'archived'
        DELETED = 'deleted'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace_id = models.UUIDField()
    name = models.CharField(max_length=255, verbose_name='Название тимспейса')
    description = models.TextField(verbose_name='Описание тимспейса', blank=True)
    owner_id = models.UUIDField(verbose_name='Владелец тимспейсы', null=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

# Участники тимспейса

class TeamspaceMember(models.Model):
    class RoleChoices(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        MEMBER = 'member', 'Участник'
        GUEST = 'guest', 'Гость'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(verbose_name='ID пользователя') # Без ForeignKey!
    teamspace = models.ForeignKey(Teamspace, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=20, choices=RoleChoices.choices, verbose_name='Роль участника')
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user_id', 'teamspace')

  

# Приглашения в тимспейс

class TeamspaceInvite(models.Model):

    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Ожидает'
        ACCEPTED = 'accepted', 'Принято'
        DECLINED = 'declined', 'Отклонено'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teamspace = models.ForeignKey(Teamspace, on_delete=models.CASCADE, related_name='invites')
    email = models.EmailField(verbose_name='Email приглашенного')
    invited_by_id = models.UUIDField(verbose_name='Пригласивший') # Без ForeignKey!
    role = models.CharField(max_length=20, choices=TeamspaceMember.RoleChoices.choices)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    expires_at = models.DateTimeField(verbose_name='Срок действия')
    created_at = models.DateTimeField(default=timezone.now)


class ArchivedTeamspace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teamspace_id = models.ForeignKey(Teamspace, on_delete=models.CASCADE, related_name='archive')
    archived_by = models.UUIDField()
    archived_at = models.DateTimeField(default=timezone.now)
    reason = models.TextField(null=True)
  

class TeamspaceRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)


class TeamspaceSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teamspace = models.ForeignKey(Teamspace, on_delete=models.CASCADE, related_name='settings')
    is_private = models.BooleanField(default=False)
    enable_notifications = models.BooleanField(default=True)


class TeamspaceTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teamspace = models.ForeignKey(Teamspace, on_delete=models.CASCADE, related_name='tag')
    tag = models.CharField(max_length=100, unique=True) 

class TeampaceHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teamspace = models.ForeignKey(Teamspace, on_delete=models.CASCADE, related_name='history')
    user_id = models.UUIDField()
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)