from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class DashboardTests(TestCase):

    def test_url_exits_at_correct_location_for_list_view(self):
        response1 = self.client.get("add-category/")
        self.assertNotEqual(response1.status_code, 200)
        response2 = self.client.get("add-item/")
        self.assertNotEqual(response2.status_code, 200)