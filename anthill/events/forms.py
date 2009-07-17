from django import forms
from anthill.events.models import Event

DISTANCE_CHOICES = (
    ('5', '5 Miles'),
    ('25', '25 Miles'),
    ('50', '50 Miles'),
    ('100', '100 Miles'),
)

class SearchForm(forms.Form):
    name = forms.CharField(required=False)
    location = forms.CharField(required=False)
    location_range = forms.ChoiceField(choices=DISTANCE_CHOICES, initial='50',
                                       required=False)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'url', 'start_date', 'end_date']

