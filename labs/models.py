from blogdor.models import Post
import popular

def url_to_post(url):
    from django.core.urlresolvers import resolve
    view,_,pieces = resolve(url)
    return Post.objects.get(slug=pieces['slug'], timestamp__year=pieces['year'])
popular.register(Post, '^/blog/[0-9]{4}/', url_to_post)
