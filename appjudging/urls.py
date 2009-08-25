from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^submit/$', 'simplesurvey.views.submit', name='appjudging_submit'),
    url(r'^app/(?P<app_id>\d+)/$', 'labssite.appjudging.views.app', name='appjudging_app'),
    url(r'^app/(?P<app_id>\d+)/scorecard/$', 'labssite.appjudging.views.app_scorecard', name='appjudging_appscorecard'),
    url(r'^(?P<contest>.*)/scores/$', 'labssite.appjudging.views.scores', name='appjudging_scores'),
    url(r'^(?P<contest>.*)/$', 'labssite.appjudging.views.index', name='appjudging_app_list'),
)
