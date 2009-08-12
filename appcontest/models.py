import datetime
from django.db import models
from django.forms import ModelForm, ValidationError
import gatekeeper

class Contest(models.Model):
    name = models.CharField("Contest Name", max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    body = models.TextField()
    template_name = models.CharField(max_length=128)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_open(self):
        """ check if the contest is currently open """
        return self.start_date < datetime.datetime.now() < self.end_date

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('appcontest_index', [self.slug])

    class Meta:
        permissions = (
            ('is_judge', 'Is Judge'),
        )

class Entry(models.Model):

    name = models.CharField("Your apps name", max_length=128)
    slug = models.SlugField(unique=True)
    contact_display = models.CharField(max_length=128)
    contact_name = models.CharField(max_length=128)
    contact_email = models.EmailField()
    contact_url = models.URLField(verify_exists=False, blank=True, null=True)
    logo_url = models.URLField(verify_exists=False, blank=True, null=True)
    url = models.URLField(verify_exists=False)
    source_url = models.URLField(verify_exists=False)
    data_source =  models.URLField(verify_exists=False)
    quick_description = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    contest = models.ForeignKey(Contest, related_name='entries')

    class Meta:
        ordering = ('-timestamp',)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('appcontest_app_detail', [self.contest.slug, self.slug])

class EntryForm(ModelForm):
    def clean_data_source(self):
        data = self.cleaned_data['data_source']
        if 'data.gov' not in data:
            raise ValidationError("Data source must be a data.gov URL")
        return data

    class Meta:
        model = Entry
        exclude = ('slug','timestamp', 'contest')

gatekeeper.register(Entry)
