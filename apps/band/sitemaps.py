from django.contrib.sitemaps import Sitemap

from .models import Band

class BandSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Band.objects.all()

    def lastmod(self, aBand):
        return aBand.last_activity
    
sitemaps = {
    'band': BandSitemap(),
}
