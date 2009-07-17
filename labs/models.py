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
