from django.db.models.signals import post_save
from django.contrib.auth.models import User
from feedinator.models import FeedEntry
from blogdor.models import Post
from newsfeed.models import Feed
from anthill.events.models import Event
from anthill.projects.models import Project
from brainstorm.models import Idea
import popular

def url_to_post(url):
    from django.core.urlresolvers import resolve
    view,_,pieces = resolve(url)
    return Post.objects.get(slug=pieces['slug'], timestamp__year=pieces['year'])
popular.register(Post, '^/blog/[0-9]{4}/', url_to_post)

def feedentry_callback(sender, instance, created, **kwargs):
    if created:
        for sub in instance.feed.subscriptions.all():
            if isinstance(sub.subscriber, Project):
                feed = Feed.objects.get(slug=sub.subscriber.slug)
                feed.items.create(item_type='rss', body=instance.title,
                                  link=instance.link, user=sub.subscriber.lead,
                                  timestamp=instance.date_published)
post_save.connect(feedentry_callback, sender=FeedEntry)

feed, created = Feed.objects.get_or_create(slug='main', defaults={'title':'main feed'})

def event_callback(sender, instance, created, **kwargs):
    if created:
        feed.items.create(user=instance.creator, item_type='event',
                          body=instance.title, link=instance.get_absolute_url())
post_save.connect(event_callback, sender=Event)

def idea_callback(sender, instance, created, **kwargs):
    if created:
        feed.items.create(user=instance.user, item_type='idea',
                          body=unicode(instance),
                          link=instance.get_absolute_url())
post_save.connect(idea_callback, sender=Idea)

def project_callback(sender, instance, created, **kwargs):
    if created:
        feed.items.create(user=instance.lead, item_type='project',
                          body=unicode(instance),
                          link=instance.get_absolute_url())
        Feed.objects.create(slug=instance.slug, title=instance.name)
post_save.connect(project_callback, sender=Project)

def user_callback(sender, instance, created, **kwargs):
    if created:
        feed.items.create(user=instance, item_type='person',
                          body=unicode(instance),
                          link=instance.get_absolute_url())
post_save.connect(user_callback, sender=User)
