from django.contrib import admin
from django_x509.admin import CaAdmin, CertAdmin
from myx509.models import DocSign

# CaAdmin.list_display.insert(1, 'my_custom_field') <-- your custom change example
CertAdmin.list_display.insert(2, 'personne')
CertAdmin.fields.insert(3, 'personne')