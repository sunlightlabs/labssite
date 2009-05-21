from django.template.defaultfilters import slugify
from django.forms.util import ErrorList
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from sunlightlabs.appcontest.models import Contest, Entry, EntryForm

def index(request, contest):
    contest = Contest.objects.get(slug=contest)
    return render_to_response('appcontest/index.html', {'contest':contest})

def thanks(request, contest):
    contest = Contest.objects.get(slug=contest)
    return render_to_response('appcontest/thanks.html', {'contest':contest})

def submit(request, contest):
    message = None
    contest = Contest.objects.get(slug=contest)

    if request.method == "POST":
        form = EntryForm(request.POST)

        if form.is_valid():
            form.cleaned_data['slug'] = slugify(form.cleaned_data['name'])
            dupe_slug = Entry.objects.filter(slug=form.cleaned_data['slug']).count()
            if dupe_slug:
                form.errors['name'] = ErrorList((u'This app name has already been used. Please choose another name.',))
            else:
                if "save" in request.POST:
                    app = form.save(commit=False)
                    app.contest_id = contest.id
                    app.slug = form.cleaned_data['slug']
                    app.save()
                    return HttpResponseRedirect(reverse('appcontest_thanks', kwargs={'contest':contest.slug}))
                else:
                    app = form.cleaned_data
                    return render_to_response("appcontest/preview.html", {"form": form, "app": app, 
                                                                          "contest":contest})
    else:
        form = EntryForm()

    return render_to_response("appcontest/submit.html", {"contest": contest, "form": form, "message": message})

def app_list(request, contest):
    contest = Contest.objects.get(slug=contest)
    apps = contest.entries.all().approved()
    return render_to_response("appcontest/app_list.html", {"contest": contest,
                                                           "apps": apps})

def app_detail(request, contest, slug):
    contest = Contest.objects.get(slug=contest)
    try:
        app = Entry.objects.get(slug=slug)
        if not request.user.is_superuser and app.moderation_status != 1:
           raise Entry.DoesNotExist
        return render_to_response("appcontest/app_detail.html", {"app": app,
                                                                 "contest":contest})
    except Entry.DoesNotExist:
        raise Http404("Application does not exist")
