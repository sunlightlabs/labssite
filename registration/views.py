from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from registration.forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
    else:
        form = RegistrationForm()

    return render_to_response('registration/registration_form.html',
                              {'form': form}, 
                              context_instance=RequestContext(request))

