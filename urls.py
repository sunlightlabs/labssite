from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.gis import admin
from django import forms
from blogdor.feeds import LatestComments, LatestPosts, LatestByTag
from contact_form.forms import ContactForm
admin.autodiscover()

class LabsContactForm(ContactForm):

    attrs_dict = { 'class': 'required' }

    from_email = "bounce@sunlightfoundation.com"
    recipient_list = ['swells@sunlightfoundation.com','cjohnson@sunlightfoundation.com','jcarbaugh@sunlightfoundation.com']
    subject = "[SunlightLabs.com] Contact"

    name = forms.CharField(max_length=100,
                widget=forms.TextInput(attrs=attrs_dict),
                label=u'Name')
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=200)),
                label=u'Email Address')
    body = forms.CharField(widget=forms.Textarea(attrs=attrs_dict),
                label=u'Comment')

class LabsLatestPosts(LatestPosts):
    feed_title = "Sunlight Labs blog"
    feed_description = "Latest blog updates from the nerds at Sunlight Labs"

class LabsLatestComments(LatestComments):
    feed_title = "Sunlight Labs blog comments"
    feed_description = "Latest comments from the nerds that read the Sunlight Labs blog"

class LabsLatestByTag(LatestByTag):
    feed_title = "Sunlight Labs loves %s"
    feed_description = "Posts from the Sunlight Labs blog tagged with '%s'"

blog_feeds = {
    'latest': LabsLatestPosts,
    'comments': LabsLatestComments,
    'tag': LabsLatestByTag,
}

urlpatterns = patterns('',
    # admin
    url(r'^admin/gatekeeper/', include('gatekeeper.urls')),
    url(r'^admin/(.*)', admin.site.root, name='admin'),

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

    # users
    url(r'^accounts/', include('registration.urls')),
    url(r'^users/', include('anthill.people.urls')),

    url(r'^ideas/', include('anthill.ideas.urls')),
    url(r'^projects/', include('showcase.urls')),

    # labs specific
    url(r'^$', 'sunlightlabs.labs.views.index', name='index'),
)

#
# redirects
#

urlpatterns += patterns('django.views.generic.simple',
    url(r'^research/familybusiness/$', 'redirect_to', {'url': 'http://research.sunlightprojects.org/research/familybusiness/'}),
    url(r'^research/sites/$', 'redirect_to', {'url': 'http://research.sunlightprojects.org/research/sites/'}),
    url(r'^visualizingearmarks/$', 'redirect_to', {'url': 'http://research.sunlightprojects.org/visualizingearmarks'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^(?P<filename>.*)\.(?P<extension>css|js)$', 'mediasync.views.static'),
    )
