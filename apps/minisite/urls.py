from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('',
                       url(r'^(?P<minisite_id>\d+)$', views.detail, name='detail'),
                       url(r'^layout/(?P<layout_id>\d+)/edit$', views.layout_edit, name='layout-edit'),
                       url(r'^layout/create$', views.layout_create, name='layout-create'),
)
