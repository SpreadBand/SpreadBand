from django.views.generic.list_detail import object_detail
from django.views.generic.create_update import create_object
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import Context, Template

from .models import Minisite, Layout
from .forms import LayoutForm

## MINISITE
def detail(request, minisite_id):
    """
    Render a minisite
    """
    minisite = get_object_or_404(Minisite, id=minisite_id)
    layout = get_object_or_404(Layout, id=minisite.layout.id)

    # Render our stored template
    # XXX: Replace this template system by a simpler one (sec. rltd)
    template = Template(layout.template)
    context = Context({})
    rendered_template = template.render(context)

    return render_to_response('minisite/minisite_detail.html',
                              { 'minisite': minisite,
                                'content' : rendered_template
                                },
                              )

## LAYOUT
def layout_create(request):
    """
    Create a new layout
    """
    return create_object(request,
                         form_class=LayoutForm,
                         template_name='minisite/layout_create.html',
                         )
                         

def layout_edit(request, layout_id):
    """
    Edit a given layout
    """

