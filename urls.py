from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.gis import admin
from labs.feeds import LabsLatestComments, LabsLatestPosts, LabsLatestForTag, LabsLatestForAuthor
from labs.forms import LabsContactForm
from labs.registration import registration_consumer
from brainstorm.feeds import SubsiteFeed

admin.autodiscover()

blog_feeds = {
    'latest': LabsLatestPosts, 'comments': LabsLatestComments,
    'tag': LabsLatestForTag, 'author': LabsLatestForAuthor,
}

from newsfeed.feeds import NewsFeed
news_feed = { 'newsfeed': NewsFeed }

urlpatterns = patterns('',
    # admin
    url(r'^admin/gatekeeper/', include('gatekeeper.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^comments/', include('django.contrib.comments.urls')),

    # contests
    url(r'^contests/', include('appcontest.urls')),
    url(r'^judgeforamerica/', include('sunlightlabs.appjudging.urls')),
    url(r'^aa2judging/$', 'sunlightlabs.labs.views.aa2_judging', name='aa2_judging'),

    # blog/blogdor
    url(r'^blog/feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': blog_feeds}, name="blogdor_feeds"),
    url(r'^blog/$', 'sunlightlabs.labs.views.blog_wrapper'),
    url(r'^blog/', include('blogdor.urls')),

    # contact-form
    url(r'^contact/sent/$', 'sunlightlabs.labs.views.contact_sent', {"form_class": LabsContactForm}),
    url(r'^contact/', include('contact_form.urls'), {"form_class": LabsContactForm, "fail_silently": False}),

    url(r'^newsfeed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': news_feed}, name="newsfeed_feeds"),

    url(r'^accounts/', include(registration_consumer.urls)),

    # anthill
    url(r'^people/', include('anthill.people.urls')),
    #url(r'^ideas/', include('brainstorm.urls')),
    url(r'^projects/', include('anthill.projects.urls')),
    url(r'^events/', include('anthill.events.urls')),

    # labs specific
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'labs/index.html'}, name='index'),
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
        url(r'^(?P<filename>.*)\.(?P<extension>css|js)$', 'mediasync.views.static'),
    )
