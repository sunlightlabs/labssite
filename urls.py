from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.gis import admin
from labs.feeds import LabsLatestComments, LabsLatestPosts, LabsLatestForTag, LabsLatestForAuthor
from labs.forms import LabsContactForm
from labs.registration import registration_consumer

admin.autodiscover()

blog_feeds = {
    'latest': LabsLatestPosts, 'comments': LabsLatestComments,
    'tag': LabsLatestForTag, 'author': LabsLatestForAuthor,
}

urlpatterns = patterns('',
    # admin
    url(r'^admin/gatekeeper/', include('gatekeeper.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^comments/', include('django.contrib.comments.urls')),

    # contests
    url(r'^contests/', include('sunlightlabs.appcontest.urls')),
    url(r'^judgeforamerica/', include('sunlightlabs.appjudging.urls')),

    # blog/blogdor
    url(r'^blog/feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': blog_feeds}, name="blogdor_feeds"),
    url(r'^blog/$', 'sunlightlabs.labs.views.blog_wrapper'),
    url(r'^blog/', include('blogdor.urls')),

    # contact-form
    url(r'^contact/sent/$', 'sunlightlabs.labs.views.contact_sent', {"form_class": LabsContactForm}),
    url(r'^contact/', include('contact_form.urls'), {"form_class": LabsContactForm, "fail_silently": False}),

    url(r'^accounts/', include(registration_consumer.urls)),

    # anthill
    url(r'^people/', include('anthill.people.urls')),
    url(r'^ideas/', include('anthill.ideas.urls')),
    url(r'^projects/', include('anthill.projects.urls')),
    url(r'^events/', include('anthill.events.urls')),

    # labs specific
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'labs/index.html'}, name='index'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^(?P<filename>.*)\.(?P<extension>css|js)$', 'mediasync.views.static'),
    )
