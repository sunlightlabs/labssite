from django.conf.urls.defaults import *

urlpatterns = patterns('anthill.projects.views',
    url(r'^$', 'projects_and_ideas', name='projects_and_ideas'),
    url(r'^all/$', 'archive', name='projects_archive'),
    url(r'^new/$', 'new_project', name='new_project'),
    url(r'^tag/(?P<tag>[^/]+)/$', 'tag_archive', name='projects_tagged'),
    url(r'^(?P<slug>[-\w]+)/$', 'project_detail', name='project_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', 'edit_project', name='edit_project'),
    url(r'^(?P<slug>[-\w]+)/join/$', 'join_project', name='join_project'),
)
