from django.db import models
from django.contrib.auth.models import User

class ItemType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    icon_url = models.CharField(max_length=200, blank=True)

class FeedItem(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    link = models.URLField(blank=True)
    user = models.ForeignKey(User)
    item_type = models.ForeignKey(ItemType)
    timestamp = models.DateTimeField(auto_now_add=True)

class Feed(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    items = models.ManyToManyField(FeedItem, related_name='feeds')

