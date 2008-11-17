from django.contrib import admin
from sunlightlabs.labs.models import Hero, Project

class HeroAdmin(admin.ModelAdmin):
    list_display = ['name','location','organization','is_enabled']
    list_display_links = ['name']
    list_filter = ['is_enabled']
    prepopulated_fields = {"slug": ['name']}

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name','type','is_enabled','is_featured']
    list_display_links = ['name']
    list_filter = ['type','is_enabled']

admin.site.register(Hero, HeroAdmin)
admin.site.register(Project, ProjectAdmin)