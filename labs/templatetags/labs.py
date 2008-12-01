from django.conf import settings
from django.template.loader import render_to_string
from djitter.models import Account
from django import template

register = template.Library()

@register.simple_tag
def recent_tweets(count=5):
    account = Account.objects.get(username='sunlightlabs')
    dms = account.direct_messages().filter(sender__username__in=settings.ALLOWED_TO_DM)[:count]
    return render_to_string('labs/sidebar_tweets.html', {'dms': dms})