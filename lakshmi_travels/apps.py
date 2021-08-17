from django.apps import AppConfig


class LakshmiTravelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lakshmi_travels'

    def ready(self):
        from . import signals