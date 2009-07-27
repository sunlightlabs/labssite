from blogdor.models import Post
import popular

def url_to_post(url):
    from django.core.urlresolvers import resolve
    view,_,pieces = resolve(url)
    return Post.objects.get(slug=pieces['slug'], timestamp__year=pieces['year'])
popular.register(Post, '^/blog/[0-9]{4}/', url_to_post)

from django.db.models.signals import post_save
from feedinator.models import FeedEntry
from newsfeed.models import Feed
from anthill.projects.models import Project
def feedentry_callback(sender, instance, created, **kwargs):
    if created:
        for sub in instance.feed.subscriptions.all():
            if isinstance(sub.subscriber, Project):
                feed = Feed.objects.get(slug=sub.subscriber.slug)
                feed.items.create(item_type='rss', body=instance.title,
                                  link=instance.link, user=sub.subscriber.lead,
                                  timestamp=instance.date_published)
post_save.connect(feedentry_callback, sender=FeedEntry)
