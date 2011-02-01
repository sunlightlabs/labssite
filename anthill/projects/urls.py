from django.conf.urls.defaults import *

urlpatterns = patterns('anthill.projects.views',
    url(r'^$', 'projects', name='projects'),
    url(r'^all/$', 'archive', name='all_projects'),
    url(r'^official/$', 'archive', {'projects':'official'},
        name='official_projects'),
    url(r'^community/$', 'archive', {'projects':'community'},
        name='community_projects'),
    url(r'^asks/$', 'ask_list', name='all_project_asks'),
    url(r'^tag/(?P<tag>[^/]+)/$', 'tag_archive', name='projects_tagged'),
    url(r'^(?P<slug>[-\w]+)/$', 'project_detail', name='project_detail'),
)
