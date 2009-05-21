from django.contrib import admin
from sunlightlabs.appcontest.models import Contest,Entry

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Contest, EntryAdmin)
admin.site.register(Entry, EntryAdmin)
