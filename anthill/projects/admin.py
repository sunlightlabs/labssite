from django.contrib import admin
from anthill.projects.models import Project, Role

class RoleInline(admin.TabularInline):
    model = Role


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'official')
    list_filter = ('official',)
    inlines = [RoleInline]

admin.site.register(Project, ProjectAdmin)
