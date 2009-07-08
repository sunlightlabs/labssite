from django import forms
from anthill.people.models import ROLES

DISTANCE_CHOICES = (
    ('1', '1 Mile'),
    ('5', '5 Miles'),
    ('10', '10 Miles'),
    ('25', '25 Miles'),
    ('50', '50 Miles'),
    ('100', '100 Miles'),
)

class SearchForm(forms.Form):
    location = forms.CharField()
    name = forms.CharField(required=False)
    position = forms.ChoiceField(label='Position', choices=ROLES,
                                 required=False)
    location_range = forms.ChoiceField(choices=DISTANCE_CHOICES)

class ProfileForm(forms.Form):
    name = forms.CharField(label='Name', required=False)
    email = forms.CharField(label='Email')
    photo = forms.ImageField(label='Avatar', required=False)
    url = forms.URLField(label='Personal URL', required=False)
    position = forms.ChoiceField(label='Position', choices=ROLES)
    location = forms.CharField(label='Location', required=False)
    skills = forms.CharField(label='Skills', required=False)
    about = forms.CharField(widget=forms.widgets.Textarea, label='About You', required=False)
