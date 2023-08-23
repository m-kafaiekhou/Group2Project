from django.test import TestCase
from django.urls import reverse
from coffeeshop.models import Footer

class StaffUrlsTestCase(TestCase):
    def setUp(self):
        self.footer = Footer.objects.create()

    def test_login_url(self):
        #url = reverse('staff:login')
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(url, 'accounts/login/')
    def test_logout_url(self):
        #url = reverse('staff:logout')
        #self.assertEqual(url, 'accounts/logout/')
        response = self.client.get("/accounts/logout/")
        self.assertEqual(response.status_code, 200)