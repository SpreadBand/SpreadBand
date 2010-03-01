from django.db import models
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _

from minisite.models.portlet import Portlet
from minisite.utils import register_portlet

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
        from django.template.loader import get_template

        template = get_template('portlets/freetext.html')
        from django.template import Context

        context = Context({'title' : self.title,
                           'text' : self.text})

        render = template.render(context)

        return render

class TwitterPortlet(Portlet):
    """
    A portlet to display feeds from twitter
    """
    targets = models.CharField(_(u'Targets'), max_length=100, blank=True)

    def __unicode__(self):
        return 'Feed for %s' % self.targets

    def render(self, context):
        """
        Renders the portlet as html.
        """
        from django.template import Context

        new_context = Context({'portlet': self,
                               'MEDIA_URL' : context['MEDIA_URL'],
                               'minisite' : context['forObject'],
                               'slot': context['slot']}
                              )

        return render_to_string('portlets/twitter.html',
                                new_context)

    def config(self, request):
        """
        Configure the portlet
        """
        from .forms import TwitterPortletForm

        if request.method == 'POST':
            print 'new targets' + request.POST['targets']
            self.targets = request.POST['targets']
            self.save()

        return render_to_response(template_name='portlets/twitter_config.html',
                                  dictionary={'portlet': self,
                                              'form': TwitterPortletForm(instance=self)},
                                  context_instance=RequestContext(request)
                                  )

from album.models import Track
class AudioPlayerPortlet(Portlet):
    """
    A portlet to play music
    """
    song = models.ForeignKey(Track)

    def __unicode__(self):
        return 'Player for %s' % self.song.title

    def render(self, context):
        from django.template import Context

        new_context = Context({'portlet': self,
                               'MEDIA_URL' : context['MEDIA_URL'],
                               'minisite' : context['forObject'],
                               'slot': context['slot']}
                              )

        return render_to_string('portlets/jplayer.html',
                                new_context)

    def config(self, request):
        """
        Configure the portlet
        """
        from .forms import TwitterPortletForm

        if request.method == 'POST':
            print 'new targets' + request.POST['targets']
            self.targets = request.POST['targets']
            self.save()

        return render_to_response(template_name='portlets/jplayer_config.html',
                                  dictionary={'portlet': self,
                                              'form': TwitterPortletForm(instance=self)},
                                  context_instance=RequestContext(request)
                                  )


# Register the portlets
register_portlet(FreetextPortlet, 'FreetextPortlet')
register_portlet(TwitterPortlet, 'TwitterPortlet')
register_portlet(AudioPlayerPortlet, 'AudioPlayerPortlet')
