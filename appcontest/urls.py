from django.conf.urls.defaults import *

urlpatterns = patterns('sunlightlabs.appcontest.views',
    url(r'^(?P<contest>.*)/apps/(?P<slug>.*)/$', 'app_detail', name='appcontest_app_detail'),
    url(r'^(?P<contest>.*)/apps/$', 'app_list', name='appcontest_app_list'),
    url(r'^(?P<contest>.*)/submit/$', 'submit', name='appcontest_submit'),
    url(r'^(?P<contest>.*)/thanks/$', 'thanks', name='appcontest_thanks'),
    url(r'^(?P<contest>.*)/$', 'index', name='appcontest_index'),
)
