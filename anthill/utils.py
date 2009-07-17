from django import template

class SimpleItemsNode(template.Node):
    def __init__(self, queryset, count, offset, varname):
        self.items = queryset[offset:count+offset]
        self.varname = varname

    def render(self, context):
        context[self.varname] = self.items
        return ''

def get_items_as_tag(token, queryset, count=5):
    pieces = token.contents.split()
    as_index = pieces.index('as')
    if as_index == -1 or as_index > 3 or len(pieces) != as_index+2:
        raise template.TemplateSyntaxError('%r tag must be in format {%% %r [count [offset]] as varname %%}' %
                                          pieces[0])

    # count & offset
    offset = 0
    if as_index > 1:
        count = int(pieces[1])
        if as_index > 2:
            count = int(pieces[2])

    varname = pieces[as_index+1]

    return SimpleItemsNode(queryset, count, offset, varname)
