import datetime
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.conf import settings
from models import Idea, Vote

def idea_list(request, ordering='-total_upvotes'):
    ordering_db = {'most_popular': '-score',
                   'latest': '-submit_date'}[ordering]
    paginator = Paginator(Idea.objects.order_by(ordering_db), 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        ideas = paginator.page(page)
    except (EmptyPage, InvalidPage):
        ideas = paginator.page(paginator.num_pages)

    return render_to_response('ideas/index.html',
                              {'ideas': ideas, 'ordering': ordering},
                              context_instance=RequestContext(request))

def idea_detail(request, id):
    idea = get_object_or_404(Idea, pk=id)
    return render_to_response('ideas/idea_detail.html',
                              {'idea': idea},
                              context_instance=RequestContext(request))

@require_POST
def new_idea(request):
    title = request.POST['title']
    description = request.POST['description']
    user = request.user
    idea = Idea.objects.create(title=title, description=description, user=user)
    return HttpResponseRedirect(idea.get_absolute_url())

@require_POST
@login_required
def submit_comment(request):
    content_type = ContentType.objects.get_for_model(Idea).id
    site = settings.SITE_ID
    object_pk = request.POST['idea_id']
    name = request.POST.get('name', 'anonymous')
    email = request.POST.get('email', '')
    url = request.POST.get('url', '')
    comment = request.POST['comment']
    date = datetime.datetime.now()
    ip = request.META['REMOTE_ADDR']
    c = Comment.objects.create(user_name=name, user_email=email, user_url=url,
            comment=comment, submit_date=date, ip_address=ip,
            site_id=site, content_type_id=content_type, object_pk=object_pk)
    idea = Idea.objects.get(pk=object_pk)
    linkback = '%s#c%s' % (idea.get_absolute_url(), c.id)
    return HttpResponseRedirect(linkback)

@require_POST
@login_required
def vote(request, idea_id, score):
    idea = get_object_or_404(Idea, pk=idea_id)
    Vote.objects.create(person=request.user, idea=idea, value=score)
    return HttpResponse("{'score':%d}" % idea.score+score)