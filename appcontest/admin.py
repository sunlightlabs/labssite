from django.contrib import admin
from sunlightlabs.appcontest.models import Contest,Entry

class ContestAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class EntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'contest')
    list_filter = ('contest',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Contest, ContestAdmin)
admin.site.register(Entry, EntryAdmin)
