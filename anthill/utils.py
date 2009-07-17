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


## google charts ##

def _piechart_url(items, width=200, height=200):
    nums = []
    names = []
    colors = []
    for item in items:
        nums.append(item['num'])
        names.append(item['name'])
        colors.append(item['color'])

    chart_data = {'width': width, 'height': height, 'nums':','.join(nums),
                  'names':'|'.join(names), 'colors':'|'.join(colors)}

    return 'http://chart.apis.google.com/chart?cht=p&chd=t:%(nums)s&chs=%(width)dx%(height)d&chl=%(names)s&chco=%(colors)s' % chart_data

def _piechart_from_tags(model, tags, width=200, height=200):
    ct = ContentType.objects.get_for_model(model).id
    tag_names = tags.items()
    items = Tag.objects.filter(items__content_type=ct, name__in=tag_names).values('name').annotate(num=Count('id'))
    for item in items:
        item['color'] = items[item['name']]
    return _piechart_url(items, width, height)
