from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.inclusion_tag('band/vcard.html')
def band_vcard(aBand):
    """
    Generates a microformat vcard for a band

    Usage::

       {%  band_vcard [object] %}

    Examples::

       {% band_vcard lymbago %}

    """
    if not aBand:
        raise template.TemplateSyntaxError, "band_vcard tag requires exactly two arguments"

    return {'band': aBand}








