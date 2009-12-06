from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list

from authority.decorators import permission_required_or_403

from .models import Band


@permission_required_or_403('band_permission.add_band')
def new(request):
    """
    register a new band
    """
    return create_object(request,
                         model=Band,
                         template_name='bands/new.html',
                         )


def list(request):
    """
    list all bands
    """
    return object_list(request,
                       queryset=Band.objects.all(),
                       template_name='bands/list.html',
                       template_object_name='band',
                       )
