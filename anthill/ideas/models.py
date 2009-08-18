from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
from markupfield.fields import MarkupField

class IdeaManager(models.Manager):

    def with_user_vote(self, user):
        return self.extra(select={'user_vote':'SELECT value FROM ideas_vote WHERE idea_id=ideas_idea.id AND user_id=%s'}, select_params=[user.id])


class Idea(models.Model):

    title = models.CharField(max_length=100)
    description = MarkupField(default_markup_type=settings.ANTHILL_DEFAULT_MARKUP)
    score = models.IntegerField(default=0)

    submit_date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, related_name='ideas')

    comments = generic.GenericRelation(Comment, object_id_field='object_pk')

    objects = IdeaManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('idea_detail', args=[self.id])

class Vote(models.Model):
    user = models.ForeignKey(User, related_name='idea_votes')
    idea = models.ForeignKey(Idea, related_name='votes')
    value = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s %s on %s' % (self.user, self.value, self.idea)

    class Meta:
        unique_together = (('user', 'idea'),)

def update_idea_votes(sender, instance, created, **kwargs):
    score = instance.idea.votes.aggregate(score=models.Sum('value'))['score']
    instance.idea.score = score
    instance.idea.save()
post_save.connect(update_idea_votes, sender=Vote)
