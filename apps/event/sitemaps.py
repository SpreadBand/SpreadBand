from django.contrib.sitemaps import Sitemap

from .models import Gig

class GigSitemap(Sitemap):
    def items(self):
        return Gig.objects.all()

    def lastmod(self, aGig):
        return aGig.mod_date
    
sitemaps = {
    'gig': GigSitemap(),
}
