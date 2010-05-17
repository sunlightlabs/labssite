from django.shortcuts import render_to_response
from judging.models import Rating, Project

def judge_form(request):
    if request.method == 'POST':
        for name, val in request.POST.iteritems():
            if val:
                project_id = int(name.split('_')[1])
                rating, created = Rating.objects.get_or_create(
                    user=request.user,
                    project=Project.objects.get(pk=project_id),
                    defaults={'rating':int(val)})
                if not created:
                    rating.rating = val
                    rating.save()

    # show projects
    projects = Project.objects.filter(creation_date__gte='2010-03-17').extra(select={'rating': 'SELECT rating from judging_rating jr where project_id=projects_project.id'})[0:7]
    return render_to_response('judging/judge_form.html',
                              {'projects':projects})

