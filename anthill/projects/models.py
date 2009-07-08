from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField

class Project(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    official = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    skills = TagField('list of skills used/required on this project')

    lead = models.ForeignKey(User, related_name='projects_lead_on')
    members = models.ManyToManyField(User, through='Role')

    def __unicode__(self):
        return self.name

ROLE_STATUSES = (
    ('P', 'Pending'),
    ('A', 'Active'),
    ('R', 'Retired')
)

class Role(models.Model):
    user = models.ForeignKey(User, related_name='project_roles')
    project = models.ForeignKey(Project, related_name='roles')
    join_time = models.DateField(auto_now_add=True)
    status = models.CharField(choices=ROLE_STATUSES, max_length=1, default='P')
    is_lead = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Role, self).save(*args, **kwargs)
        if self.is_lead:
            self.project.lead = self.user
            self.project.save()