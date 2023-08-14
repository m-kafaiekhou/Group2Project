from django.apps import AppConfig
from django.contrib.admin import apps
from core.admin import MainAdminArea


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

class MainAdminConfig(apps.AdminConfig) :
    default_site = 'core.admin.MainAdminArea'
