from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/(.*)', admin.site.root, name='admin'),
    #url(r'^blog/$', 'sunlightlabs.labs.views.blog', name="blog"),
    url(r'^blog/comments/', include('django.contrib.comments.urls')),
    url(r'^blog/', include('blogdor.urls')),
    url(r'^about/$', 'sunlightlabs.labs.views.about', name="about"),
    url(r'^projects/$', 'sunlightlabs.labs.views.projects', name="projects"),
    url(r'^$', 'sunlightlabs.labs.views.index', name='index'),
)

if (settings.DEBUG):
    urlpatterns += patterns('',
        url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT + "images/"}),
    )