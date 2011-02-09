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

    url(r'^accounts/', include(registration_consumer.urls)),

    url(r'^people/(?P<username>\w+)/$', 'labssite.labs.views.profile_redirect',
        name='user_profile'),

    # anthill
    url(r'^projects/', include('anthill.projects.urls')),

    # redirects
    url(r'^events/', 'django.views.generic.simple.redirect_to',
        {'url': 'http://meetup.com/sunlightfoundation/'}),
    url(r'^api/', 'django.views.generic.simple.redirect_to',
        {'url': 'http://services.sunlightlabs.com/api/'}),
    url(r'^people/', 'django.views.generic.simple.redirect_to',
        {'url': '/about/'}),
    url(r'^projects/all/', 'django.views.generic.simple.redirect_to',
        {'url': '/projects/'}),
    url(r'^projects/official/', 'django.views.generic.simple.redirect_to',
        {'url': '/projects/'}),
    url(r'^projects/community/', 'django.views.generic.simple.redirect_to',
        {'url': '/projects/'}),

    # markupwiki
    url(r'^wiki/', include('markupwiki.urls')),

    # labs specific
    url(r'^photobooth/$', 'django.views.generic.simple.redirect_to',
        {'url': 'http://www.flickr.com/photos/sunlightfoundation/sets/72157624999270674/'}),
    url(r'^$', 'labssite.labs.views.index', name='index'),

    url(r'^d4a_entry/$', 'labssite.labs.views.sponsor_iframe'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        #url(r'^(?P<filename>.*)\.(?P<extension>css|js)$', 'mediasync.views.static'),
    )
