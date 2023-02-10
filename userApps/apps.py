from django.apps import AppConfig


class UserappsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userApps'

    def ready(self):
        import userApps.signals