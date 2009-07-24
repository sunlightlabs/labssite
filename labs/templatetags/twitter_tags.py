from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import urlize
import twitter

register = template.Library()

class TweetsNode(template.Node):
    def __init__(self, user, count, context_var):
        self.user = user
        self.count = count
        self.context_var = context_var

    def render(self, context):
        api = twitter.Api()
        if self.user[0] == self.user[-1] and self.user[0] in ('"', "'"):
            user = self.user[1:-1]
        else:
            user = template.Variable(self.user).resolve(context)
        context[self.context_var] = api.GetUserTimeline(user, count=self.count)
        return ''

@register.tag
def get_latest_tweets(parser, token):
    '''
        {% get_latest_tweets user 5 as tweets %}
    '''
    pieces = token.split_contents()
    if len(pieces) != 5 or pieces[-2] != 'as':
        raise TemplateSyntaxError('call {%% %s username num_tweets as context_var %%}' % pieces[0])

    return TweetsNode(pieces[1], pieces[2], pieces[4])


@register.filter
@stringfilter
def twitterize(value, autoescape=None):
    '''
        twitterize filter from http://www.djangosnippets.org/snippets/1445/
        by thomasw
    '''
    import re
    # Link URLs
    value = urlize(value, nofollow=False, autoescape=autoescape)
    # Link twitter usernames prefixed with @
    value = re.sub(r'(\s+|\A)@([a-zA-Z0-9\-_]*)\b',r'\1<a href="http://twitter.com/\2">@\2</a>',value)
    # Link hash tags
    value = re.sub(r'(\s+|\A)#([a-zA-Z0-9\-_]*)\b',r'\1<a href="http://search.twitter.com/search?q=%23\2">#\2</a>',value)
    return mark_safe(value)
twitterize.is_safe=True
twitterize.needs_autoescape=True
