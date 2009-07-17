from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from geopy import geocoders

class LocationModel(models.Model):
    location = models.CharField('description of location, hopefully geocodable (eg. Washington, DC)', max_length=100, blank=True)
    lat_long = models.PointField('geocoded location', null=True, blank=True)

    objects = models.GeoManager()

    def static_google_map(self):
        base_url = 'http://maps.google.com/staticmap?markers=%(lat)s,%(long)s&zoom=12&size=210x210'
        return base_url % {'lat':self.lat_long.x, 'long':self.lat_long.y}

    def save(self, *args, **kwargs):
        if self.location:
            geocoder = geocoders.Google(settings.GMAPS_API_KEY)
            addr,point = geocoder.geocode(self.location)
            self.lat_long = Point(*point)
        super(Profile, self).save(*args, **kwargs)

    class Meta:
        abstract = True
