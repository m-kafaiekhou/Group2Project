from django.apps import AppConfig
from django.contrib.admin import apps


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

class MainAdminConfig(apps.AdminConfig) :
    default_site = 'core.admin.MainAdminArea'
