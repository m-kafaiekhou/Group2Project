from django.test import TestCase
from django.contrib.auth.admin import UserAdmin
from staff.models import CustomUserModel
from django.contrib.admin.sites import AdminSite


class CustomUserAdminTest(TestCase):


    def setUp(self):
        self.site = AdminSite()
        self.user_admin = UserAdmin(CustomUserModel, self.site)

    def test_search_fields(self):
        self.assertEqual(self.user_admin.search_fields, ('phone_number', 'last_name', 'first_name'))

    def test_list_filter(self):
        expected_list_filter = ('phone_number', 'last_name', 'first_name', 'is_active', 'is_staff')
        self.assertEqual(self.user_admin.list_filter, expected_list_filter)

    def test_ordering(self):
        expected_ordering = ('-date_added',)
        self.assertEqual(self.user_admin.ordering, expected_ordering)

    def test_list_display(self):
        expected_list_display = ('phone_number', 'last_name', 'first_name', 'is_active', 'is_staff', 'is_superuser')
        self.assertEqual(self.user_admin.list_display, expected_list_display)

    def test_fieldsets(self):
        expected_fieldsets = ( (None, {'fields': ('phone_number', 'last_name', 'first_name')}),
                               ('Permissions', {'fields': ('is_staff', 'is_active')}), )
        self.assertEqual(self.user_admin.fieldsets, expected_fieldsets)

    def test_add_fieldsets(self):
        expected_add_fieldsets = ( (None, { 'classes': ('wide',),
                                            'fields': ('phone_number', 'last_name', 'first_name',
                                                       'password1', 'password2','is_active','is_staff') }), )
        self.assertEqual(self.user_admin.add_fieldsets, expected_add_fieldsets)