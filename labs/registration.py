from django import forms
from django.shortcuts import redirect
from django_openid.registration import RegistrationConsumer
from django_openid.forms import RegistrationFormPasswordConfirm

from django.conf import settings

class RegistrationForm(RegistrationFormPasswordConfirm):
    extra_required = ('email',)
    email_opt_in = forms.BooleanField(label='Keep me posted about other Sunlight news and information', 
                                      required=False)

class CustomRegistrationConsumer(RegistrationConsumer):
    confirm_email_addresses = False
    RegistrationForm = RegistrationForm
    trust_root = settings.TRUST_ROOT
    on_complete_url = '/accounts/complete/'
    after_registration_url = '/people/edit_profile/'
    recovery_email_subject = 'Recover Your SunlightLabs.com Account'

    def redirect_if_valid_next(self, request):
        "Logic for checking if a signed ?next= token is included in request"
        next = request.REQUEST.get('next')
        if next:
            return redirect(next)
        else:
            return None

    def show_login(self, request, message=None):
        if request.user.is_authenticated():
            return self.show_already_logged_in(request)

        response = self.render(request, self.login_template, {
            'action': request.path,
            'logo': self.logo_path or (request.path + 'logo/'),
            'message': message,
            'next': request.REQUEST.get('next'),
        })

        if self.password_logins_enabled:
            response.template_name = self.login_plus_password_template
            response.template_context.update({
                'account_recovery': self.account_recovery_enabled and (
                    self.account_recovery_url or (request.path + 'recover/')
                ),
            })
        return response

    def on_registration_complete(self, request):
        if request.POST.get('email_opt_in'):
            request.user.profile.allow_org_emails = True
            request.user.profile.save()
        return super(CustomRegistrationConsumer, self).on_registration_complete(request)

    def show_unknown_openid(self, request, openid):
        return redirect('/accounts/register/')

    def show_error(self, request, message, exception=None):
        self.do_logout(request)
        super(CustomRegistrationConsumer, self).show_error(request, message, exception)




registration_consumer = CustomRegistrationConsumer()
