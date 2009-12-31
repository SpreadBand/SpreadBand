from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list, object_detail

from .models import Contract

def list(request, band_id):
    return object_list(request,
                       queryset=Contract.objects.all(),
                       template_name='bargain/contract_list.html',
                       template_object_name='contract',
                       )
