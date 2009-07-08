from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from forms import SearchForm, ProfileForm

def search(request):
    if request.GET:
        form = SearchForm(request.GET)
    else:
        form = SearchForm()
    num_users = User.objects.all().count()
    latest_users = User.objects.all().order_by('-date_joined')[0:5]

    return render_to_response('people/search.html',
                              {'form':form, 'num_users':num_users, 
                               'latest_users':latest_users,},
                             context_instance=RequestContext(request))

def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render_to_response('people/profile.html', {'p_user':user}, 
                             context_instance=RequestContext(request))

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            profile = user.profile
            user.first_name = form.cleaned_data['name']
            user.email = form.cleaned_data['email']
            profile.photo = form.cleaned_data['photo']
            profile.url = form.cleaned_data['url']
            profile.role = form.cleaned_data['position']
            profile.location = form.cleaned_data['location']
            profile.skills = form.cleaned_data['skills']
            profile.about = form.cleaned_data['about']
            user.save()
            profile.save()
            request.user.message_set.create(message='Saved profile changes.')
    else:
        user = request.user
        profile = user.profile
        data = {'name': user.first_name,
                'email': user.email,
                'photo': profile.photo,
                'url': profile.url, 
                'position': profile.role,
                'location': profile.location,
                'skills': profile.skills,
                'about': profile.about}
        form = ProfileForm(data)
    return render_to_response('people/edit_profile.html', {'form':form},
                             context_instance=RequestContext(request))
