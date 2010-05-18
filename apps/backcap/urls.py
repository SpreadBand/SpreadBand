from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',             
    url(r'^new/(?P<referer>.*)$', views.feedback_new, name='feedback-new'),
    url(r'^new$', views.feedback_new, name='feedback-new'),

    url(r'^thanks$', views.feedback_thanks, name='feedback-thanks'),
    url(r'^list/page/(?P<page>[0-9]+)/$', views.feedback_list, name='feedback-list'),
    url(r'^list$', views.feedback_list, name='feedback-list'),
    url(r'^(?P<feedback_id>\d+)/$', views.feedback_detail, name='feedback-detail'),
    url(r'^(?P<feedback_id>\d+)/update$', views.feedback_update, name='feedback-update'),
    url(r'^(?P<feedback_id>\d+)/close$', views.feedback_close, name='feedback-close'),

    # Votes
    url(r'^(?P<feedback_id>\d+)/(?P<direction>up|down|clear)vote/?$', views.feedback_vote, name='feedback-vote'),

)



