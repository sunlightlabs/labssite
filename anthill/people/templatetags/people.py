from django import template
from django.conf import settings
from anthill.utils import get_items_as_tag
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
