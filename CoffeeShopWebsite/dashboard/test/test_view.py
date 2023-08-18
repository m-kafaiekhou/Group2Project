from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class DashboardTests(TestCase):

    def test_url_exits_at_correct_location_for_list_view(self):
        response1 = self.client.get("add-category/")
        self.assertNotEqual(response1.status_code, 200)
        response2 = self.client.get("add-item/")
        self.assertNotEqual(response2.status_code, 200)
        response3 = self.client.get("category-list/")
        self.assertNotEqual(response3.status_code, 200)
        response4 = self.client.get("item-list/")
        self.assertNotEqual(response4.status_code, 200)
        response5 = self.client.get("order-list/")
        self.assertNotEqual(response5.status_code, 200)
        response6 = self.client.get("")
        self.assertNotEqual(response6.status_code, 200)