from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('driver', 'Salaried Driver'),
        ('owner', 'Car Owner'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='driver')
    phone_number = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    
    # Driver specific details (optional for owners/admins)
    license_number = models.CharField(max_length=50, blank=True)
    license_expiry = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
