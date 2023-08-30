from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from coffeeshop.models import Footer
from menus.models import Category, CafeItem
from staff.models import CustomUserModel
from orders.models import Order, OrderItem
from coffeeshop.models import Dashboard
from datetime import datetime
import tempfile
from model_bakery import baker
from ..views import ranking




class DashboardTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.footer = Footer.objects.create()
        cls.dashboard = Dashboard.objects.create()

        cls.user = CustomUserModel.objects.create_superuser(
            phone_number='09030001122',
            first_name='testfname',
            last_name='testlname',
            password='1X<ISRUkw+tuK',
            is_staff=True,
            is_active=True,
        )
        
        cls.category = Category.objects.create(name='test')

        cls.order = Order.objects.create(
            status='C',
            staff=cls.user,
            phone_number='09030001122',
            table_number=1,
        )

        cls.cafeitem1 = CafeItem.objects.create(
            name='test1',
            description='test1',
            is_available=True,
            price=50,
            category=cls.category,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )

        cls.orderitem1 = OrderItem.objects.create(
            order=cls.order,
            cafeitem=cls.cafeitem1,
            quantity=2,
        ).set_price()

        cls.cafeitem2 = CafeItem.objects.create(
            name='test2',
            description='test2',
            is_available=True,
            price=10,
            category=cls.category,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )

        cls.orderitem2 = OrderItem.objects.create(
            order=cls.order,
            cafeitem=cls.cafeitem2,
            quantity=3,
        ).set_price()

        cls.date_list = ["year", "month", "day"]

        cls.start_date = "2023-8-05"
        cls.end_date = "2023-8-20"
        cls.status = "C"
        

    # Item list view

    # def test_item_list_view(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse("item_list"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "dashboard/item_list.html")
    #
    #
    # def test_item_list_view_template(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse("item_list"))
    #     self.assertTemplateUsed(response, "dashboard/item_list.html")
    #
    #
    # def test_item_list_view_data(self): # Not Done
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse("item_list"))


    # Category list view

    # def test_category_list_view_connection(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse("category_list"))
    #     self.assertEqual(response.status_code, 200)
    #
    #
    #
    # def test_category_list_view_template(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse("category_list"))
    #     self.assertTemplateUsed(response, "dashboard/category_list.html")
    #
    #
    # def test_category_list_view_data(self): # Not Done
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse("category_list"))


    # Item Detail view

    # def test_item_detail_view(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     response = self.client.get(f"item-details/{self.cafeitem1.pk}")
    #     self.assertEqual(response.status_code, 404)
    #     self.assertTemplateUsed(response, "404.html")


    # Category Detail view

    # def test_category_detail_view(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     response = self.client.get(f"category-details/{self.category.pk}")
    #     self.assertEqual(response.status_code, 404)
    #     self.assertTemplateUsed(response, "404.html")


    # Order Detail view and Order Update view

    def test_order_detail_view_get(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("order_details", kwargs={"pk":self.order.pk}))
        self.assertEqual(response.status_code, 200)


    def test_order_detail_view_post(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        data = {
            "pk":self.orderitem1.pk,
            "orderitem":self.orderitem1,
            "quantity":3,
            "item":self.cafeitem1,
        }
        response = self.client.post(reverse("order_details", kwargs={"pk":self.order.pk}), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("order_details", kwargs={"pk":self.order.pk}))


    # Order List view

    def test_order_list_view_get(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("order_list"))
        self.assertEqual(response.status_code, 200)
        

    def test_order_list_view_template(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("order_list"))
        self.assertTemplateUsed(response, "dashboard/order_list.html")


    def test_order_list_view_post(self): # Not Done
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        data = {
            "itemId":self.order.pk,
        }
        response = self.client.post(reverse("order_status", kwargs={"stat":self.order.status}), data=data)
        self.assertEqual(response.status_code, 200)


    def test_order_status(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("order_status", kwargs={"stat":self.order.status}))
        self.assertEqual(response.status_code, 200)
        

    # Dashboard

    def test_dashboard_view_connection(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        


    def test_dashboard_view_connection(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("dashboard"))
        self.assertTemplateUsed(response, "dashboard/dashboard.html")
        

    # -------- Chart tests -------- #

    def test_year_filter_options(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("year-filter-options"))
        self.assertEqual(response.status_code, 200)
        

    def test_month_filter_options(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("month-filter-options"))
        self.assertEqual(response.status_code, 200)


    def test_day_filter_options(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("day-filter-options"))
        self.assertEqual(response.status_code, 200)


    def test_yearly_sales_chart(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("this-year-sales"))
        self.assertEqual(response.status_code, 200)


    def test_monthly_sales_chart(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("month-sales"))
        self.assertEqual(response.status_code, 200)


    def test_daily_sales_chart(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("day-sales"))
        self.assertEqual(response.status_code, 200)


    def test_sales_by_time_of_day(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("daily-time-sale"))
        self.assertEqual(response.status_code, 200)


    def test_sales_by_time_of_day_data_start_date_smaller(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        end_date = "2023-8-20"
        url = reverse("daily-time-sale")
        data = {'start_date': start_date, 'end_date': end_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Sales by Time of Day Between {start_date} and {end_date}",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertAlmostEqual(response.json(), expected_data)
        
    
    def test_sales_by_time_of_day_data_start_date_bigger(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        end_date = "2023-8-20"
        url = reverse("daily-time-sale")
        data = {'start_date': end_date, 'end_date': start_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Sales by Time of Day Between {start_date} and {end_date}",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertAlmostEqual(response.json(), expected_data)


    def test_sales_by_time_of_day_data_start_date_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        end_date = "2023-8-20"
        url = reverse("daily-time-sale")
        data = {'end_date': end_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Sales by Time of Day Between {None} and {end_date}",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertAlmostEqual(response.json(), expected_data)


    def test_sales_by_time_of_day_data_end_date_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        url = reverse("daily-time-sale")
        data = {'start_date': start_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Sales by Time of Day Between {start_date} and {None}",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertAlmostEqual(response.json(), expected_data)


    
    def test_sales_by_time_of_day_data_date_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        url = reverse("daily-time-sale")
        data = {}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Sales by Time of Day Between {None} and {None}",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertNotEqual(response.json(), expected_data)




    def test_total_sales(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("total-sales"))
        self.assertEqual(response.status_code, 200)


    def test_total_sales_data_start_date_smaller(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        end_date = "2023-8-20"
        url = reverse("total-sales")
        data = {'start_date': start_date, 'end_date': end_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Total Sales Between {start_date} and {end_date}",
            "data": {
                "labels": ["total"],
                "datasets": [{
                    "label": "Amount (T)",
                    "data": [0],
                }]
            }
        }
        self.assertEqual(response.json(), expected_data)
        
    
    def test_total_sales_data_start_date_bigger(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        end_date = "2023-8-20"
        url = reverse("total-sales")
        data = {'start_date': end_date, 'end_date': start_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Total Sales Between {start_date} and {end_date}",
            "data": {
                "labels": ["total"],
                "datasets": [{
                    "label": "Amount (T)",
                    "data": [0],
                }]
            }
        }
        self.assertEqual(response.json(), expected_data)


    def test_total_sales_data_start_date_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        end_date = "2023-8-20"
        url = reverse("total-sales")
        data = {'end_date': end_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Total Sales Between {None} and {end_date}",
            "data": {
                "labels": ["total"],
                "datasets": [{
                    "label": "Amount (T)",
                    "data": [0],
                }]
            }
        }
        self.assertEqual(response.json(), expected_data)


    def test_total_sales_data_end_date_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        url = reverse("total-sales")
        data = {'start_date': start_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Total Sales Between {start_date} and {None}",
            "data": {
                "labels": ["total"],
                "datasets": [{
                    "label": "Amount (T)",
                    "data": [0],
                }]
            }
        }
        self.assertEqual(response.json(), expected_data)


    
    def test_total_sales_data_date_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        url = reverse("total-sales")
        data = {}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Total Sales Between {None} and {None}",
            "data": {
                "labels": ["total"],
                "datasets": [{
                    "label": "Amount (T)",
                    "data": [0],
                }]
            }
        }
        self.assertNotEqual(response.json(), expected_data)




    def test_top_10_selling_items(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("top-selling"))
        self.assertEqual(response.status_code, 200)


    def test_top_10_selling_items_data_start_date_smaller(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        end_date = "2023-8-20"
        url = reverse("top-selling")
        data = {'start_date': start_date, 'end_date': end_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": "Top 10 Best Sellers",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertAlmostEqual(response.json(), expected_data)
        
    
    def test_top_10_selling_items_data_start_date_bigger(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        end_date = "2023-8-20"
        url = reverse("top-selling")
        data = {'start_date': end_date, 'end_date': start_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": "Top 10 Best Sellers",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertAlmostEqual(response.json(), expected_data)


    def test_top_10_selling_items_data_start_date_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        end_date = "2023-8-20"
        url = reverse("top-selling")
        data = {'end_date': end_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": "Top 10 Best Sellers",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertAlmostEqual(response.json(), expected_data)


    def test_top_10_selling_items_data_end_date_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        url = reverse("top-selling")
        data = {'start_date': start_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": "Top 10 Best Sellers",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertAlmostEqual(response.json(), expected_data)


    
    def test_top_10_selling_items_data_date_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        url = reverse("top-selling")
        data = {}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": "Top 10 Best Sellers",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertNotEqual(response.json(), expected_data)



    def test_top_10_customers(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("best-customers"))
        self.assertEqual(response.status_code, 200)


    def test_sales_by_category(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("category-sale"))
        self.assertEqual(response.status_code, 200)


    def test_sales_by_employee_connection(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("employee-sales"))
        self.assertEqual(response.status_code, 200)

    
    def test_sales_by_employee_data_start_date_smaller(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        end_date = "2023-8-20"
        url = reverse("employee-sales")
        data = {'start_date': start_date, 'end_date': end_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": "Employee Sales",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertAlmostEqual(response.json(), expected_data)
        
    
    def test_sales_by_employee_data_start_date_bigger(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        end_date = "2023-8-20"
        url = reverse("employee-sales")
        data = {'start_date': end_date, 'end_date': start_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": "Employee Sales",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertAlmostEqual(response.json(), expected_data)


    def test_sales_by_employee_data_start_date_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        end_date = "2023-8-20"
        url = reverse("employee-sales")
        data = {'end_date': end_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": "Employee Sales",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertAlmostEqual(response.json(), expected_data)


    def test_sales_by_employee_data_end_date_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        url = reverse("employee-sales")
        data = {'start_date': start_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": "Employee Sales",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertAlmostEqual(response.json(), expected_data)


    
    def test_sales_by_employee_data_date_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        url = reverse("employee-sales")
        data = {}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": "Employee Sales",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertNotEqual(response.json(), expected_data)



    def test_peak_business_hour(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("peak-hour"))
        self.assertEqual(response.status_code, 200)


    def test_most_popular_items(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("popular-items"))
        self.assertEqual(response.status_code, 200)


    def test_order_status_report_connection(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("status", kwargs={"status":"C"}))
        self.assertEqual(response.status_code, 200)


    def test_order_status_report_data_start_date_smaller(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        end_date = "2023-8-20"
        url = reverse("status", kwargs={"status":"C"})
        data = {'start_date': start_date, 'end_date': end_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Order Status Count between {start_date} and {end_date}",
            "data": {
                "labels": [],
                "datasets": [
                    {
                        "label": "Amount (T)",
                        "borderColor": "#d048b6",
                        "borderWidth": 2,
                        "borderDash": [],
                        "borderDashOffset": 0.0,
                        "pointBackgroundColor": "#d048b6",
                        "pointBorderColor": "rgba(255,255,255,0)",
                        "pointHoverBackgroundColor": "#d048b6",
                        "pointBorderWidth": 20,
                        "pointHoverRadius": 4,
                        "pointHoverBorderWidth": 15,
                        "pointRadius": 4,
                        "data": [],
                    }
                ],
            },
        }
        self.assertEqual(response.json(), expected_data)

    
    def test_order_status_report_data_start_date_bigger(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        end_date = "2023-8-20"
        url = reverse("status", kwargs={"status":"C"})
        data = {'start_date': end_date, 'end_date': start_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Order Status Count between {start_date} and {end_date}",
            "data": {
                "labels": [],
                        "label": "Amount (T)",
                        "borderColor": "#d048b6",
                        "borderWidth": 2,
                        "borderDash": [],
                        "borderDashOffset": 0.0,
                        "pointBackgroundColor": "#d048b6",
                        "pointBorderColor": "rgba(255,255,255,0)",
                        "pointHoverBackgroundColor": "#d048b6",
                        "pointBorderWidth": 20,
                        "pointHoverRadius": 4,
                        "pointHoverBorderWidth": 15,
                        "pointRadius": 4,
                        "data": [],
        }
        self.assertEqual(response.json(), expected_data)


    def test_order_status_report_data_start_date_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        end_date = "2023-8-20"
        url = reverse("status", kwargs={"status":"C"})
        data = {'end_date': end_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Order Status Count between {None} and {end_date}",
            "data": {
                "labels": [],
                        "label": "Amount (T)",
                        "borderColor": "#d048b6",
                        "borderWidth": 2,
                        "borderDash": [],
                        "borderDashOffset": 0.0,
                        "pointBackgroundColor": "#d048b6",
                        "pointBorderColor": "rgba(255,255,255,0)",
                        "pointHoverBackgroundColor": "#d048b6",
                        "pointBorderWidth": 20,
                        "pointHoverRadius": 4,
                        "pointHoverBorderWidth": 15,
                        "pointRadius": 4,
                        "data": [],
        }
        self.assertEqual(response.json(), expected_data)


    def test_order_status_report_data_end_date_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        url = reverse("status", kwargs={"status":"C"})
        data = {'start_date': start_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Order Status Count between {start_date} and {None}",
            "data": {
                "labels": [],
                        "label": "Amount (T)",
                        "borderColor": "#d048b6",
                        "borderWidth": 2,
                        "borderDash": [],
                        "borderDashOffset": 0.0,
                        "pointBackgroundColor": "#d048b6",
                        "pointBorderColor": "rgba(255,255,255,0)",
                        "pointHoverBackgroundColor": "#d048b6",
                        "pointBorderWidth": 20,
                        "pointHoverRadius": 4,
                        "pointHoverBorderWidth": 15,
                        "pointRadius": 4,
                        "data": [],
        }
        self.assertEqual(response.json(), expected_data)


    
    def test_order_status_report_data_date_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        url = reverse("status", kwargs={"status":"C"})
        data = {}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Order Status Count between {None} and {None}",
            "data": {
                "labels": ["C"],
                        "label": "Amount (T)",
                        "borderColor": "#d048b6",
                        "borderWidth": 2,
                        "borderDash": [],
                        "borderDashOffset": 0.0,
                        "pointBackgroundColor": "#d048b6",
                        "pointBorderColor": "rgba(255,255,255,0)",
                        "pointHoverBackgroundColor": "#d048b6",
                        "pointBorderWidth": 20,
                        "pointHoverRadius": 4,
                        "pointHoverBorderWidth": 15,
                        "pointRadius": 4,
                        "data": [1],
        }
        self.assertEqual(response.json(), expected_data)

    
    # customer_order_history Does not have a template

    # def test_customer_order_history(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse("customer-history"))
    #     self.assertEqual(response.status_code, 200)


    # def test_customer_order_history_check_template(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse("customer-history"))
    #     self.assertTemplateUsed(response, "")


    # def test_customer_order_history_data_start_date_smaller(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     start_date = "2023-8-10"
    #     end_date = "2023-8-20"
    #     phone = self.order.phone_number
    #     url = reverse("customer-history")
    #     data = {'start_date': start_date, 'end_date': end_date, 'phone_number': phone}
    #     response = self.client.get(url, data=data)

    #     expected_data = expected_data = {
    #         "customer_orderitem_data":"",
    #         "customer_order_data":"",
    #     }
    #     self.assertEqual(response.context, expected_data)

    
    # def test_customer_order_history_data_start_date_bigger(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     start_date = "2023-8-10"
    #     end_date = "2023-8-20"
    #     phone = self.order.phone_number
    #     url = reverse("customer-history")
    #     data = {'start_date': start_date, 'end_date': end_date, 'phone_number': phone}
    #     response = self.client.get(url, data=data)

    #     expected_data = expected_data = {
    #         "customer_orderitem_data":"",
    #         "customer_order_data":"",
    #     }
    #     self.assertEqual(response.context, expected_data)


    # def test_customer_order_history_data_start_date_none(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     end_date = "2023-8-20"
    #     phone = self.order.phone_number
    #     url = reverse("customer-history")
    #     data = {'end_date': end_date, 'phone_number': phone}
    #     response = self.client.get(url, data=data)

    #     expected_data = expected_data = {
    #         "customer_orderitem_data":"",
    #         "customer_order_data":"",
    #     }
    #     self.assertEqual(response.context, expected_data)


    # def test_customer_order_history_data_end_date_none(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     start_date = "2023-8-10"
    #     phone = self.order.phone_number
    #     url = reverse("customer-history")
    #     data = {'start_date': start_date, 'phone_number': phone}
    #     response = self.client.get(url, data=data)

    #     expected_data = expected_data = {
    #         "customer_orderitem_data":"",
    #         "customer_order_data":"",
    #     }
    #     self.assertEqual(response.context, expected_data)


    
    # def test_customer_order_history_data_date_none(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     phone = self.order.phone_number
    #     url = reverse("customer-history")
    #     data = {'phone_number': phone}
    #     response = self.client.get(url, data=data)

    #     expected_data = expected_data = {
    #         "customer_orderitem_data":"",
    #         "customer_order_data":"",
    #     }
    #     self.assertEqual(response.context, expected_data)


    # def test_customer_order_history_data_all_none(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     url = reverse("customer-history")
    #     data = {}
    #     response = self.client.get(url, data=data)

    #     expected_data = {
    #         "customer_orderitem_data":"",
    #         "customer_order_data":"",
    #     }
    #     self.assertEqual(response.context, expected_data)


    # -------- Customer Demographic tests -------- #

    def test_ranking(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        number = self.orderitem1.order.phone_number
        rank = ranking(number)
        self.assertEqual(rank, None)


    # customer_data Does not have a template

    # def test_customer_data(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse("customer-data"))
    #     self.assertEqual(response.status_code, 200)

    # def test_customer_data_check_template(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse("customer-data"))
    #     self.assertTemplateUsed(response, "")


    # def test_customer_data_phone_none(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     url = reverse("customer-data")
    #     data = {}
    #     response = self.client.get(url, data=data)

    #     expected_data = {}
    #     self.assertEqual(response.context, expected_data)

    
    # def test_customer_data(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
    #     phone = self.orderitem1.order.phone_number
    #     url = reverse("customer-data")
    #     data = {"phone_number":phone}
    #     response = self.client.get(url, data=data)

    #     expected_data = {
    #     "total_money_spent":"",       
    #     "average_money_spent":"",   
    #     "favorite_item":"",               
    #     "favorite_category":"",       
    #     "rank":"",                                 
    #     "all_attended_days":"",       
    #     }
    #     self.assertEqual(response.context, expected_data)



    def test_number_of_items_bought_connection(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("customer-items-bought"))
        self.assertEqual(response.status_code, 200)


    def test_number_of_items_bought_data_phone_none(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        url = reverse("customer-items-bought")
        data = {}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"No Data Found!",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    "data": [],
                }]
            }
        }
        self.assertEqual(response.json(), expected_data)

    
    def test_number_of_items_bought_data(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        phone = self.orderitem1.order.phone_number
        url = reverse("customer-items-bought")
        data = {"phone_number":phone}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Number of Each Item Bought By Customer",
            "data": {
                "labels": ['test1', 'test2'],
                "datasets": [{
                    "label": "Amount (T)",
                    "data": [2, 3],
                }]
            }
        }
        self.assertEqual(response.json(), expected_data)