from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from coffeeshop.models import Footer
from menus.models import Category, CafeItem
from staff.models import CustomUserModel
from orders.models import Order, OrderItem
import tempfile


class DashboardTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.footer = Footer.objects.create()

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

        

    # def test_dashboard_list_view(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')

    #     response1 = self.client.get("add_category/")
    #     self.assertEqual(response1.status_code, 404)
    #     self.assertTemplateUsed(response1, "404.html")

    #     response2 = self.client.get("add_item/")
    #     self.assertEqual(response2.status_code, 404)
    #     self.assertTemplateUsed(response2, "404.html")

    #     response3 = self.client.get(reverse("dashboard:category_list"))
    #     self.assertEqual(response3.status_code, 200)
    #     self.assertTemplateUsed(response3, "dashboard/category_list.html")

    #     response4 = self.client.get(reverse("dashboard:item_list"))
    #     self.assertEqual(response4.status_code, 200)
    #     self.assertTemplateUsed(response4, "dashboard/item_list.html")

    #     response5 = self.client.get(reverse("dashboard:order_list"))
    #     self.assertEqual(response5.status_code, 200)
    #     self.assertTemplateUsed(response5, "dashboard/order_list.html")

    #     response6 = self.client.get(reverse("dashboard:dashboard"))
    #     self.assertEqual(response6.status_code, 200)
    #     self.assertTemplateUsed(response6, "dashboard/dashboard.html")


    # def test_dashboard_detail_view(self):
    #     self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')

    #     response7 = self.client.get(reverse("dashboard:order_details", kwargs={"pk":self.order.pk}))
    #     self.assertEqual(response7.status_code, 200)

    #     response8 = self.client.post(reverse("dashboard:order_item_update", kwargs={"pk":self.order.pk}))
    #     self.assertEqual(response8.status_code, 200)

    #     response9 = self.client.get("category-details/1/")
    #     self.assertEqual(response9.status_code, 200)
    #     response10 = self.client.get("item-details/1/")
    #     self.assertEqual(response10.status_code, 200)
    #     response11 = self.client.get("order-list/1/")
    #     self.assertEqual(response11.status_code, 200)
        

    def test_chart_list_view(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')

        response12 = self.client.get(reverse("dashboard:year-filter-options"))
        self.assertEqual(response12.status_code, 200)

        response13 = self.client.get(reverse("dashboard:month-filter-options"))
        self.assertEqual(response13.status_code, 200)

        response14 = self.client.get(reverse("dashboard:day-filter-options"))
        self.assertEqual(response14.status_code, 200)

        response15 = self.client.get(reverse("dashboard:this-year-sales"))
        self.assertEqual(response15.status_code, 200)

        response16 = self.client.get(reverse("dashboard:month-sales"))
        self.assertEqual(response16.status_code, 200)

        response17 = self.client.get(reverse("dashboard:day-sales"))
        self.assertEqual(response17.status_code, 200)

        response18 = self.client.get(reverse("dashboard:day-sales-sum"))
        self.assertEqual(response18.status_code, 200)

        response19 = self.client.get(reverse("dashboard:all-time-sales"))
        self.assertEqual(response19.status_code, 200)

        response20 = self.client.get(reverse("dashboard:top-selling"))
        self.assertEqual(response20.status_code, 200)
        # response21 = self.client.get("chart/sales/category-sale/")
        # self.assertEqual(response21.status_code, 200)
        # response22 = self.client.get("chart/sales/employee-sales/")
        # self.assertEqual(response22.status_code, 200)
        # response23 = self.client.get("chart/sales/peak-hour/")
        # self.assertEqual(response23.status_code, 200)
        # response24 = self.client.get("chart/sales/popular-items/")
        # self.assertEqual(response24.status_code, 200)
        


    def test_chart_detail_view(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')

        # response25 = self.client.get("chart/sales/top-selling/year/")
        # self.assertEqual(response25.status_code, 200)
        # response26 = self.client.get("chart/sales/status/C/")
        # self.assertEqual(response26.status_code, 200)
        pass