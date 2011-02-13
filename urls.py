from django.conf.urls.defaults import patterns, url, include

from django.conf import settings
from django.contrib.gis import admin
from django.contrib.sitemaps import FlatPageSitemap

from dajaxice.core import dajaxice_autodiscover

from .utils.sitemaps import DirectToTemplateSitemap
from .utils.views import home_spreadband

admin.autodiscover()
dajaxice_autodiscover()

# Sitemaps
# import venue.sitemaps
import band.sitemaps
# import event.sitemaps
sitemaps = {}
# sitemaps.update(venue.sitemaps.sitemaps)
sitemaps.update(band.sitemaps.sitemaps)
# sitemaps.update(event.sitemaps.sitemaps)

# For server errors
handler500 = 'django.views.defaults.server_error'
handler404 = 'django.views.defaults.page_not_found'

# URLS
urlpatterns = patterns('',
    # temporary index page
    url(r'^$', home_spreadband, name='home'),

    # Private beta
    url(r'^beta/$', 'privatebeta.views.invite', name='privatebeta_invite'),
    url(r'^beta/bars$', 'privatebeta.views.invite', {'template_name': 'privatebeta/invite-bars.html'}, name='privatebeta_invite_bars'),
    url(r'^beta/sent/$', 'privatebeta.views.sent', name='privatebeta_sent'),

    # auth + profile
    # (r'^user/', include('socialregistration.urls')),

    (r'^user/', include('account.urls', namespace='account')),
    (r'^user/', include('userena.urls')),


    # Contacts import
    (r'^user/contacts/', include('contacts_import.urls')),
    # Oauth auth
    (r'^user/oauth/', include('oauth_access.urls')),

    # avatar
    (r'^user/profile/avatar/', include('avatar.urls')),

    # comments
    (r'^comments/', include('django.contrib.comments.urls')),

    # reviews
    (r'^reviews/', include('reviews.urls')),

    # Feedback
    (r'^feedback/', include('backcap.urls', namespace='backcap')),

    # Bands
    (r'^b/', include('band.urls', namespace='band')),
    (r'^b/', include('album.urls', namespace='album')),
    (r'^b/', include('presskit.urls', namespace='presskit', app_name='presskit')),

    # Venues
    (r'^v/', include('venue.urls', namespace='venue')),

    # Events
    # (r'^e/', include('event.urls', namespace='event')),

    # bargain
    # (r'^e/gigbargain/', include('gigbargain.urls', namespace='gigbargain')),

    # static pages
    ('^pages/', include('django.contrib.flatpages.urls')),

    # BigBrother
    # (r'^bb/', include('bigbrother.urls')),

    # Ajax select channels
    (r'^ajax_select/', include('ajax_select.urls')),

    # Activity stream
    (r'^activity/', include('actstream.urls')),

    # Notifications
    (r'^notification/', include('notification.urls')),

    # Search
    (r'^search/', include('haystack.urls')),

    # FAQ
    (r'^faq/', include('faq.urls', namespace='faq')),

    # Social bridge
    (r'^socialbridge/', include('socialbridge.urls')),

    # Badges
#    (r'^badges/', include('badges.url')),
                      
    # REST API
    (r'^api/', include('api.urls')),

    (r'^robots\.txt$', include('robots.urls')),

    # Announcements
    url(r"^announcements/", include("announcements.urls")),

    # Dajax(ice)
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),

    # Django admin
    (r'^admin/', include(admin.site.urls)),
)



# Redirections
urlpatterns += patterns('django.views.generic.simple',
    url(r'^alpha/$', 'redirect_to', {'url': '/beta/', 'permanent': True}),
)

# Static pages
urlpatterns += patterns('django.views.generic',
        url(r'^discover/band$', 'simple.direct_to_template', {'template': 'band_discover.html'}, name='discover-band'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^styles$',             'django.views.generic.simple.direct_to_template', {'template': 'band_new_styles.html'}),

        url(r'^rosetta/', include('rosetta.urls')),
    )


# Sitemaps
sitemaps.update({'flatpages': FlatPageSitemap,
                 'pages': DirectToTemplateSitemap(urlpatterns)}
                )

urlpatterns += patterns('',
    # Robots.txt and sitemap
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
