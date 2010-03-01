from django.views.generic.list_detail import object_detail
from django.views.generic.create_update import create_object
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import Context, Template, RequestContext

from .models.portlet import Slot, PortletRegistration, Portlet, PortletAssignment
from .models.minisite import Minisite, Layout

from .forms import LayoutForm

from bands.models import Band

## MINISITE
def detail(request, minisite_id, template='minisite/minisite_detail.html'):
    """
    Render a minisite
    """
    minisite = get_object_or_404(Minisite, id=minisite_id)
    layout = get_object_or_404(Layout, id=minisite.layout.id)

    # Render our stored template
    # XXX: Replace this template system by a simpler one (sec. rltd)
    templ = Template(layout.template)
    context = RequestContext(request, {'forObject' : minisite})
    rendered_template = templ.render(context)
    
    return render_to_response(template,
                              { 'minisite': minisite,
                                'content' : rendered_template,
                                },
                              context_instance=RequestContext(request)
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
                         

from django.views.generic.simple import direct_to_template
def layout_edit(request, layout_id):
    """
    Edit a given layout
    """
    return direct_to_template(request,
                              'minisite/layout_edit.html')


def layout_save(request, layout_id):
    """
    Save a given layout
    """
    from django.http import HttpResponse, HttpResponseBadRequest
    from django.core import serializers
    import json
    if request.method == 'GET':
        rlay = request.GET['layout']
        print rlay
        for o in json.loads(rlay):
            print o
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

## PORTLETS
def portlet_assign(request, minisite_id, slot_id, portlet_type, portlet_id):
    minisite = get_object_or_404(Minisite, id=minisite_id)
    slot = get_object_or_404(Slot, id=slot_id)

def portlet_config(request, minisite_id, slot_id):
    minisite = get_object_or_404(Minisite, id=minisite_id)
    slot = get_object_or_404(Slot, id=slot_id)
    assignment = get_object_or_404(PortletAssignment, slot=slot)

    return assignment.portlet.config(request)

def portlet_render(request, minisite_id, slot_id):
    from django.http import HttpResponse

    minisite = get_object_or_404(Minisite, id=minisite_id)
    slot = get_object_or_404(Slot, id=slot_id)
    assignment = get_object_or_404(PortletAssignment, slot=slot)

    res = assignment.portlet.render(RequestContext(request, 
                                                   {'forObject' : minisite,
                                                    'slot': slot}
                                                   )
                                    )
    
    return HttpResponse(res)
