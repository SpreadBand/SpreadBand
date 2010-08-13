from django.contrib.sitemaps import Sitemap

from .models import Venue

class VenueSitemap(Sitemap):
    def items(self):
        return Venue.objects.all()

    def lastmod(self, aVenue):
        return aVenue.last_activity
    
sitemaps = {
    'venue': VenueSitemap(),
}
