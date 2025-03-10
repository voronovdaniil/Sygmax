from django.db.models.signals import post_save
from django.dispatch import receiver
from ..auth.models import User
from .models import UserProfile
import uuid

def generate_storage_path(user_id):
    """Генерирует уникальный путь для хранения файлов пользователя"""
    return f"users/{user_id}/{uuid.uuid4()}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создает профиль пользователя при регистрации"""
    if created:
        UserProfile.objects.create(
            user=instance,
            full_name=instance.full_name,  # Копируем полное имя из модели User
            storage_path=generate_storage_path(instance.id)  # Генерируем уникальный путь хранения
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Обновляет профиль при изменении данных пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.full_name = instance.full_name
        instance.profile.save()