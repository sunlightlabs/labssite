from django.conf import settings
from django.db.models import Manager
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.db.models.signals import post_save
from tagging.fields import TagField
import twitter
from geopy import geocoders

ROLES = (
    ('dev', 'Developer'),
    ('des', 'Designer'),
    ('both', 'Developer/Designer'),
    ('other', 'Community Member'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    photo = models.ImageField(upload_to='profile_images', blank=True)
    url = models.URLField(blank=True)
    location = models.CharField('description of location, hopefully geocodable (eg. Washington, DC)', max_length=100, blank=True)
    lat_long = models.PointField('geocoded location', null=True, blank=True)
    about = models.TextField(blank=True)
    role = models.CharField(max_length=5, choices=ROLES, default='other')
    twitter_id = models.CharField(max_length=15, blank=True)
    skills = TagField('comma separated list of your skills (eg. python, django)')

    objects = models.GeoManager()
    non_geo_manager = Manager()

    def static_google_map(self):
        base_url = 'http://maps.google.com/staticmap?markers=%(lat)s,%(long)s&zoom=12&size=210x210'
        return base_url % {'lat':self.lat_long.x, 'long':self.lat_long.y}

    def save(self, *args, **kwargs):
        if self.location:
            geocoder = geocoders.Google(settings.GMAPS_API_KEY)
            addr,point = geocoder.geocode(self.location)
            self.lat_long = Point(*point)
        super(Profile, self).save(*args, **kwargs)

    def possessive(self):
        name = self.user.first_name or self.user.username
        if name[-1] == 's':
            name = ''.join((name, "'"))
        else:
            name = ''.join((name, "'s"))
        return name

    def latest_tweets(self, num=5):
        if self.twitter_id:
            api = twitter.Api()
            return api.GetUserTimeline(self.twitter_id, count=num)

    def __unicode__(self):
        return unicode(self.user)

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
post_save.connect(create_profile, sender=User)
