from django.contrib.syndication import feeds
from anthill.ideas.models import Idea

class IdeaFeed(feeds.Feed):

    title = 'Latest Ideas'
    description = 'Latest Ideas'
    link = '/ideas/'

    title_template = 'ideas/feed_title.html'
    description_template = 'ideas/feed_description.html'

    def items(self):
        return Idea.objects.order_by('-submit_date')[:30]

    def item_link(self, item):
        return item.get_absolute_url()

    def item_author_name(self, item):
        return item.user

    def item_pubdate(self, item):
        return item.submit_date

