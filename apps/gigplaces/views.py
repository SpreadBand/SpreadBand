from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list, object_detail

from authority.decorators import permission_required_or_403

from schedule.periods import Month

from .models import GigPlace
from .forms import GigPlaceForm


@permission_required_or_403('gigplace_permission.add_gigplace')
def new(request):
    """
    register a new gigplace
    """
    return create_object(request,
                         form_class=GigPlaceForm,
                         template_name='gigplaces/gigplace_new.html',
                         )


def detail(request, gigplace_id):
    """
    Show details about a gigplace
    """
    period = [Month]
    return object_detail(request,
                         queryset=GigPlace.objects.all(),
                         object_id=gigplace_id,
                         template_name='gigplaces/gigplace_detail.html',
                         template_object_name='gigplace',
                         extra_context={"period" : period},
                         )
                          
def list(request):
    """
    list all gigplaces
    """
    return object_list(request,
                       queryset=GigPlace.objects.all(),
                       template_name='gigplaces/gigplace_list.html',
                       template_object_name='gigplace',
                       )


