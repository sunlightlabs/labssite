from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django import forms
from blogdor.feeds import LatestPosts
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

blog_feeds = {
    'latest': LabsLatestPosts,
}

urlpatterns = patterns('',
    #url(r'^about/$', 'sunlightlabs.labs.views.about', name="about"),
    url(r'^admin/(.*)', admin.site.root, name='admin'),
    url(r'^blog/comments/', include('django.contrib.comments.urls')),
    url(r'^blog/feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': blog_feeds}),
    url(r'^blog/', include('blogdor.urls')),
    url(r'^contact/', include('contact_form.urls'), {"form_class": LabsContactForm, "fail_silently": False}),
    url(r'^projects/$', 'sunlightlabs.labs.views.projects', name="projects"),
    url(r'^$', 'sunlightlabs.labs.views.index', name='index'),
)

if (settings.DEBUG):
    urlpatterns += patterns('',
        url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT + "images/"}),
        url(r'^(?P<filename>.*)\.(?P<extension>css|js)$', 'sunlightcore.views.static'),
    )