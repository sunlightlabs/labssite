import datetime
from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __unicode__(self):
        return self.title


class FeedItem(models.Model):
    body = models.TextField(blank=True)
    link = models.TextField(blank=True)
    item_type = models.SlugField(max_length=20)
    user = models.ForeignKey(User)
    feed = models.ForeignKey(Feed, related_name='items')
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ('-timestamp',)

    def __unicode__(self):
        return self.body
