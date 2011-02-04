from django.conf.urls.defaults import *

urlpatterns = patterns('anthill.projects.views',
    url(r'^tag/(?P<tag>[^/]+)/$', 'tag_archive', name='projects_tagged'),
    url(r'^(?P<slug>[-\w]+)/$', 'project_detail', name='project_detail'),
)
