from django.apps import AppConfig


class MainsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MainSite'

    def ready(self):
        import MainSite.signals