from django import template
from django.template.loader import select_template
from django.template.context import Context
from newsfeed.models import Feed

register = template.Library()

@register.simple_tag
def render_feed(feed, max_items=5):
    if isinstance(feed, basestring):
        feed = Feed.objects.get(slug=feed)
    results = []
    for item in feed.items.all().select_related()[:max_items]:
        template = select_template(('newsfeed/%s.html' % item.item_type,
                                    'newsfeed/item.html'))
        results.append(template.render(Context({'item': item})))
    return ' '.join(results)
