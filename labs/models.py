from django.conf import settings
from django.db import models
from djitter.models import account_updated
from sunlightlabs.labs import genimage
import djitter

PROJECT_TYPE_CHOICES = (
    ('api', 'API'),
    ('data', 'Data'),
    ('os', 'Open Source'),
)

class Project(models.Model):
    type = models.CharField(max_length=8, choices=PROJECT_TYPE_CHOICES, db_index=True)
    name = models.CharField(max_length=128, db_index=True)
    description = models.TextField()
    url = models.URLField(verify_exists=False, blank=True, null=True)
    is_enabled = models.BooleanField(default=False, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class Hero(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(max_length=128)
    location = models.CharField(max_length=128, blank=True, null=True)
    organization = models.CharField(max_length=128, blank=True, null=True)
    organization_url = models.URLField(verify_exists=False, blank=True, null=True)
    is_enabled = models.BooleanField(default=False, db_index=True)
    has_photo = models.BooleanField(default=False, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

def tweet_callback(sender, **kwargs):
    if not settings.DEBUG:
        account = kwargs['account']
        for tweet in reversed(kwargs['tweets']):
            message = "@%s says: %s" % (tweet.sender.username, tweet.message)
            djitter.post(account, message[:140])
    genimage.generate_image()
account_updated.connect(tweet_callback)