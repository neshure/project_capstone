from django.apps import AppConfig



class SmokeshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smokeShop'

    def ready(self):
        import smokeShop.signals