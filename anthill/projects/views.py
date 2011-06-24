from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from django.template import RequestContext
from django.template.loader import render_to_string
from tagging.views import tagged_object_list
from anthill.projects.models import Project, Role, Ask

def tag_archive(request, tag):
    """
        Paginated listing of ``Project``s by tag.

        Template: projects/projects_list.html

        Context:
            tag          - tag being displayed
            project_list - list of projects

            See ``django.views.generic.list_detail.object_list`` for pagination variables.
    """
    qs = Project.objects.select_related()
    if hasattr(qs, '_gatekeeper'):
        qs = qs.approved()
    return tagged_object_list(request, qs, tag, paginate_by=10,
                              template_object_name='project',
                              extra_context={'tag':tag},
                              allow_empty=True)

def project_detail(request, slug):
    """
        Detail view of a ``Project``.

        Template: projects/project_detail.html

        Context:
            project - ``Project`` instance
    """
    # explicitly don't use _gatekeeper check here
    return object_detail(request,
                         queryset=Project.objects.select_related().all(),
                         slug=slug, template_object_name='project')
