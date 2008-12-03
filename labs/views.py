from blogdor.models import Post
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from djitter.models import Account
from sunlightlabs.labs.models import Hero, Project

def index(request):

    account = Account.objects.get(username='jcarbaugh')
    
    featured_projects = Project.objects.filter(is_enabled=True, is_featured=True)
    recent_posts = Post.objects.public()[:3]
    
    data = {
        "featured_projects": featured_projects,
        "recent_posts": recent_posts,
    }
    return render_to_response("labs/index.html", data)

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

def blog(request):
    return render_to_response("labs/blog.html")