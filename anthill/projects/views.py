from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.template import RequestContext
from django.template.loader import render_to_string
from tagging.views import tagged_object_list
from anthill.projects.models import Project, Role
from anthill.projects.forms import ProjectForm, LinkFormSet, RoleFormSet, FeedFormSet, JoinProjectForm
from anthill.ideas.models import Idea
from feedinator.models import Feed

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

def tag_archive(request, tag):
    return tagged_object_list(request,
                              Project.objects.select_related(),
                              tag,
                              paginate_by=10,
                              template_object_name='project',
                              extra_context={'tag':tag},
                              allow_empty=True)

def project_detail(request, slug):
    return object_detail(request,
                         queryset=Project.objects.select_related().all(),
                         slug=slug, template_object_name='project')

@login_required
def new_project(request):
    if request.method == 'GET':
        project_form = ProjectForm()
    else:
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.lead = request.user
            project.save()
            request.user.message_set.create(message='Your project has been created.')
            return redirect('edit_project', project.slug)
    return render_to_response('projects/new_project.html',
                              {'project_form':project_form},
                              context_instance=RequestContext(request))

@login_required
def edit_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.user != project.lead and not request.user.is_staff:
        return HttpResponseForbidden('Only the project lead can edit a project.')

    if request.method == 'GET':
        project_form = ProjectForm(instance=project)
        link_formset = LinkFormSet(instance=project, prefix='links')
        role_formset = RoleFormSet(instance=project, prefix='roles')
        feed_data = [{'id':s.feed.id, 'title':s.feed.title, 'url':s.feed.url}
                     for s in project.subscriptions.all()]
        feed_formset = FeedFormSet(prefix='feeds', initial=feed_data)
    else:
        project_form = ProjectForm(request.POST, instance=project)
        link_formset = LinkFormSet(request.POST, instance=project, prefix='links')
        role_formset = RoleFormSet(request.POST, instance=project, prefix='roles')
        feed_formset = FeedFormSet(request.POST, prefix='feeds')

        # only save if the main form + all three formsets validate
        if (project_form.is_valid() and link_formset.is_valid() 
            and role_formset.is_valid() and feed_formset.is_valid()):

            # three simple saves do so much
            project_form.save()
            link_formset.save()
            role_formset.save()

            # update or create feeds
            for form in feed_formset.forms:
                data = dict(form.cleaned_data)
                if data and not data['DELETE']:
                    feed_id = data.pop('id')
                    data.pop('DELETE')
                    if feed_id:
                        Feed.objects.filter(pk=feed_id).update(**data)
                    else:
                        feed = Feed.objects.create(**data)
                        project.subscriptions.create(feed=feed)

            # delete feeds in deleted_forms
            del_ids = [f.cleaned_data['id'] for f in feed_formset.deleted_forms]
            Feed.objects.filter(pk__in=del_ids).delete()

            request.user.message_set.create(message='Your changes have been saved.')
            return redirect(project)

    # display on GET or failed POST
    return render_to_response('projects/edit_project.html',
                              {'project':project, 'project_form':project_form,
                               'role_formset': role_formset,
                               'link_formset': link_formset,
                               'feed_formset': feed_formset,},
                              context_instance=RequestContext(request))

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
                                        {'project': project, 'role': role})
                project.lead.email_user(subject, body)
                request.user.message_set.create(message='Thank you for submitting your request to join %s' % project)
                return redirect(project.get_absolute_url())

    return render_to_response('projects/join_project.html',
                              {'project':project, 'form':form},
                             context_instance=RequestContext(request))
