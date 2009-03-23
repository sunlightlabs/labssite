from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from sunlightlabs.appcontest.models import Entry
from simplesurvey.forms import SurveyForm
from simplesurvey.models import QuestionSet, AnswerSet

@login_required
def index(request):
    apps = Entry.objects.all().approved()
    judged_ids = AnswerSet.objects.for_model(Entry).filter(user=request.user).values_list('object_id', flat=True)
    for app in apps:
        app.judged = app.pk in judged_ids
    return render_to_response("appjudging/index.html", {"apps": apps, "judged_ids": judged_ids})

@login_required
def app(request, app_id):
    app = Entry.objects.get(pk=app_id)
    return render_to_response('appjudging/app.html', {"app": app})

@login_required
def app_scorecard(request, app_id):

    app = Entry.objects.get(pk=app_id)
    qs = QuestionSet.objects.get(slug="appcontest")

    try:
        aset = AnswerSet.objects.for_model(Entry).get(question_set=qs, user=request.user)
    except AnswerSet.DoesNotExist:
        aset = None

    form = SurveyForm(qs, related_object=app, answer_set=aset)

    data = {
        "question_set": qs,
        "app": app,
        "form": form,
    }

    return render_to_response('appjudging/app_scorecard.html', data)
    