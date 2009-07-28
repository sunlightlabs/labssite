from django import forms
from django.forms.formsets import formset_factory
from anthill.projects.models import Project, Link

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['slug', 'name', 'description', 'skills']

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ['project']
    order = forms.CharField(max_length=3)
LinkFormSet = formset_factory(LinkForm, extra=3, can_delete=True)

class JoinProjectForm(forms.Form):
    message = forms.CharField(widget=forms.widgets.Textarea)

