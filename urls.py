from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django import forms
from blogdor.feeds import LatestComments, LatestPosts
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
    title = "Sunlight Labs Blog"
    link = "/blog/feeds/latest/"
    description = "Latest blog updates from the nerds at Sunlight Labs"

class LabsLatestComments(LatestComments):
    title = "Sunlight Labs Blog Comments"
    link = "/blog/feeds/comments/"
    description = "Latest comments from the nerds that read the Sunlight Labs blog"
    
blog_feeds = {
    'latest': LabsLatestPosts,
    'comments': LabsLatestComments,
}

urlpatterns = patterns('',
    #url(r'^about/$', 'sunlightlabs.labs.views.about', name="about"),
    url(r'^admin/gatekeeper/', include('gatekeeper.urls')),
    url(r'^admin/(.*)', admin.site.root, name='admin'),
    url(r'^appsforamerica/', include('sunlightlabs.appcontest.urls')),
    url(r'^blog/comments/', include('django.contrib.comments.urls')),
    url(r'^blog/feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': blog_feeds}, name="latest_blog_feed"),
    url(r'^blog/$', 'sunlightlabs.labs.views.blog_wrapper'),
    url(r'^blog/', include('blogdor.urls')),
    url(r'^contact/sent/$', 'sunlightlabs.labs.views.contact_sent', {"form_class": LabsContactForm}),
    url(r'^contact/', include('contact_form.urls'), {"form_class": LabsContactForm, "fail_silently": False}),
    url(r'^contest/$', 'django.views.generic.simple.redirect_to', {'url': '/appsforamerica/'}),
    url(r'^images/(?P<image_path>.*)$', 'sunlightlabs.labs.views.image_wrapper', name="image_wrapper"),
    url(r'^projects/$', 'sunlightlabs.labs.views.projects', name="projects"),
    url(r'^$', 'sunlightlabs.labs.views.index', name='index'),
)

if (settings.DEBUG):
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^(?P<filename>.*)\.(?P<extension>css|js)$', 'sunlightcore.views.static'),
    )