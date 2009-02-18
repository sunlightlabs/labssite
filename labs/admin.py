from django.contrib import admin
from sunlightlabs.labs.models import Hero

class HeroAdmin(admin.ModelAdmin):
    list_display = ['name','location','organization','is_enabled']
    list_display_links = ['name']
    list_filter = ['is_enabled']
    prepopulated_fields = {"slug": ['name']}

admin.site.register(Hero, HeroAdmin)
