from django.contrib import admin
from anthill.projects.models import Project, Role, Link

class RoleInline(admin.TabularInline):
    model = Role

class LinkInline(admin.TabularInline):
    model = Link

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'official')
    list_filter = ('official',)
    inlines = [LinkInline, RoleInline]

class PublicProjectAdmin(ProjectAdmin):
    exclude = ('official','lead')

    def queryset(self, request):
        return Project.objects.filter(lead=request.user)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if obj:
            return obj.lead == request.user
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        return False

projects_admin = admin.AdminSite(name='projects_admin')
projects_admin.register(Project, PublicProjectAdmin)
