from django import template
from django.db.models import get_model
from popular import get_popular_items

register = template.Library()

class ItemsNode(template.Node):
    def __init__(self, items, context_var):
        self.items = items
        self.context_var = context_var

    def render(self, context):
        context[self.context_var] = [x[0] for x in self.items]
        return ''

@register.tag
def get_recently_popular(parser, token):
    '''
        {% get_recently_popular model num_items num_days as context_var %}
    '''
    pieces = token.split_contents()
    tagname = pieces[0]
    as_index = pieces.index('as')

    # check tag structure
    if as_index < 2 or as_index > 4 or len(pieces) != as_index+2:
        raise template.TemplateSyntaxError("Syntax for tag is {%% %s app.Model [num_items] [num_days] as context_var %%}" % tagname)

    # get model from tag
    try:
        label, modelname = pieces[1].split('.')
        model = get_model(label, modelname)
    except Exception as e:
        raise template.TemplateSyntaxError('%s is not a valid app.Model reference' % pieces[1])

    # get num items/days if they were provided
    num_items = 5
    num_days = 7
    if as_index > 2:
        num_items = int(pieces[2])
    if as_index > 3:
        num_days = int(pieces[3])

    items = get_popular_items(model, num_items, num_days)

    varname = pieces[-1]
    return ItemsNode(items, varname)
