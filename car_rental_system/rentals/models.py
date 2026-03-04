from django.conf import settings
from django.db import models
from vehicles.models import Vehicle

class RentalPolicy(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Company pays owner this rate per hour.")
    per_km_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Company pays owner this rate per km driven.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Rental Policies'

    def __str__(self):
        return f"{self.title} (Active: {self.is_active})"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    policy = models.ForeignKey(RentalPolicy, on_delete=models.PROTECT, related_name='bookings')
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    purpose = models.TextField(help_text="Why is this vehicle needed for company business?")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Booking for {self.vehicle} by {self.driver} ({self.status})"

class TripLog(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='trip_log')
    
    start_odometer = models.IntegerField()
    end_odometer = models.IntegerField()
    
    driver_feedback = models.TextField(blank=True, help_text="Any issues with the car?")
    owner_feedback = models.TextField(blank=True, help_text="Was the car returned in good condition?")
    
    logged_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def distance_driven(self):
        if self.end_odometer and self.start_odometer:
            return self.end_odometer - self.start_odometer
        return 0
        
    @property
    def total_cost(self):
        # Calculate cost based on distance and hourly rate
        policy = self.booking.policy
        distance_cost = float(self.distance_driven) * float(policy.per_km_rate)
        
        # Calculate hourly cost
        duration = self.logged_at - self.booking.start_time
        hours = duration.total_seconds() / 3600
        time_cost = float(hours) * float(policy.hourly_rate)
        
        return round(distance_cost + time_cost, 2)
        
    def __str__(self):
        return f"Log for {self.booking}"
