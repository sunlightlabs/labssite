import urllib2
from django.http import HttpResponse
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
        # hack to get people to stop using this
        return HttpResponse('''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel><title>Sunlight Labs blog</title><link>http://sunlightlabs.com/blog/</link><description>Latest blog updates from the nerds at Sunlight Labs</description><language>en-us</language><lastBuildDate>Fri, 19 Feb 2010 13:39:08 -0500</lastBuildDate><ttl>3600</ttl>
<item>
    <title>Sunlight Labs Feed Has Moved</title>
    <link>http://feeds.feedburner.com/sunlightlabs/blog</link>
    <description> This feed has moved to &lt;a href="http://feeds.feedburner.com/sunlightlabs/blog"&gt;http://feeds.feedburner.com/sunlightlabs/blog&lt;/a&gt;
    </description>
    <pubDate>Fri, 19 Feb 2010 13:39:08 -0500</pubDate>
    <guid isPermaLink="true">http://feeds.feedburner.com/sunlightlabs/blog</guid>
</item></channel></rss>''')

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
