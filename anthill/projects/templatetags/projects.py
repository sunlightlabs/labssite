from django import template
from django.db.models import Count
from anthill.utils import get_items_as_tag, piechart_from_tags
from anthill.projects.models import Project
from newsfeed.models import FeedItem

register = template.Library()

@register.tag
def get_active_projects(parser, token):
    most_active = FeedItem.objects.values_list('feed__slug', flat=True).order_by('count').annotate(count=Count('id'))[:5]
    projects = Project.objects.filter(slug__in=list(most_active))
    return get_items_as_tag(token, projects)

@register.tag
def project_skills_piechart(parser, token):
    return piechart_from_tags(Project, token)
