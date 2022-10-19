from django.apps import AppConfig
from django_x509.apps import DjangoX509Config


class Myx509Config(DjangoX509Config):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myx509'