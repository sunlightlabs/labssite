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

#
# Akismet comment moderation
#

def validate_comment(sender, comment, request, **kwargs):
    from akismet import Akismet
    a = Akismet(settings.AKISMET_KEY, blog_url='http://sunlightlabs.com/')
    akismet_data = {
        'user_ip': comment.ip_address,
        'user_agent': request.META['HTTP_USER_AGENT'],
        'comment_author': comment.user_name,
        'comment_author_email': comment.user_email,
        'comment_author_url': comment.user_url,
        'comment_type': 'comment',
    }
    is_spam = a.comment_check(comment.comment.encode('ascii','ignore'), akismet_data)
    if is_spam:
        comment.is_public = False
comment_will_be_posted.connect(validate_comment, sender=Comment)

# save Post to newsfeed
from newsfeed.models import ItemType
from blogdor.models import Post
from django.db.models.signals import post_save
def post_callback(sender, instance, created, **kwargs):
    if instance.is_published():
        FeedItem.objects.create(title=instance.title, body=instance.excerpt,
                                link=instance.get_absolute_url(),
                                user=instance.author,
                                item_type=ItemType.objects.all()[0])
post_save.connect(post_callback, sender=Post)
