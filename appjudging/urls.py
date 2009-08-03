from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^submit/$', 'simplesurvey.views.submit', name='appjudging_submit'),
    url(r'^app/(?P<app_id>\d+)/$', 'sunlightlabs.appjudging.views.app', name='appjudging_app'),
    url(r'^app/(?P<app_id>\d+)/scorecard/$', 'sunlightlabs.appjudging.views.app_scorecard', name='appjudging_appscorecard'),
    url(r'^(?P<contest>.*)/scores/$', 'sunlightlabs.appjudging.views.scores', name='appjudging_scores'),
    url(r'^(?P<contest>.*)/$', 'sunlightlabs.appjudging.views.index', name='appjudging_app_list'),
)
