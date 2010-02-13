from django.contrib import admin


from .models.portlet import PortletAssignment
from .models.portlet import PortletBlocking
from .models.portlet import PortletRegistration
from .models.portlet import Slot

from .models.minisite import Minisite, Layout

admin.site.register((Minisite, Layout))
admin.site.register((PortletAssignment, PortletRegistration, PortletBlocking, Slot))
