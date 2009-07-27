from fabric.api import run, get, cd, env, local
import json

POST_CT_ID = 22 # ContentType.objects.get_for_model(Post).id
APP_CT_ID = 30  # ContentType.objects.get_for_model(Entry).id
env.hosts = ['tina.sunlightlabs.org']
env.user = 'jturk'

def convert_blog(filename):
    blogdata = json.load(open(filename))
    for entry in blogdata:
        if entry['model'] == 'blogdor.post':
            fields = entry['fields']
            fields.pop('comment_count')
            status = fields.pop('status')
            markup = fields.pop('markup')
            if markup == 'none':
                markup = 'plain'
            fields['content_markup_type'] = fields['excerpt_markup_type'] = markup
            fields['is_published'] = (status == 'public')
        if entry['model'] == 'comments.comment':
            entry['fields']['content_type'] = POST_CT_ID
            if entry['fields']['ip_address'] == '':
                entry['fields']['ip_address'] = None
    json.dump(blogdata, open('new_'+filename,'w'), indent=1)

def convert_appcontest(filename):
    data = json.load(open(filename))
    for entry in data:
        if entry['model'] == 'appcontest.entry':
            if entry['fields']['data_source'] is None:
                entry['fields']['data_source'] = ''
        elif entry['model'] in ('gatekeeper.moderatedobject', 'simplesurvey.answerset'):
            entry['fields']['content_type'] = APP_CT_ID
    json.dump(data, open('new_'+filename,'w'), indent=1)

def get_dumps():
    mappings = (
        ('auth flatpages redirects sites', 'meta.json'),
        ('simplesurvey appcontest gatekeeper', 'appcontest.json'),
        ('blogdor comments', 'blog.json'))

    # generate files
    with cd('/home/sunlabs/lib/python/sunlightlabs'):
        for mapping in mappings:
            run('export PYTHONPATH=..; ./manage.py dumpdata %s --indent 1 > /home/jturk/%s' % mapping)

    # download files
    for mapping in mappings:
        get('/home/jturk/%s' % mapping[1], '.')

def convert_dumps():
    convert_blog('blog.json')
    convert_appcontest('appcontest.json')

def load_dumps():
    local('./manage.py loaddata meta.json')
    local('./manage.py loaddata new_blog.json')
    local('./manage.py loaddata new_appcontest.json')

def move_data():
    get_dumps()
    convert_dumps()
    load_dumps()

