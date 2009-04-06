from blogdor.models import Post
from blogdor.views import archive_index
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from djitter.models import Account
from sunlightlabs.labs.models import Hero
from contact_form.views import contact_form
from showcase.models import Project, FEATURED

def index(request):

    account = Account.objects.get(username='jcarbaugh')
    
    featured_projects = Project.objects.filter(status=FEATURED)
    recent_posts = Post.objects.public()[:2]
    
    data = {
        "featured_projects": featured_projects,
        "recent_posts": recent_posts,
    }
    
    return render_to_response("labs/index.html", data)
    
def blog_wrapper(request):
    if 'feed' in request.GET:
        return HttpResponseRedirect('/blog/feeds/latest')
    return archive_index(request)
    
def contact_sent(request, form_class):
    return contact_form(request, form_class, template_name='contact_form/contact_form_sent.html')
    
def image_wrapper(request, image_path):
    image_path = "images/%s" % image_path
    data = {"image_path": image_path}
    return render_to_response("labs/image_wrapper.html", data)
