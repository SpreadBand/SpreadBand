from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from portlets.models import Portlet
from portlets.utils import register_portlet

class FreetextPortlet(Portlet):
    """
    A simple portlet to display some text.
    """
    text = models.TextField(_(u'Text'), blank=True)

    def __unicode__(self):
        return '%s' % self.id

    def render(self, context):
        """
        Renders the portlet as html.
        """
        return render_to_string('portlets/freetext.html',
                                {'title' : self.title,
                                 'text' : self.text
                                 }
                                )

    def form(self, **kwargs):
        """
        """
        from .forms import FreetextPortletForm
        return FreetextPortletForm(instance=self, **kwargs)


# Register this portlet
register_portlet(FreetextPortlet, "FreetextPortlet")
