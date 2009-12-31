from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('',                       
    (r'^list$', 'bargain.views.list'),
)



