from django.contrib.gis.db import models

class City(models.Model):
    name = models.CharField(max_length=60)
    insee = models.CharField(max_length=5)
    zip = models.CharField(max_length=5)
    geom = models.PointField()
    objects = models.GeoManager()


class Place(models.Model):
    """
    A place in the world
    """
    objects = models.GeoManager()


    address = models.TextField()
    geom = models.PointField()

    def __unicode__(self):
        return self.address

