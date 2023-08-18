from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class DashboardTests(TestCase):

    def test_url_exits_at_correct_location_for_dashboard_list_view(self):
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


    def test_url_exits_at_correct_location_for_dashboard_detail_view(self):
        response7 = self.client.get("order-details/1/")
        self.assertNotEqual(response7.status_code, 200)
        response8 = self.client.get("order-details/1/quantity/")
        self.assertNotEqual(response8.status_code, 200)
        response9 = self.client.get("category-details/1/")
        self.assertNotEqual(response9.status_code, 200)
        response10 = self.client.get("item-details/1/")
        self.assertNotEqual(response10.status_code, 200)
        response11 = self.client.get("order-list/1/")
        self.assertNotEqual(response11.status_code, 200)

    def test_url_exits_at_correct_location_for_chart_list_view(self):
        response12 = self.client.get("chart/year-filter-options/")
        self.assertNotEqual(response12.status_code, 200)
        response13 = self.client.get("chart/month-filter-options/")
        self.assertNotEqual(response13.status_code, 200)
        response14 = self.client.get("chart/day-filter-options/")
        self.assertNotEqual(response14.status_code, 200)
        response15 = self.client.get("chart/sales/this-year/")
        self.assertNotEqual(response15.status_code, 200)
        response16 = self.client.get("chart/sales/this-month/")
        self.assertNotEqual(response16.status_code, 200)
        response17 = self.client.get("chart/sales/this-day/")
        self.assertNotEqual(response17.status_code, 200)
        response18 = self.client.get("chart/sales/daily-sum/")
        self.assertNotEqual(response18.status_code, 200)
        response19 = self.client.get("chart/sales/all-time/")
        self.assertNotEqual(response19.status_code, 200)
        response20 = self.client.get("chart/sales/best-customers/")
        self.assertNotEqual(response20.status_code, 200)
        response21 = self.client.get("chart/sales/category-sale/")
        self.assertNotEqual(response21.status_code, 200)
        response22 = self.client.get("chart/sales/employee-sales/")
        self.assertNotEqual(response22.status_code, 200)
        response23 = self.client.get("chart/sales/peak-hour/")
        self.assertNotEqual(response23.status_code, 200)
        response24 = self.client.get("chart/sales/popular-items/")
        self.assertNotEqual(response24.status_code, 200)