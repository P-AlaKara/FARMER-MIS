from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import FarmerProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_farmer_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'farmer':
        FarmerProfile.objects.get_or_create(user=instance)