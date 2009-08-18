from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from appcontest.models import Entry, Contest
from simplesurvey.forms import SurveyForm
from simplesurvey.models import QuestionSet, AnswerSet, Answer

@permission_required('appcontest.is_judge')
def index(request, contest):
    contest = get_object_or_404(Contest, slug=contest)
    apps = contest.entries.all().approved()
    judged_ids = AnswerSet.objects.for_model(Entry).filter(user=request.user).values_list('object_id', flat=True)
    for app in apps:
        app.judged = app.pk in judged_ids
    return render_to_response("appjudging/index.html", {"apps": apps, "judged_ids": judged_ids},
                             context_instance=RequestContext(request))

@permission_required('appcontest.is_judge')
def app(request, app_id):
    app = Entry.objects.get(pk=app_id)
    return render_to_response('appjudging/app.html', {"app": app})

@permission_required('appcontest.is_judge')
def app_scorecard(request, app_id):

    app = Entry.objects.get(pk=app_id)
    qs = QuestionSet.objects.get(slug="judgeforamerica2")

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
def scores(request, contest):
    
    # app id
    # question 1
    # question 2
    # question 3
    # judge id

    entry_ids = list(Entry.objects.filter(contest__slug=contest).values_list('id',flat=True))
    question_set = QuestionSet.objects.get(slug="appcontest")
    answers_sets = AnswerSet.objects.filter(object_id__in=entry_ids).select_related()
    scores = []

    csv = ""

    for answer_set in answers_sets:
        score = [answer_set.related_object.name, 0, 0, 0, answer_set.user.get_full_name()]
        for answer in answer_set.answers.all():
            score[answer.question_id-5] = int(answer.text[0])
        scores.append(score)
        csv += '''"%s",%i,%i,%i,"%s"\n''' % (score[0], score[1], score[2], score[3], score[4])

    return HttpResponse(csv, content_type="text/plain")
