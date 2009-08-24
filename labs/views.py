from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from contact_form.views import contact_form
from blogdor.models import Post
from blogdor.views import archive
from simplesurvey.models import AnswerSet, QuestionSet
from simplesurvey.forms import SurveyForm
from anthill.projects.models import Project

def index(request):
    return render_to_response("labs/index.html",
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

@login_required
def aa2_judging(request):
    qs = QuestionSet.objects.get(slug='aa2public')
    try:
        aset = AnswerSet.objects.get(question_set=qs, user=request.user)
        message = 'Your vote has been recorded, you may change it if you wish.'
    except AnswerSet.DoesNotExist:
        aset = None
        message = None

    form = SurveyForm(qs, answer_set=aset)

    return render_to_response('labs/public_judging.html',
                              {'form': form, 'message': message},
                             context_instance=RequestContext(request))

