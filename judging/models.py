from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from anthill.projects.models import Project

class Rating(models.Model):
    user = models.ForeignKey(User, related_name='ratings')
    project = models.ForeignKey(Project, related_name='ratings')
    rating = models.PositiveIntegerField()
