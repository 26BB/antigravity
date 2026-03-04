from django.test import TestCase
from accounts.models import User
from vehicles.models import Vehicle, VehicleAvailability
from rentals.models import RentalPolicy, Booking, TripLog
from django.utils import timezone
import datetime

class RentalsTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='pw', role='Admin')
        self.owner = User.objects.create_user(username='owner1', password='pw', role='owner')
        self.driver = User.objects.create_user(username='driver1', password='pw', role='driver')

        self.vehicle = Vehicle.objects.create(
            owner=self.owner, make='Honda', model='Civic', year=2022, license_plate='XYZ123',
            insurance_provider='State Farm', insurance_policy_number='123', insurance_expiry='2025-01-01'
        )

        self.policy = RentalPolicy.objects.create(
            title='Standard',
            description='Standard',
            hourly_rate=10.00,
            per_km_rate=0.50,
            is_active=True
        )

    def test_total_cost_calculation(self):
        # 2 hours duration, 50 km driven
        # Cost = (2 * 10) + (50 * 0.50) = 20 + 25 = 45.00
        start_time = timezone.now() - datetime.timedelta(hours=2)
        end_time = timezone.now()

        booking = Booking.objects.create(
            driver=self.driver, vehicle=self.vehicle, policy=self.policy,
            start_time=start_time, end_time=end_time, status='completed', purpose='Test'
        )

        trip_log = TripLog.objects.create(
            booking=booking, start_odometer=1000, end_odometer=1050
        )

        # We need to simulate 'logged_at' which is auto_now_add. We can mock the duration or update logged_at directly.
        # Since logged_at is created roughly at timezone.now(), the duration is roughly 2 hours.
        # Let's enforce the exact logged_at
        trip_log.logged_at = end_time
        trip_log.save()

        self.assertAlmostEqual(trip_log.total_cost, 45.00, places=1)
