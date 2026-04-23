from django.db import models
from django.conf import settings

# Create your models here.
class FarmerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='farmer_profile'
    )
    location = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)  # used for weather lookup
    crop = models.CharField(max_length=100, blank=True)
    farm_size_acres = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.get_full_name()} — {self.crop or "No crop set"}'