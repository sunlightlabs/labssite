from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from geopy import geocoders

class LocationModelQuerySet(models.query.GeoQuerySet):
    def search_by_distance(self, location, mile_radius):
        geocoder = geocoders.Google(settings.GMAPS_API_KEY)
        addr, point = geocoder.geocode(location)
        point = Point(*point)
        return self.filter(lat_long__distance_lte=(point, D(mi=mile_radius))).distance(point).order_by('distance')

class LocationModelManager(models.GeoManager):
    def get_query_set(self):
        return LocationModelQuerySet(self.model)

class LocationModel(models.Model):
    location = models.CharField('description of location, hopefully geocodable (eg. Washington, DC)', max_length=100, blank=True)
    lat_long = models.PointField('geocoded location', null=True, blank=True)

    objects = LocationModelManager()

    def static_google_map(self):
        base_url = 'http://maps.google.com/staticmap?markers=%(lat)s,%(long)s&zoom=12&size=210x210'
        return base_url % {'lat':self.lat_long.x, 'long':self.lat_long.y}

    def save(self, *args, **kwargs):
        if self.location:
            geocoder = geocoders.Google(settings.GMAPS_API_KEY)
            addr,point = geocoder.geocode(self.location)
            self.lat_long = Point(*point)
        super(LocationModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
