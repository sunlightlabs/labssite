from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

class ItemType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    icon_url = models.CharField(max_length=200, blank=True)

class FeedItem(models.Model):
    body = models.TextField(blank=True)
    link = models.URLField(blank=True)
    user = models.ForeignKey(User)
    item_type = models.ForeignKey(ItemType, related_name='items')
    feed = models.ForeignKey(Feed, related_name='items')
    timestamp = models.DateTimeField(auto_now_add=True)

