from django import template
from django.db.models import Q
from django.template.loader import render_to_string
from anthill.events.models import Event
import datetime

register = template.Library()

@register.simple_tag
def hackathon_events():
    events = Event.objects.filter(
                start_date__gte=datetime.datetime(2009, 12, 12, 0, 0, 0),
                start_date__lte=datetime.datetime(2009, 12, 13, 23, 59, 59)).order_by('-official', 'title')
    return render_to_string("labs/hackathon_events.html", {"event_list": events})