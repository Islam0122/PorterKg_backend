from django.db import models
from .driver_profile import DriverProfile

class Car(models.Model):
    driver = models.OneToOneField(DriverProfile, on_delete=models.CASCADE, related_name="car")

    marka = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    year = models.PositiveIntegerField()
    number_plate = models.CharField(max_length=20)

    vin_code = models.CharField(max_length=100, blank=True)
    fuel_type = models.CharField(max_length=20, default="petrol")
    max_passengers = models.IntegerField(default=4)

    description = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.marka} {self.model}"
