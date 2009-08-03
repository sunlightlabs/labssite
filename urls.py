from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.gis import admin
from django import forms
from blogdor.feeds import LatestComments, LatestPosts, LatestForTag, LatestForAuthor
from contact_form.forms import ContactForm

admin.autodiscover()

### openid ###
from django_openid.registration import RegistrationConsumer
from django_openid.forms import RegistrationFormPasswordConfirm

class RegistrationForm(RegistrationFormPasswordConfirm):
    extra_required = ('email',)

class CustomRegistrationConsumer(RegistrationConsumer):
    confirm_email_addresses = False
    RegistrationForm = RegistrationForm
    after_registration_url = '/users/edit_profile/'

registration_consumer = CustomRegistrationConsumer()


### newsfeed ###
from newsfeed.models import Feed
from django.db.models.signals import post_save
from anthill.events.models import Event
from anthill.projects.models import Project
from anthill.ideas.models import Idea
from django.contrib.auth.models import User
feed, created = Feed.objects.get_or_create(slug='main', 
                                           defaults={'title':'main feed'})

def event_callback(sender, instance, created, **kwargs):
    if created:
        feed.items.create(user=instance.creator, item_type='event',
                          body=instance.title, link=instance.get_absolute_url())
post_save.connect(event_callback, sender=Event)

def idea_callback(sender, instance, created, **kwargs):
    if created:
        feed.items.create(user=instance.user, item_type='idea',
                          body=unicode(instance),
                          link=instance.get_absolute_url())
post_save.connect(idea_callback, sender=Idea)

def project_callback(sender, instance, created, **kwargs):
    if created:
        feed.items.create(user=instance.lead, item_type='project',
                          body=unicode(instance),
                          link=instance.get_absolute_url())
        Feed.objects.create(slug=instance.slug, title=instance.name)
post_save.connect(project_callback, sender=Project)

def user_callback(sender, instance, created, **kwargs):
    if created:
        feed.items.create(user=instance, item_type='person',
                          body=unicode(instance),
                          link=instance.get_absolute_url())
post_save.connect(user_callback, sender=User)


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

class LabsLatestForTag(LatestForTag):
    feed_title = "Sunlight Labs loves %s"
    feed_description = "Posts from the Sunlight Labs blog tagged with '%s'"

class LabsLatestForAuthor(LatestForAuthor):
    feed_title = "Sunlight Labs' %s"
    feed_description = "Posts written by %s for the Sunlight Labs blog"

blog_feeds = {
    'latest': LabsLatestPosts,
    'comments': LabsLatestComments,
    'tag': LabsLatestForTag,
    'author': LabsLatestForAuthor,
}

urlpatterns = patterns('',
    # admin
    url(r'^admin/gatekeeper/', include('gatekeeper.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^openid/', include(registration_consumer.urls)),

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
    url(r'^projects/', include('anthill.projects.urls')),
    url(r'^events/', include('anthill.events.urls')),

    # labs specific
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'labs/index.html'}, name='index'),
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
