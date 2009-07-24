from django import template
from django.conf import settings
from django.db.models import Count
from anthill.utils import get_items_as_tag, piechart_from_tags, PiechartNode
from anthill.people.models import Profile

register = template.Library()

@register.tag
def get_latest_user_profiles(parser, token):
    return get_items_as_tag(token,
         Profile.objects.all().select_related().order_by('-user__date_joined'))

@register.simple_tag
def display_name(user):
    return user.first_name or user.username

@register.simple_tag
def possessive(user):
    name = user.first_name or user.username
    if name[-1] == 's':
        name = ''.join((name, "'"))
    else:
        name = ''.join((name, "'s"))
    return name

@register.simple_tag
def num_registered_users():
    return Profile.objects.all().count()

@register.tag
def people_skills(parser, token):
    pieces = token.contents.split(None)
    args = pieces[1:]
    tags = dict(arg.split(':') for arg in args)
    return piechart_from_tags(Profile, tags)

@register.tag
def people_roles(parser, token):
    pieces = token.contents.split(None)
    args = pieces[1:]
    colors = dict(arg.split(':') for arg in args)
    items = Profile.objects.filter(role__in=colors.keys()).values('role').annotate(num=Count('id'))
    for item in items:
        item['name'] = name = item.pop('role')
        item['color'] = colors[name]
    return PiechartNode(items)

