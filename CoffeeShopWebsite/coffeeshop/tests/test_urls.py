from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class HomePageUrlTestCase(TestCase):
    def test_home_page_url(self):
        url = reverse("coffeeshop:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "coffeeshop/home.html")
