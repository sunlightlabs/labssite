import urllib2
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.flatpages.models import FlatPage
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.core.cache import cache
from labs.forms import LabsContactForm
from blogdor.models import Post
from blogdor.views import archive
from anthill.projects.models import Project

def index(request):
    try:
        fpage = FlatPage.objects.get(url='alertbox-content')
        box = fpage.content.strip()
    except FlatPage.DoesNotExist:
        box = ''
    return render_to_response("labs/index.html", {'alertbox': box},
                             context_instance=RequestContext(request))


def contact_form(request):

    recipient_list = ['swells@sunlightfoundation.com','tlee@sunlightfoundation.com','jcarbaugh@sunlightfoundation.com', 'jturk@sunlightfoundation.com']
    subject = "[SunlightLabs.com] Contact"

    if request.method == 'POST':
        form = LabsContactForm(request.POST)
        if form.is_valid():
            message = render_to_string('labs/contact_email.txt',
                                       form.cleaned_data)
            send_mail(subject, message, form.cleaned_data['email'],
                      recipient_list, fail_silently=False)

            # use a message for success
            messages.success(request, 'Your message has been sent, thank you for your email.')
            form = LabsContactForm()
    else:
        if not request.user.is_anonymous():
            form = LabsContactForm(initial={'email':request.user.email})
        else:
            form = LabsContactForm()

    return render_to_response('labs/contact_form.html', {'form': form},
                              context_instance=RequestContext(request))

def image_wrapper(request, image_path):
    image_path = "images/%s" % image_path
    data = {"image_path": image_path}
    return render_to_response("labs/image_wrapper.html", data)

def sponsor_iframe(request):
    return render_to_response("labs/sponsor_iframe.html", {'url': request.GET['url']})

def profile_redirect(request, username):
    return redirect('/blog/author/%s/' % username)
