from django import forms
from contact_form.forms import ContactForm

class LabsContactForm(ContactForm):

    attrs_dict = { 'class': 'required' }

    from_email = "bounce@sunlightfoundation.com"
    recipient_list = ['swells@sunlightfoundation.com','cjohnson@sunlightfoundation.com','jcarbaugh@sunlightfoundation.com', 'jturk@sunlightfoundation.com']
    subject = "[SunlightLabs.com] Contact"

    name = forms.CharField(max_length=100,
                widget=forms.TextInput(attrs=attrs_dict),
                label=u'Name')
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=200)),
                label=u'Email Address')
    body = forms.CharField(widget=forms.Textarea(attrs=attrs_dict),
                label=u'Comment')



