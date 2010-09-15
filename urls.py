from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.gis import admin
from labs.feeds import LabsLatestComments, LabsLatestPosts, LabsLatestForTag, LabsLatestForAuthor
from labs.forms import LabsContactForm
from labs.registration import registration_consumer

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

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        #url(r'^(?P<filename>.*)\.(?P<extension>css|js)$', 'mediasync.views.static'),
    )
