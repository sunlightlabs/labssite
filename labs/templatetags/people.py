from django import template

register = template.Library()

@register.simple_tag
def display_name(user):
    return user.first_name or user.username

