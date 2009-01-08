from django.db import models
from django.forms import ModelForm
import gatekeeper

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
    quick_description = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-timestamp',)
    
    def __unicode__(self):
        return self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ('appcontest_app_detail', [self.slug])
        
class EntryForm(ModelForm):
    class Meta:
        model = Entry
        exclude = ('slug','timestamp')

class Vote(models.Model):
    entry = models.ForeignKey(Entry)
    ip = models.IPAddressField()
    
    def __unicode__(self):
        return u"%s %s" % (self.ip, str(self.entry))

gatekeeper.register(Entry)