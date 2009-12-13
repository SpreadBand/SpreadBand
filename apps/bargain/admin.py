from django.contrib import admin

from .models import Contract, Party

admin.site.register((Contract, Party))



