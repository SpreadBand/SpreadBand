from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'list'}),
)

urlpatterns += patterns('',                       
    (r'^new$', 'gigplaces.views.new'),
    (r'^list$', 'gigplaces.views.list'),
    (r'^detail/(?P<gigplace_id>\d+)$', 'gigplaces.views.detail'),
)



