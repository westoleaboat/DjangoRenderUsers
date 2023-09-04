from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_initial_superuser(sender, instance, created, **kwargs):
    if created and not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', '', '123')
