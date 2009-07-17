from django.contrib.auth.models import User
from anthill.models import LocationModel

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True)
    creator = models.ForeignKey(User)

