## File taken from django-portlets

# django imports
from django import template
from django.contrib.contenttypes.models import ContentType

# portlets imports
from minisite import utils
from minisite.models.portlet import PortletBlocking
from minisite.models.portlet import Slot

register = template.Library()

@register.inclusion_tag('minisite/portlet_slot.html', takes_context=True)
def portlet_slot(context, slot_name, instance=None):
    """
    Returns the portlets for given slot and instance. If the instance
    implements the ``get_parent_for_portlets`` method the portlets of
    the parent of the instance are also added.
    """

    if instance is None:
        return { "portlets" : [] }

    try:
        slot = Slot.objects.get(name=slot_name)
        # Set current slot
        context.update({'slot': slot})
    except Slot.DoesNotExist:
        return { "portlets" : [] }

    # Get portlets for given instance
    temp = utils.get_portlets(slot, instance)

    # Get inherited portlets
    try:
        instance.get_parent_for_portlets()
    except AttributeError:
        instance = None

    while instance:
        # If the portlets are blocked no portlets should be added
        if utils.is_blocked(instance, slot):
            break

        # If the instance has no get_parent_for_portlets, there are no portlets
        try:
            instance = instance.get_parent_for_portlets()
        except AttributeError:
            break

        # If there is no parent for portlets, there are no portlets to add
        if instance is None:
            break

        parent_portlets = utils.get_portlets(slot, instance)
        parent_portlets.reverse()
        for p in parent_portlets:
            if p not in temp:
                temp.insert(0, p)

    rendered_portlets = []

    # Render portlets
    for portlet in temp:
        rendered_portlets.append(portlet.render(context))

    return { "portlets" : rendered_portlets }
