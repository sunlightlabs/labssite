from blogdor.models import Post
from blogdor.views import archive_index
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from djitter.models import Account
from sunlightlabs.labs.models import Hero, Project
from contact_form.views import contact_form

def index(request):

    account = Account.objects.get(username='jcarbaugh')
    
    featured_projects = Project.objects.filter(is_enabled=True, is_featured=True)
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
    
def projects(request):

    account = Account.objects.get(username='jcarbaugh')
    
    project_dict = {}
    projects = Project.objects.filter(is_enabled=True, type__in=('api','data','os'))
    for project in projects:
        if project.type not in project_dict:
            project_dict[project.type] = []
        project_dict[project.type].append(project)
    
    data = {
        "api_projects": project_dict.get('api', None),
        "data_projects": project_dict.get('data', None),
        "opensource_projects": project_dict.get('os', None),
    }
    
    return render_to_response("labs/projects.html", data)

def contact_sent(request, form_class):
    return contact_form(request, form_class, template_name='contact_form/contact_form_sent.html')
    
def image_wrapper(request, image_path):
    image_path = "%s/images/%s" % (settings.MEDIA_URL, image_path)
    data = {"image_path": image_path}
    return render_to_response("labs/image_wrapper.html", data)