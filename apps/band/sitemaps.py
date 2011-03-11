from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from .models import Band

class BandSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Band.objects.all()

    def location(self, band):
        return reverse('presskit:presskit-detail', args=[band.slug])

    def lastmod(self, aBand):
        return aBand.last_activity
    
sitemaps = {
    'band': BandSitemap(),
}
