from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response
from django.template import RequestContext
from anthill.projects.models import Project
from anthill.ideas.models import Idea

def projects_and_ideas(request):
    context = {'projects': Project.objects.all()[0:3],
               'ideas': Idea.objects.all()[0:3]}
    return render_to_response('projects/projects_and_ideas.html', context,
                              context_instance=RequestContext(request))

def archive(request):
    return object_list(request, queryset=Project.objects.all(),
                       template_object_name='project', allow_empty=True, 
                       paginate_by=10)

def project_detail(request, slug):
    return object_detail(request, queryset=Project.objects.all(), slug=slug,
                         template_object_name='project')
