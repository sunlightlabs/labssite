from django.contrib import admin
from anthill.projects.models import Project
from anthill.projects.projects_admin import ProjectAdmin

admin.site.register(Project, ProjectAdmin)
