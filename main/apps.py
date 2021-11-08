from django.apps import AppConfig

class FirstConfig(AppConfig):
    name = 'first'

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'


