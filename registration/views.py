from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from registration.forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            login(request, user)
            if form.cleaned_data['email_opt_in']:
                user.profile.allow_org_emails = True
                user.profile.save()
            user.message_set.create(message="Thank you for creating an account.  You may now create your profile if you wish.")
            return redirect('edit_profile')
    else:
        form = RegistrationForm()

    return render_to_response('registration/registration_form.html',
                              {'form': form}, 
                              context_instance=RequestContext(request))

