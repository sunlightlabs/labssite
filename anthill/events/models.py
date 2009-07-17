from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models
from anthill.models import LocationModel

class Event(LocationModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', args=[self.id])
