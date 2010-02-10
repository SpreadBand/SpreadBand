from django.contrib import admin

from .models import Minisite, Layout
admin.site.register((Minisite, Layout))


