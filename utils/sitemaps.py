import datetime

from django.contrib.sitemaps import Sitemap

class DirectToTemplateSitemap(Sitemap):
  def __init__(self, patterns):
    self.patterns = patterns

  def items(self):
    return [p for p in self.patterns if p.callback 
               and p.callback.__module__ == 'django.views.generic.simple'
               and p.callback.func_name == 'direct_to_template']

  def location(self, obj):
    url = obj.regex.pattern.replace('^', '/').replace('$','')
    return url
