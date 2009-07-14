from django import template
from django.conf import settings
from anthill.people.models import Profile

register = template.Library()

class SimpleItemsNode(template.Node):
    def __init__(self, queryset, count, offset, varname):
        self.items = queryset[offset:count+offset]
        self.varname = varname

    def render(self, context):
        context[self.varname] = self.items
        return ''

def _simple_get_items(token, queryset):
    pieces = token.contents.split()
    as_index = pieces.index('as')
    if as_index == -1 or as_index > 3 or len(pieces) != as_index+2:
        raise template.TemplateSyntaxError('%r tag must be in format {%% %r [count [offset]] as varname %%}' %
                                          pieces[0])

    # count & offset
    count = 5
    offset = 0
    if as_index > 1:
        count = int(pieces[1])
        if as_index > 2:
            count = int(pieces[2])

    varname = pieces[as_index+1]

    return SimpleItemsNode(queryset, count, offset, varname)

@register.tag
def get_latest_user_profiles(parser, token):
    return _simple_get_items(token, 
         Profile.objects.all().select_related().order_by('-user__date_joined'))

@register.simple_tag
def num_registered_users():
    return Profile.objects.all().count()
