from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('',                       
#    url(r'^list$', views.contract_list, name='contract-list'),
#    url(r'^new$', views.contract_new, name='contract-new'),
#    url(r'^detail/(?P<contract_id>\d+)/$', views.contract_detail, name='contract-detail'),
#    url(r'^update/(?P<contract_id>\d+)/$', views.contract_update, name='contract-update'),
   url(r'^closed/(?P<contract_id>\d+)/$', views.generic.contract_closed, name='contract-closed'),
)



