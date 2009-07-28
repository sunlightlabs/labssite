from django import forms
from django.forms.models import inlineformset_factory
from anthill.projects.models import Project, Link

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['slug', 'name', 'description', 'skills']

LinkFormSet = inlineformset_factory(Project, Link, extra=3)

class JoinProjectForm(forms.Form):
    message = forms.CharField(widget=forms.widgets.Textarea)

