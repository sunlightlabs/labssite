from django import forms
from django.contrib.auth.models import User

required = {'class': 'required'}

class RegistrationForm(forms.Form):

    username = forms.RegexField(regex=r'^\w+$', max_length=30,
                                widget=forms.TextInput(attrs=required),
                                label='Username')
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required, 
                                                               maxlength=75)),
                            label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=required, 
                                                           render_value=False),
                                label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=required, 
                                                           render_value=False),
                                label='Confirm Password')

    banned_names = ['admin']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).count() > 0:
            raise forms.ValidationError('This username is already taken. Please choose another')
        if username in self.banned_names:
            raise forms.ValidationError('This username is invalid. Please choose another.')
        return self.cleaned_data['username']

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError('This email address is already in use.')
        return self.cleaned_data['email']

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError('Passwords must match')
        return self.cleaned_data

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password1'])
        return user
