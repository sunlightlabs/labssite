from django import template
from django.conf import settings
from django.db.models import Count
from anthill.utils import get_items_as_tag, piechart_url, piechart_from_tags
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

@register.simple_tag
def people_skills():
    return piechart_from_tags(Profile, {'python':'00aa00', 'ruby':'aa0000'})

@register.simple_tag
def people_roles():
    colors = {'dev': '003300', 'des': '009900', 
              'both': '00cc00', 'other': '00ff00'}
    items = Profile.objects.values('role').annotate(num=Count('id'))
    for item in items:
        item['name'] = name = item.pop('role')
        item['color'] = colors[name]
    return piechart_url(items)

