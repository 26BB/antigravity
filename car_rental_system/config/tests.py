from django.test import TestCase, Client
from accounts.models import User
from django.urls import reverse

class DashboardRoutingTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username='admin', password='pw', role='Admin')
        self.owner = User.objects.create_user(username='owner1', password='pw', role='owner')
        self.driver = User.objects.create_user(username='driver1', password='pw', role='driver')

    def test_routing(self):
        # Admin
        self.client.login(username='admin', password='pw')
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(response, 'dashboard/admin.html')
        self.client.logout()

        # Owner
        self.client.login(username='owner1', password='pw')
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(response, 'dashboard/owner.html')
        self.client.logout()

        # Driver
        self.client.login(username='driver1', password='pw')
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(response, 'dashboard/driver.html')
        self.client.logout()
