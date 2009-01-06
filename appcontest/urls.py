from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^apps/(?P<slug>.*)/$', 'sunlightlabs.appcontest.views.app_detail', name='appcontest_app_detail'),
    url(r'^apps/$', 'sunlightlabs.appcontest.views.app_list', name='appcontest_app_list'),
    url(r'^submit/$', 'sunlightlabs.appcontest.views.submit', name='appcontest_submit'),
    #url(r'^$', 'sunlightlabs.appcontest.views.index', name='appcontest_index'),
)