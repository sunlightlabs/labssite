from django.template.defaultfilters import slugify
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from sunlightlabs.appcontest.models import Entry, EntryForm
import gatekeeper

def index(request):
    pass

def submit(request):
    
    message = None
    
    if request.method == "POST":
        
        form = EntryForm(request.POST)
        
        if form.is_valid():
            
            form.cleaned_data['slug'] = slugify(form.cleaned_data['name'])
            
            dupe_slug = Entry.objects.filter(slug=form.cleaned_data['slug']).count()
            
            if dupe_slug:
                form.errors['name'] = ErrorList((u'This app name has already been used. Please choose another name.',))
                
            else:
                if "save" in request.POST:
                    form.save()
                    return HttpResponseRedirect('/contest/')
                else:
                    app = form.cleaned_data
                    return render_to_response("appcontest/preview.html", {"form": form, "app": app})
        
    else:
        form = EntryForm()
    
    return render_to_response("appcontest/submit.html", {"form": form, "message": message})

def app_list(request):
    apps = gatekeeper.approved(Entry.objects.all())
    return render_to_response("appcontest/app_list.html", {"apps": apps})

def app_detail(request, slug):
    try:
        app = Entry.objects.get(slug=slug)
        if not request.user.is_superuser and not gatekeeper.approved(app):
           raise Entry.DoesNotExist
        return render_to_response("appcontest/app_detail.html", {"app": app})
    except Entry.DoesNotExist:
        raise Http404("Application does not exist")