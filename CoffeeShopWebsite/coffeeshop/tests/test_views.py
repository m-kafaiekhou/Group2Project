from django.test import TestCase
from django.urls import reverse


class HomePageViewTestCase(TestCase):
    def test_home_page_context_data(self):
        url = reverse("coffeeshop:home")
        response = self.client.get(url)
        self.assertIn("top_rated_items", response.context)
        self.assertIsNone(response.context["top_rated_items"])
