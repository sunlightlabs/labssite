from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import generic
from tagging.fields import TagField
from markupfield.fields import MarkupField
from anthill.ideas.models import Idea

class Project(models.Model):
    slug = models.SlugField('unique identifier for project',
                            max_length=50, unique=True,
                            help_text="changing this value will alter your project's URL")
    name = models.CharField('displayed name of project', max_length=100)
    description = MarkupField()
    official = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    skills = TagField('list of skills used/required on this project')

    lead = models.ForeignKey(User, related_name='projects_lead_on')
    members = models.ManyToManyField(User, through='Role')
    idea = models.ForeignKey(Idea, blank=True, null=True, related_name='projects')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_detail', args=[self.slug])

    def get_members(self):
        return self.members.filter(project_roles__is_lead=False, 
                                   project_roles__status='A')

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
    message = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super(Role, self).save(*args, **kwargs)
        if self.is_lead:
            self.project.lead = self.user
            self.project.save()

SOURCE_LINK, DOCS_LINK, DOWNLOAD_LINK = range(3)
LINK_TYPES = (
    (SOURCE_LINK, 'source'),
    (DOCS_LINK, 'documentation'),
    (DOWNLOAD_LINK, 'download'),
)

class Link(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    link_type = models.PositiveSmallIntegerField(choices=LINK_TYPES)
    order = models.PositiveSmallIntegerField()

    project = models.ForeignKey(Project, related_name='links')

    class Meta:
        ordering = ['order']
