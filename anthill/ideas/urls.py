from django.conf.urls.defaults import *
from django.contrib.contenttypes.models import ContentType
from anthill.ideas.models import Idea
from anthill.ideas.feeds import IdeaFeed

feeds = {
    'latest': IdeaFeed,
}

# feeds live at rss/latest/site-name/
urlpatterns = patterns('',
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}),
)

urlpatterns += patterns('anthill.ideas.views',
    url(r'^$', 'idea_list', {'ordering': 'most_popular'}, name='ideas_popular'),
    url(r'^latest/$', 'idea_list', {'ordering': 'latest'}, name='ideas_latest'),
    url(r'^(?P<id>\d+)/$', 'idea_detail', name='idea_detail'),
    url(r'^new_idea/$', 'new_idea', name='new_idea'),
    url(r'^vote/$', 'vote', name='idea_vote'),
)

