from haystack import site
from haystack import indexes
from blogdor.models import Post
from anthill.projects.models import Project
from anthill.events.models import Event
from anthill.people.models import Profile
from brainstorm.models import Idea

class PostIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    pub_date = indexes.DateTimeField(model_attr='date_published')

    def get_queryset(self):
        return Post.objects.filter(is_published=True)
site.register(Post, PostIndex)


class ProjectIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='lead')

    def get_queryset(self):
        return Project.objects.all()
site.register(Project, ProjectIndex)


class IdeaIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='submit_date')
site.register(Idea, IdeaIndex)


class EventIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='creator')

    def get_queryset(self):
        return Event.objects.future()
site.register(Event, EventIndex)

