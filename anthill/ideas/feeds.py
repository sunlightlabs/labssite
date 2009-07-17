from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from anthill.ideas.models import Idea

class LatestIdeasFeed(Feed):

    description_template = 'ideas/idea_rss_description.html'

    def title(self):
        return 'Latest Ideas'

    def description(self, obj):
        return 'Latest ideas submitted for %s' % obj.name

    def items(self):
        return Idea.objects.order_by('-submit_date')[:30]

    def item_author_name(self, item):
        return item.user

    def item_pubdate(self, item):
        return item.submit_date

