from django.test import TestCase
from django.urls import reverse
class StaffUrlsTestCase(TestCase):
    def test_login_url(self):
        url = reverse('staff:login')
        self.assertEqual(url, '/accounts/login/')
    def test_logout_url(self):
        url = reverse('staff:logout')
        self.assertEqual(url, '/accounts/logout/')