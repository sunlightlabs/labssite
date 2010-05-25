from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.gis import admin
from labs.feeds import LabsLatestComments, LabsLatestPosts, LabsLatestForTag, LabsLatestForAuthor
from labs.forms import LabsContactForm
from labs.registration import registration_consumer
from brainstorm.feeds import SubsiteFeed

admin.autodiscover()

blog_feeds = {
    'latest_fburner': LabsLatestPosts,
    'comments': LabsLatestComments,
    'tag': LabsLatestForTag,
    'author': LabsLatestForAuthor,
}

from newsfeed.feeds import NewsFeed
news_feed = {
    'newsfeed': NewsFeed
}

urlpatterns = patterns('',
    # admin
    url(r'^admin/', include(admin.site.urls)),

    url(r'^search/', include('haystack.urls')),

    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^images/(?P<image_path>.*)$', 'labssite.labs.views.image_wrapper', name="image_wrapper"),

    # blog/blogdor
    url(r'^blog/feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': blog_feeds}, name="blogdor_feeds"),
    url(r'^blog/$', 'labssite.labs.views.blog_wrapper'),
    url(r'^blog/', include('blogdor.urls')),

    # contact form
    url(r'^contact/$', 'labssite.labs.views.contact_form', name='contact_form'),

    url(r'^newsfeed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': news_feed}, name="newsfeed_feeds"),

    url(r'^accounts/', include(registration_consumer.urls)),

    # anthill
    url(r'^people/', include('anthill.people.urls')),
    url(r'^projects/', include('anthill.projects.urls')),
    url(r'^events/', include('anthill.events.urls')),

    # labs specific
    url(r'^$', 'labssite.labs.views.index', name='index'),

    url(r'^d4a_entry/$', 'labssite.labs.views.sponsor_iframe'),
)

# brainstorm - custom urls so slug isn't needed
urlpatterns += patterns('brainstorm.views',
    url(r'^ideas/$', 'idea_list', {'ordering': 'most_popular', 'slug':'ideas'}, name='ideas_popular'),
    url(r'^ideas/latest/$', 'idea_list', {'ordering': 'latest', 'slug': 'ideas'}, name='ideas_latest'),
    url(r'^ideas/(?P<id>\d+)/$', 'idea_detail', {'slug': 'ideas'}, name='idea_detail'),
    url(r'^ideas/new_idea/$', 'new_idea', {'slug': 'ideas'}, name='new_idea'),
    url(r'^ideas/vote/$', 'vote', name='idea_vote'),
)
urlpatterns += patterns('',
    url(r'^ideas/feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': {'latest': SubsiteFeed}}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        #url(r'^(?P<filename>.*)\.(?P<extension>css|js)$', 'mediasync.views.static'),
    )
