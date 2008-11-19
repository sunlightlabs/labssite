from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from blogdor.feeds import LatestPosts

admin.autodiscover()

class LabsLatestPosts(LatestPosts):
    title = "Sunlight Labs Blog"
    link = "/blog/feeds/latest/"
    description = "Latest blog updates from the nerds at Sunlight Labs"

blog_feeds = {
    'latest': LabsLatestPosts,
}

urlpatterns = patterns('',
    url(r'^about/$', 'sunlightlabs.labs.views.about', name="about"),
    url(r'^admin/(.*)', admin.site.root, name='admin'),
    url(r'^blog/comments/', include('django.contrib.comments.urls')),
    url(r'^blog/feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': blog_feeds}),
    url(r'^blog/', include('blogdor.urls')),
    url(r'^projects/$', 'sunlightlabs.labs.views.projects', name="projects"),
    url(r'^$', 'sunlightlabs.labs.views.index', name='index'),
)

if (settings.DEBUG):
    urlpatterns += patterns('',
        url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT + "images/"}),
    )