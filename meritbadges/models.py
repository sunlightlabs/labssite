from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

class Badge(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    image_url = models.URLField(verify_exists=False)

    recipients = models.ManyToManyField(User, through='BadgeAward', related_name='badges')

    def admin_image_tag(self):
        return '<img src="%s" title="%s" alt="%s" /> %s' % (self.image_url, self.name, self.name, self.name)
    admin_image_tag.allow_tags = True
    admin_image_tag.admin_order_field = 'name'

    def __unicode__(self):
        return self.name

class BadgeAward(models.Model):
    badge = models.ForeignKey(Badge, related_name='awards')
    user = models.ForeignKey(User, related_name='awards')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return '%s for %s' % (self.badge, self.user)
