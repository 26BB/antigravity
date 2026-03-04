from django.test import TestCase
from accounts.models import User
from .models import Vehicle, VehicleAvailability
import datetime
from django.utils.timezone import make_aware

class VehicleModelTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner1', password='pw', role='owner')
        self.driver = User.objects.create_user(username='driver1', password='pw', role='driver')

    def test_vehicle_creation(self):
        vehicle = Vehicle.objects.create(
            owner=self.owner,
            make='Honda',
            model='Civic',
            year=2022,
            license_plate='XYZ987',
            insurance_provider='State Farm',
            insurance_policy_number='POL123',
            insurance_expiry='2025-01-01'
        )
        self.assertEqual(vehicle.make, 'Honda')
        self.assertEqual(vehicle.owner, self.owner)
        self.assertEqual(vehicle.status, 'active')

    def test_vehicle_availability_creation(self):
        vehicle = Vehicle.objects.create(
            owner=self.owner, make='Honda', model='Civic', year=2022, license_plate='XYZ987',
            insurance_provider='State Farm', insurance_policy_number='POL123', insurance_expiry='2025-01-01'
        )
        avail = VehicleAvailability.objects.create(
            vehicle=vehicle,
            day_of_week=0, # Monday
            start_time=datetime.time(9, 0),
            end_time=datetime.time(17, 0)
        )
        self.assertEqual(avail.day_of_week, 0)
        self.assertEqual(str(avail), f"{vehicle} available on Monday from 09:00:00 to 17:00:00")
