from django.conf import settings
from django.template.loader import render_to_string
from django import template
from sunlightlabs.appcontest.models import Contest,Entry

register = template.Library()

@register.simple_tag
def recent_apps(contest, count=5):
    apps = contest.entries.all().approved()[:count]
    return render_to_string('appcontest/tags/app_list.html', {'contest':contest,
                                                              'apps': apps})
