from django.contrib import admin
from django.shortcuts import get_object_or_404, render_to_response
from django.conf.urls.defaults import patterns, url
from django.contrib.auth.models import User
from meritbadges.models import Badge, BadgeAward

class AwardInline(admin.TabularInline):
    model = BadgeAward

class BadgeAdmin(admin.ModelAdmin):
    model = Badge
    list_display = ('admin_image_tag',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [AwardInline]

    def assign(self, request, username=None):
        user = get_object_or_404(User, username=username)
        if request.method == 'POST':
            user.badges.clear()     # clear assigned badges
            for slug in request.POST.iterkeys():
                badge = Badge.objects.get(slug=slug)
                BadgeAward.objects.create(user=user, badge=badge)
        badges = Badge.objects.all()
        user_badges = user.badges.values_list('slug', flat=True)
        for badge in badges:
            if badge.slug in user_badges:
                badge.checked = True
        return render_to_response('meritbadges/assign.html',
                                  {'title': 'Assigning Badges to %s' % user,
                                   'badges':badges})

    def user_list(self, request):
        users = User.objects.all().order_by('username')
        return render_to_response('meritbadges/user_list.html',
                                  {'title': 'User List',
                                   'users': users})

    def get_urls(self):
        urls = super(BadgeAdmin, self).get_urls()
        return patterns('',
            url(r'^assign/$', self.admin_site.admin_view(self.user_list), name='badges_user_list'),
            url(r'^assign/(?P<username>\w+)/$', self.admin_site.admin_view(self.assign), name='assign_badges'),
        ) + urls

admin.site.register(Badge, BadgeAdmin)
