from django.db import models
from .car import Car

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.car}"
