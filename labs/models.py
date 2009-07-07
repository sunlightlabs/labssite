from django.conf import settings
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_will_be_posted
from django.db import models
from djitter.models import account_updated
import djitter

def tweet_callback(sender, **kwargs):
    if not settings.DEBUG:
        account = kwargs['account']
        for tweet in reversed(kwargs['tweets']):
            message = "%s (via @%s)" % (tweet.message, tweet.sender.username)
            djitter.post(account, message[:140])
account_updated.connect(tweet_callback)

# save Post to newsfeed
from newsfeed.models import ItemType, FeedItem
from blogdor.models import Post
from django.db.models.signals import post_save
def post_callback(sender, instance, created, **kwargs):
    if instance.is_published:
        FeedItem.objects.create(title=instance.title, body=instance.excerpt,
                                link=instance.get_absolute_url(),
                                user=instance.author,
                                item_type=ItemType.objects.all()[0])
#post_save.connect(post_callback, sender=Post)
