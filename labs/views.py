import urllib2
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.flatpages.models import FlatPage
from django.views.decorators.cache import cache_control
from django.core.cache import cache
from contact_form.views import contact_form
from blogdor.models import Post
from blogdor.views import archive
from simplesurvey.models import AnswerSet, QuestionSet
from simplesurvey.forms import SurveyForm
from anthill.projects.models import Project

def index(request):
    try:
        fpage = FlatPage.objects.get(url='alertbox-content')
        box = fpage.content.strip()
    except FlatPage.DoesNotExist:
        box = ''
    return render_to_response("labs/index.html", {'alertbox': box},
                             context_instance=RequestContext(request))

def blog_wrapper(request):
    if 'feed' in request.GET:
        return HttpResponseRedirect('/blog/feeds/latest')
    return archive(request)

def contact_sent(request, form_class):
    return contact_form(request, form_class, template_name='contact_form/contact_form_sent.html')

def image_wrapper(request, image_path):
    image_path = "images/%s" % image_path
    data = {"image_path": image_path}
    return render_to_response("labs/image_wrapper.html", data)

def proxypage(request):

    # could look up a proxy object here based on URL
    proxy_url = 'http://tasks.sunlightfoundation.com/open/'
    cache_time = 300                # 5 minute default timeout
    proxypage_template = 'flatpages/default_openpage.html'

    cache_key = 'proxy_%s' % proxy_url

    proxypage = cache.get(cache_key)
    if proxypage is None:
        try:
            proxypage = urllib2.urlopen(proxy_url).read()
            cache.set(cache_key, proxypage, cache_time)
        except urllib2.HTTPError:
            proxypage = 'Error Retrieving Content'

    if proxypage:
        proxypage = mark_safe(proxypage)

    return render_to_response(proxypage_template, {'proxypage_content':proxypage},
                              context_instance=RequestContext(request))
