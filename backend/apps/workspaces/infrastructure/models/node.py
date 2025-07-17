from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
import uuid
from django.utils import timezone
from django.conf import settings

class Node(MPTTModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name="Статус")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="owned_workspaces"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Родительский узел
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    
    # Тип узла (workspace, teamspace и т.д.)
    TYPE_CHOICES = [
        ('workspace', 'Workspace'),
        ('teamspace', 'Teamspace'),
    ]
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='teamspace')
    
    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"