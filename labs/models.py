from django.conf import settings
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_will_be_posted
from django.db import models
from djitter.models import account_updated
from sunlightlabs.labs import genimage
import djitter

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
            message = "%s (via @%s)" % (tweet.message, tweet.sender.username)
            djitter.post(account, message[:140])
    genimage.generate_image()
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
