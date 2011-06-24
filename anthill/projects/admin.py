from django.contrib import admin
from django.contrib.contenttypes import generic
from anthill.projects.models import Project, Role, Link

class RoleInline(admin.TabularInline):
    model = Role

class LinkInline(admin.TabularInline):
    model = Link

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'official')
    list_filter = ('official',)
    inlines = [LinkInline, RoleInline]

admin.site.register(Project, ProjectAdmin)
