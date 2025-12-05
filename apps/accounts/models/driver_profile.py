from django.db import models
from .user import User


class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="driver_profile")
    phone_number = models.CharField(max_length=20)
    bio = models.TextField(max_length=500, blank=True)

    rating = models.FloatField(default=100)
    experience_years = models.IntegerField(default=0)
    verified_driver = models.BooleanField(default=False)

    driver_license_number = models.CharField(max_length=50)
    driver_license_category = models.CharField(max_length=10)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Driver: {self.user.email}"
