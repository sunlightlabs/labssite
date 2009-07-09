from django import template
from django.template.loaders import select_template
from newsfeed.models import Feed

register = template.Library()

@register.simple_tag
def render_feed(feed):
    if isinstance(feed, str):
        feed = Feed.objects.get(slug=feed)
    results = []
    for item in feed.items.all().select_related():
        template = select_template(('newsfeed/%s.html' % item.item_type.slug,
                                    'newsfeed/item.html'))
        results.append(template.render(Context({'item': item})))
    return ' '.join(results)
