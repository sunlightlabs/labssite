import datetime
from django import template
from django.db.models import Count
from anthill.utils import get_items_as_tag
from anthill.projects.models import Project
from newsfeed.models import FeedItem

register = template.Library()

@register.tag
def get_active_projects(parser, token):
    start_time = datetime.datetime.now() - datetime.timedelta(30)  # month ago
    most_active = FeedItem.objects.filter(timestamp__gt=start_time).values_list('feed__slug', flat=True).order_by('count').annotate(count=Count('id'))[:5]
    print most_active
    projects = Project.objects.filter(slug__in=list(most_active))
    if hasattr(projects, '_gatekeeper'):
        projects = projects.approved()
    return get_items_as_tag(token, projects)
