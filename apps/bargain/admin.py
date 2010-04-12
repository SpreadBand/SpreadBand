from django.contrib import admin

from .models import Contract, Party, Terms, ContractParty

admin.site.register((Contract, Party, Terms, ContractParty))



