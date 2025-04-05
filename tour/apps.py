from django.apps import AppConfig
# tour/apps.py

class TourConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tour'

    def ready(self):
        import tour.signals  # سیگنال‌ها رو لود کن
