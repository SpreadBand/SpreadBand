from django.db import models

from django.contrib.sites.models import Site

class DailyStats(models.Model):
    class Meta:
        abstract = True
        
    date = models.DateField(primary_key=True)

class BandStatsDaily(DailyStats):
    count = models.IntegerField(default=0)
    site = models.ForeignKey(Site)
    
from django.db.models.signals import post_save
from django.contrib.auth.models import User

import settings

from datetime import datetime

def new_user_cb(instance, created, **kwargs):
    today = datetime.now()
    if created:
        site = Site.objects.get(id=settings.SITE_ID)
        bs = BandStatsDaily.objects.get_or_create(date=today, site=site)[0]
        bs.count += 1
        bs.save()


post_save.connect(new_user_cb, sender=User)
