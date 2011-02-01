from django.contrib.syndication import feeds
from django.core.exceptions import ObjectDoesNotExist
from newsfeed.models import Feed, FeedItem

# unfortunately there are three things named feed in this file:
#   feeds.Feed - base django syndication class
#   Feed - newsfeed model representing a 'feed'
#   NewsFeed - syndication class for newsfeed Feeds

class NewsFeed(feeds.Feed):

    title_template = 'newsfeed/feed_title.html'
    description_template = 'newsfeed/item_description.html'

    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Feed.objects.get(slug=bits[0])

    def title(self, obj):
        return unicode(obj)

    link = '/'

    def description(self, obj):
        return unicode(obj)

    def items(self, obj):
        return FeedItem.objects.filter(feed=obj)[:30]

    def item_link(self, item):
        return item.link

    def item_author_name(self, item):
        return item.user.first_name or item.user.username

    def item_pubdate(self, item):
        return item.timestamp

    def item_categories(self, item):
        return (item.item_type,)

