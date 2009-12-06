from django.views.generic.create_update import create_object

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


