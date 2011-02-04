from django.db.models.signals import post_save
from django.contrib.comments.models import Comment
from blogdor.models import Post
from newsfeed.models import Feed
#import popular

#def url_to_post(url):
#    from django.core.urlresolvers import resolve
#    view,_,pieces = resolve(url)
#    return Post.objects.get(slug=pieces['slug'], timestamp__year=pieces['year'])
#popular.register(Post, '^/blog/[0-9]{4}/', url_to_post)

feed, created = Feed.objects.get_or_create(slug='main', defaults={'title':'main feed'})

def comment_callback(sender, instance, created, **kwargs):
    if created and instance.user:
        feed.items.create(user=instance.user, item_type='comment',
                          body=unicode(instance.content_object),
                          link=instance.content_object.get_absolute_url())
post_save.connect(comment_callback, sender=Comment)
