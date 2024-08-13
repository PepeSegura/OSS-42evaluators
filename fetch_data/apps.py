from django.apps import AppConfig


class FetchDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fetch_data'

    def ready(self):
        from update_database import schedule_update
        schedule_update.start()
