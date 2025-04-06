from django.db import models
import uuid
from django.utils import timezone
from django.conf import settings

class BaseObject(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    ]
    TYPE_CHOICES = [
        ('page', 'Page'),
        ('block', 'Block')    
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    object_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Тип объекта")
    created_at = models.DateTimeField(default=timezone.now)
    edited_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="created_blocks"
    )
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="edited_blocks"
    )
    has_children = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name="Статус")
    
    