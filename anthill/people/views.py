from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from anthill.people.models import Profile
from anthill.people.forms import SearchForm, ProfileForm, PasswordForm

def search(request):
    if request.GET:
        form = SearchForm(request.GET)
        form.is_valid()
        location = form.cleaned_data['location']
        name = form.cleaned_data['name']
        position = form.cleaned_data['position']
        location_range = form.cleaned_data['location_range']

        users = Profile.objects.all().select_related()
        if position:
            users = users.filter(role=position)
        if location:
            pass
            # point = geocode(location)
            # users = users.filter(lat_long__dwithin=(point, location_range))
        if name:
            users = users.filter(user__first_name__icontains=name)
        context = { 'form': form, 'searched': True, 'search_results': users }
    else:
        context = { 'form': SearchForm() }

    return render_to_response('people/search.html', context,
                             context_instance=RequestContext(request))

def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render_to_response('people/profile.html', {'p_user':user}, 
                             context_instance=RequestContext(request))

def _user_to_profileform(user):
    profile = user.profile
    data = {'name': user.first_name,
            'email': user.email,
            'twitter_id': profile.twitter_id,
            'photo': profile.photo,
            'url': profile.url, 
            'position': profile.role,
            'location': profile.location,
            'skills': profile.skills,
            'about': profile.about}
    return ProfileForm(data)

@login_required
def edit_profile(request):
    password_form = PasswordForm()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            profile = user.profile
            user.first_name = form.cleaned_data['name']
            user.email = form.cleaned_data['email']
            profile.twitter_id = form.cleaned_data['twitter_id']
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
        form = _user_to_profileform(request.user)
    return render_to_response('people/edit_profile.html', 
                              {'form':form, 'password_form':password_form},
                              context_instance=RequestContext(request))

@login_required
@require_POST
def change_password(request):
    user = request.user
    password_form = PasswordForm(request.POST)
    form = _user_to_profileform(user)
    if password_form.is_valid():
        user.set_password(password_form.cleaned_data['password1'])
        user.message_set.create(message='Password changed.')
        password_form = PasswordForm()
    else:
        user.message_set.create(message='Passwords did not match.')
    return redirect('edit_profile')
