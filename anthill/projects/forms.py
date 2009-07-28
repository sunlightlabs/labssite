from django import forms
from django.forms.models import inlineformset_factory
from anthill.projects.models import Project, Link, Role

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['slug', 'name', 'description', 'skills']

LinkFormSet = inlineformset_factory(Project, Link, extra=3)
RoleFormSet = inlineformset_factory(Project, Role, extra=0, fields=['status'], can_delete=False)

class JoinProjectForm(forms.Form):
    message = forms.CharField(widget=forms.widgets.Textarea)

