from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from blogdor.models import Post
from labs.feeds import LabsLatestPosts, LabsLatestForTag, LabsLatestForAuthor
from labs.forms import LabsContactForm

admin.autodiscover()

blog_feeds = {
    'latest_fburner': LabsLatestPosts,
    'tag': LabsLatestForTag,
    'author': LabsLatestForAuthor,
}


def thegreatredirector(request, year, slug):
    post = get_object_or_404(Post.objects.published(), date_published__year=year, slug=slug)
    date_str = post.date_published.strftime("%Y/%m/%d")
    url = "http://sunlightfoundation.com/blog/%s/%s" % (date_str, post.slug)
    return HttpResponsePermanentRedirect(url)


urlpatterns = patterns('',
    # apps
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', include('haystack.urls')),
    url(r'^projects/', include('anthill.projects.urls')),
    url(r'^wiki/', include('markupwiki.urls')),

    # blog/blogdor
    url(r'^blog/feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': blog_feeds}, name="blogdor_feeds"),
    # url(r'^blog/(?P<year>\d{4})/(?P<slug>[\w-]+)/$', thegreatredirector),
    url(r'^blog/', include('blogdor.urls')),

    # contact form
    url(r'^contact/$', 'labs.views.contact_form', name='contact_form'),

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

    # labs specific
    url(r'^images/(?P<image_path>.*)$', 'labs.views.image_wrapper',
        name="image_wrapper"),
    url(r'^photobooth/$', 'django.views.generic.simple.redirect_to',
        {'url': 'http://www.flickr.com/photos/sunlightfoundation/sets/72157632180391380/'}),
    url(r'^people/(?P<username>\w+)/$', 'labs.views.profile_redirect',
        name='user_profile'),
    url(r'^$', 'labs.views.index', name='index'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
