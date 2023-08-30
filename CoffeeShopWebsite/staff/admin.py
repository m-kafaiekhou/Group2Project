from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUserModel


@admin.register(CustomUserModel)
class UserAdminConfig(UserAdmin):
    model = CustomUserModel
    search_fields = ('phone_number', 'last_name', 'first_name',)
    list_filter = ('phone_number', 'last_name', 'first_name', 'is_active', 'is_staff')
    ordering = ('-date_added',)
    list_display = ('phone_number', 'last_name', 'first_name', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('phone_number', 'last_name', 'first_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    # formfield_overrides = {
    #     NewUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    # }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'last_name', 'first_name',
                       'password1', 'password2', 'is_active',
                       'is_staff', 'groups', 'user_permissions')
        }
         ),
    )
