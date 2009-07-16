from django.conf.urls.defaults import *

urlpatterns = patterns('anthill.projects.views',
    url(r'^$', 'projects_and_ideas', name='projects_and_ideas'),
    url(r'^all/$', 'archive', name='projects_archive'),
    url(r'^(?P<slug>[-\w]+)/$', 'project_detail', name='project_detail'),
    url(r'^(?P<slug>[-\w]+)/join/$', 'join_project', name='join_project'),
)
