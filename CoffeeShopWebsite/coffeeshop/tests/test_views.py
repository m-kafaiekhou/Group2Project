from django.test import TestCase
from django.urls import reverse


class HomePageViewTestCase(TestCase):
    def test_home_page_context_data(self):
        url = reverse("coffeeshop:home")
        response = self.client.get(url)
        self.assertIn("top_rated_items", response.context)
        self.assertIsNone(response.context["top_rated_items"])


class GalleryPageViewTestCase(TestCase):
    def test_gallery_page_context_data(self):
        url = reverse("coffeeshop:gallery")
        response = self.client.get(url)
        self.assertIn("page_name", response.context)
        self.assertEqual(response.context["page_name"], "gallery")
