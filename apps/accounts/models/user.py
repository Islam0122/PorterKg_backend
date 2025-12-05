from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from ..managers.user_manager import UserManager

AUTH_CHOICES = (
    ('local', 'Local'),
    ('google', 'Google'),
)

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('driver', 'Driver'),
    ('guest', 'Guest'),
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_verified = models.BooleanField(default=False)
    auth_type = models.CharField(max_length=10, choices=AUTH_CHOICES, default='local')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email
