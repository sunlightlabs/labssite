from django.contrib import admin
from sunlightlabs.appcontest.models import Entry, Vote

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Entry, EntryAdmin)
admin.site.register(Vote)