from django.conf import settings
from django.db import models

class Vehicle(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('inactive', 'Inactive'),
    )
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    
    insurance_provider = models.CharField(max_length=100)
    insurance_policy_number = models.CharField(max_length=100)
    insurance_expiry = models.DateField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

class VehicleAvailability(models.Model):
    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        verbose_name_plural = 'Vehicle Availabilities'
        
    def __str__(self):
        return f"{self.vehicle} available on {self.get_day_of_week_display()} from {self.start_time} to {self.end_time}"
