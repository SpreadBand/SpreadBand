from django.conf.urls.defaults import url, patterns
from django.conf import settings

import views.band
import views.venue
import views.dashboard

urlpatterns = patterns('',
    # Bargain
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)$', views.gigbargain_detail, name='gigbargain-detail'),

    # Dashboards
    url(r'^band/dashboard/(?P<band_slug>[-\w]+)$', views.dashboard.gigbargain_band_dashboard, name='gigbargain-band-dashboard'),

    # Bargain, comments
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/comments/(?P<section>[-\w]+)$', views.comments_section_display, name='gigbargain-comments-section-display'),

    # Bargain, venue specific
    url(r'^new/venue$', views.venue.gigbargain_new_from_venue, name='gigbargain-new-from-venue'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/venue/confirm_bands$', views.venue.gigbargain_venue_confirm_bands, name='gigbargain-venue-confirm-bands'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/venue/conclude$', views.venue.gigbargain_venue_conclude, name='gigbargain-venue-conclude'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/venue/decline$', views.venue.gigbargain_venue_decline, name='gigbargain-venue-decline'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/venue/enter$', views.venue.gigbargain_venue_enter_negociations, name='gigbargain-venue-enter'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/venue/renegociate', views.venue.gigbargain_venue_renegociate, name='gigbargain-venue-renegociate'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/venue/cancel', views.venue.gigbargain_venue_cancel, name='gigbargain-venue-cancel'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/venue/invite_band', views.venue.gigbargain_venue_invite_band, name='gigbargain-venue-invite-band'),

    # Bargain, band specific
    url(r'^new/band/(?P<band_slug>[-\w]+)$', views.band.gigbargain_new_from_band, name='gigbargain-new-from-band'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)/enter$', views.band.gigbargain_enter_for_band, name='gigbargain-band-enter'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)/reject$', views.band.gigbargain_refuse_for_band, name='gigbargain-band-refuse'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)/quit$', views.band.gigbargain_band_quit, name='gigbargain-band-quit'),

    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)/lock$', views.band.gigbargain_band_part_lock, name='gigbargain-band-part-lock'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)/unlock$', views.band.gigbargain_band_part_unlock, name='gigbargain-band-part-unlock'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)/edit$', views.band.gigbargain_band_part_edit, name='gigbargain-band-part-edit'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)/edit/timeline$', views.band.gigbargain_band_edit_timeline, name='gigbargain-band-edit-timeline'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)/edit/remuneration$', views.band.gigbargain_band_edit_remuneration, name='gigbargain-band-edit-remuneration'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)/edit/defrayment$', views.band.gigbargain_band_edit_defrayment, name='gigbargain-band-edit-defrayment'),

    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/band/(?P<band_slug>[-\w]+)$', views.band.gigbargain_band_part_display, name='gigbargain-band-part-display'),

    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/submit_to_venue', views.band.gigbargain_band_submit_draft_to_venue, name='gigbargain-band-submit-to-venue'),

    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/invite_band', views.band.gigbargain_band_invite_band, name='gigbargain-band-invite-band'),

    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/renegociate', views.band.gigbargain_band_draft_renegociate, name='gigbargain-band-draft-renegociate'),

    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/kick/(?P<band_slug>[-\w]+)', views.band.gigbargain_band_kick, name='gigbargain-band-kick'),



    # Bargain, common parts
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/common/band/(?P<band_slug>[-\w]+)$', views.band.gigbargain_band_common_edit, name='gigbargain-band-common-edit'),
    url(r'^(?P<gigbargain_uuid>[\w\d-]+)/common/venue$', views.venue.gigbargain_venue_common_edit, name='gigbargain-venue-common-edit'),

)


