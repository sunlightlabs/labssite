from django import template
from django.template.loader import render_to_string
from newsfeed.models import Feed

register = template.Library()

@register.simple_tag
def render_feed(feed, max_items=5):
    if isinstance(feed, basestring):
        feed = Feed.objects.get(slug=feed)
    results = []
    for item in feed.items.all().select_related()[:max_items]:
        results.append(render_to_string('newsfeed/item.html', {'obj': item}))
    return ' '.join(results)
