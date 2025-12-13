from django.apps import AppConfig


class AjserpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ajserp'

    def ready(self):
        import ajserp.signals
        print("✅✅✅ signals.py LOADED SUCCESSFULLY ✅✅✅")
