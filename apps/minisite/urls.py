from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('',
   # Minisite
   url(r'^(?P<minisite_id>\d+)$', views.detail, name='detail'),

   # Layout
   url(r'^layout/create$', views.layout_create, name='layout-create'),
   url(r'^layout/(?P<layout_id>\d+)/edit$', views.layout_edit, name='layout-edit'),

)
