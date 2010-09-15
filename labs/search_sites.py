from haystack import site
from haystack import indexes
from blogdor.models import Post
from anthill.projects.models import Project
from anthill.people.models import Profile

class PostIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    pub_date = indexes.DateTimeField(model_attr='date_published')

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def should_update(self, instance, **kwargs):
        return instance.is_published
site.register(Post, PostIndex)


class ProjectIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='lead')

    def get_queryset(self):
        return Project.objects.all()
site.register(Project, ProjectIndex)

