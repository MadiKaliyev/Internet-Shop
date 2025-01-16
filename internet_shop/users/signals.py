from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User  

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Автоматически вызывается после создания нового пользователя.
    """
    if created:
        print(f"Профиль создан для пользователя: {instance.username}")
        instance.save()
