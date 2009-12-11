from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list, object_detail

from authority.decorators import permission_required_or_403

from .models import Band
from .forms import BandForm


@permission_required_or_403('band_permission.add_band')
def new(request):
    """
    register a new band
    """
    return create_object(request,
                         form_class=BandForm,
                         template_name='bands/band_new.html',
                         )

def detail(request, band_id):
    """
    Show details about a band
    """
    return object_detail(request,
                         queryset=Band.objects.all(),
                         object_id=band_id,
                         template_object_name='band'
                         )
                          
def list(request):
    """
    list all bands
    """
    return object_list(request,
                       queryset=Band.objects.all(),
                       template_name='bands/band_list.html',
                       template_object_name='band',
                       )
