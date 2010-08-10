from django.contrib.gis import admin
from .models import City

class CityAdmin(admin.GeoModelAdmin):
    #extra_js = [settings.GMAP.api_url + GMAP.key]
    #map_template = 'world/admin/google.html'
    pass

admin.site.register(City, CityAdmin)
