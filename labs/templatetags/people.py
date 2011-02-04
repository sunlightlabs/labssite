from django import template
from django.conf import settings
from django.db.models import Count
from anthill.utils import get_items_as_tag, chart_from_tags, _extract_chart_params, ChartNode

register = template.Library()


@register.simple_tag
def display_name(user):
    return user.first_name or user.username

