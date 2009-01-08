from django.conf import settings
from django.template.loader import render_to_string
from django import template
from sunlightlabs.appcontest.models import Entry
import gatekeeper

register = template.Library()

@register.simple_tag
def recent_apps(count=5):
    apps = gatekeeper.approved(Entry.objects.all())[:count]
    return render_to_string('appcontest/tags/app_list.html', {'apps': apps})