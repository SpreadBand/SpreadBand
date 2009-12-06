from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('',
    (r'^new$', views.new),
#    (r'^my/list$', views.mylist),
)
