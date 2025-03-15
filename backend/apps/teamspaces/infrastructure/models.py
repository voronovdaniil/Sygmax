from django.db import models
import uuid
from django.utils import timezone

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='Название команды')
    description = models.TextField(blank=True, verbose_name='Описание команды')
    owner_id = models.UUIDField(verbose_name='Владелец команды')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class TeamMember(models.Model):
    class RoleChoices(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        MEMBER = 'member', 'Участник'
        GUEST = 'guest', 'Гость'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user_id = models.UUIDField(verbose_name='ID пользователя')
    role = models.CharField(max_length=20, choices=RoleChoices.choices)
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('team', 'user_id')

class TeamInvite(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Ожидает'
        ACCEPTED = 'accepted', 'Принято'
        DECLINED = 'declined', 'Отклонено'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invites')
    email = models.EmailField(verbose_name='Email приглашенного')
    invited_by_id = models.UUIDField(verbose_name='Пригласивший')
    role = models.CharField(max_length=20, choices=TeamMember.RoleChoices.choices)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    expires_at = models.DateTimeField(verbose_name='Срок действия')
    created_at = models.DateTimeField(default=timezone.now)
