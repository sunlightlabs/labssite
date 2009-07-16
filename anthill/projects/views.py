from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from anthill.projects.models import Project, Role
from anthill.projects.forms import ProjectForm, JoinProjectForm
from anthill.ideas.models import Idea
from django.template.loader import render_to_string


def projects_and_ideas(request):
    context = {'projects': Project.objects.select_related().all()[0:3],
               'ideas': Idea.objects.select_related().all()[0:3]}
    return render_to_response('projects/projects_and_ideas.html', context,
                              context_instance=RequestContext(request))

def archive(request):
    return object_list(request,
                       queryset=Project.objects.select_related().all(),
                       template_object_name='project', allow_empty=True,
                       paginate_by=10)

def project_detail(request, slug):
    return object_detail(request,
                         queryset=Project.objects.select_related().all(),
                         slug=slug, template_object_name='project')

@login_required
def join_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'GET':
        form = JoinProjectForm()
    else:
        form = JoinProjectForm(request.POST)
        if form.is_valid():
            if Role.objects.filter(user=request.user, project=project).count():
                request.user.message_set.create(message='You already have a pending request to join this project.')
            else:
                role = Role.objects.create(user=request.user, project=project,
                                           message=form.cleaned_data['message'])

                subject = 'Sunlight Labs: Request to join project %s' % project
                body = render_to_string('projects/join_request_email.txt',
                                        {'role': role})
                project.lead.email_user(subject, body)
                request.user.message_set.create(message='Thank you for submitting your request to join %s' % project)
                return redirect(project.get_absolute_url())

    return render_to_response('projects/join_project.html',
                              {'project':project, 'form':form},
                             context_instance=RequestContext(request))
