from django.test import TestCase
from orders.models import Order
from orders.admin import FilterOrder
import unicodedata
from django.urls import reverse
from staff.models import CustomUserModel


class AdminOrderTest(TestCase):
    def setUp(self):
        self.password = 'Test123@'
        self.user = CustomUserModel.objects.create_superuser(
            phone_number='09036138552',
            password='Test123@',
            first_name='fafsf',
            last_name='dfafsd'
        )
        self.fixtures = [
         Order.objects.create(
            status='A',
            phone_number='09036138552',
            table_number=1,
         ),
         Order.objects.create(
            status='D',
            phone_number='09036138552',
            table_number=1,
         ),
         Order.objects.create(
            status='C',
            phone_number='09036138552',
            table_number=1,
         )]
        self.should_be_untouched_cancel = Order.objects.create(
            status='C',
            phone_number='09036138552',
            table_number=1,
         )
        self.should_be_untouched_accept = Order.objects.create(
            status='A',
            phone_number='09036138552',
            table_number=1,
         )

    def test_accept_action(self):
        url = reverse('admin:orders_order_changelist')
        data = {'action': 'accept_order',
                '_selected_action': [str(f.id) for f in self.fixtures]}

        self.client.login(phone_number=self.user.phone_number, password=self.password)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.get(id=self.fixtures[0].id).status, 'A')
        self.assertEqual(Order.objects.get(id=self.fixtures[1].id).status, 'A')
        self.assertEqual(Order.objects.get(id=self.fixtures[2].id).status, 'A')
        self.assertEqual(
            Order.objects.get(id=self.should_be_untouched_cancel.id).status, 'C'
        )

    def test_draft_action(self):
        url = reverse('admin:orders_order_changelist')
        data = {'action': 'draft_order',
                '_selected_action': [str(f.id) for f in self.fixtures]}

        self.client.login(phone_number=self.user.phone_number, password=self.password)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.get(id=self.fixtures[0].id).status, 'D')
        self.assertEqual(Order.objects.get(id=self.fixtures[1].id).status, 'D')
        self.assertEqual(Order.objects.get(id=self.fixtures[2].id).status, 'D')
        self.assertEqual(
            Order.objects.get(id=self.should_be_untouched_accept.id).status, 'A'
        )

    def test_cancel_action(self):
        url = reverse('admin:orders_order_changelist')
        data = {'action': 'cancel_order',
                '_selected_action': [str(f.id) for f in self.fixtures]}

        self.client.login(phone_number=self.user.phone_number, password=self.password)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.get(id=self.fixtures[0].id).status, 'C')
        self.assertEqual(Order.objects.get(id=self.fixtures[1].id).status, 'C')
        self.assertEqual(Order.objects.get(id=self.fixtures[2].id).status, 'C')
        self.assertEqual(
            Order.objects.get(id=self.should_be_untouched_accept.id).status, 'A'
        )
