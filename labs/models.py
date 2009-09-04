from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from feedinator.models import FeedEntry
from blogdor.models import Post
from newsfeed.models import Feed
from anthill.events.models import Event
from anthill.projects.models import Project, Role, Ask
from anthill.people.signals import message_sent
from brainstorm.models import Idea
from meritbadges.models import award_badge
import gatekeeper
import popular


gatekeeper.register(Idea, auto_moderator=lambda o: True)
gatekeeper.register(Project, auto_moderator=lambda o: True)

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
noisy, created = Feed.objects.get_or_create(slug='noisy', defaults={'title':'noisy feed'})

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

        # assign badge to lead
        award_badge(instance.lead, 'lead-project')
post_save.connect(project_callback, sender=Project)


def user_callback(sender, instance, created, **kwargs):
    if created:
        feed.items.create(user=instance, item_type='person',
                          body=unicode(instance),
                          link=instance.get_absolute_url())
post_save.connect(user_callback, sender=User)


def message_callback(sender, **kwargs):
    recipient = kwargs['recipient']
    noisy.items.create(user=sender, item_type='message',
                       body=recipient.first_name or recipient.username,
                       link=recipient.get_absolute_url())
message_sent.connect(message_callback)


def role_callback(sender, instance, created, **kwargs):
    if created:
        feed.items.create(user=instance.user, item_type='role',
                          body=unicode(instance.project),
                          link=instance.project.get_absolute_url())
post_save.connect(role_callback, sender=Role)


def ask_callback(sender, instance, created, **kwargs):
    if created:
        feed.items.create(user=instance.user, item_type='ask',
                          body=unicode(instance.project),
                          link=instance.project.get_absolute_url())
post_save.connect(ask_callback, sender=Ask)


def comment_callback(sender, instance, created, **kwargs):
    if created and instance.user:
        feed.items.create(user=instance.user, item_type='comment',
                          body=unicode(instance.content_object),
                          link=instance.content_object.get_absolute_url())
post_save.connect(comment_callback, sender=Comment)
