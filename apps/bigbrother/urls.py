from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',                       
    (r'^show$', 'bigbrother.views.show'),
    (r'^monthly.png$', 'bigbrother.views.make_monthly_graph'),
    (r'^month_data$', 'bigbrother.views.monthly_data'),
    (r'^yearly.png$', 'bigbrother.views.make_yearly_graph'),
)



