from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('',
   # Minisite
   url(r'^(?P<minisite_id>\d+)$', views.detail, name='detail'),

   # Porlets
   url(r'^slot/render/(?P<minisite_id>\d+)/(?P<slot_id>\d+)$', views.portlet_render, name='portlet-render'),
   url(r'^slot/config/(?P<minisite_id>\d+)/(?P<slot_id>\d+)$', views.portlet_config, name='portlet-config'),
                       
   # Layout
   url(r'^layout/create$', views.layout_create, name='layout-create'),
   url(r'^layout/(?P<layout_id>\d+)/edit/$', views.layout_edit, name='layout-edit'),
   url(r'^layout/(?P<layout_id>\d+)/edit/save$', views.layout_save, name='layout-save'),

)
