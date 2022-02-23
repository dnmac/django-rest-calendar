from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

User = get_user_model


@receiver(post_save, sender=User)
def create_user(created, **kwargs):
    """Terminal output for created user."""
    if created:
        print('User created!')
