from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from sunlightlabs.appcontest.models import Entry
from simplesurvey.forms import SurveyForm
from simplesurvey.models import QuestionSet, AnswerSet, Answer

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
        aset = AnswerSet.objects.for_model(Entry).get(question_set=qs, user=request.user, object_id=app.pk)
    except AnswerSet.DoesNotExist:
        aset = None

    form = SurveyForm(qs, related_object=app, answer_set=aset)

    data = {
        "question_set": qs,
        "app": app,
        "form": form,
    }

    return render_to_response('appjudging/app_scorecard.html', data)

@login_required
def scores(request):
    
    # app id
    # question 1
    # question 2
    # question 3
    # question 4
    # question 5
    # judge id
    
    question_set = QuestionSet.objects.get(slug="appcontest")
    answers_sets = AnswerSet.objects.all().select_related()
    scores = []
    
    csv = ""
    
    for answer_set in answers_sets:
        score = [answer_set.related_object.name, 0, 0, 0, 0, 0, answer_set.user.get_full_name()]
        for answer in answer_set.answers.all():
            score[answer.question_id] = int(answer.text)
        scores.append(score)    
        print score
        csv += '''"%s",%i,%i,%i,%i,%i,"%s"\n''' % (score[0], score[1], score[2], score[3], score[4], score[5], score[6])
        
    return HttpResponse(csv, content_type="text/plain")