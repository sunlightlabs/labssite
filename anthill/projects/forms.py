from django import forms
from anthill.projects.models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['slug', 'name', 'description', 'skills']

class JoinProjectForm(forms.Form):
    message = forms.CharField(widget=forms.widgets.Textarea)

