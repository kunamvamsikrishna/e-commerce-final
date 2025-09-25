from django.apps import AppConfig


class CAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'c_app'
    def ready(self):
        import c_app.signals