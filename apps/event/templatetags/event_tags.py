from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.inclusion_tag('event/gig_vevent.html')
def gig_vevent(aGig):
    """
    Generates a microformat vevent for a gig

    Usage::

       {%  gig_vevent [object] %}

    """
    if not aGig:
        raise template.TemplateSyntaxError, "gig_vevent tag requires exactly two arguments"

    return {'gig': aGig}
