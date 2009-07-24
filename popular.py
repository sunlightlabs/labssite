import datetime
from django.conf import settings
from django.core.urlresolvers import resolve
from googleanalytics import Connection

registered_models = {}

_ga_acct = None
def get_analytics_account():
    global _ga_acct
    if not _ga_acct:
        connection = Connection(settings.GOOGLE_ANALYTICS_EMAIL, settings.GOOGLE_ANALYTICS_PASSWORD)
        _ga_acct = connection.get_account(settings.GOOGLE_ANALYTICS_ID)
    return _ga_acct

def register(model, regex, lookup_func):
    if lookup_func is None:
        def default_lookup_func(url):
            view,_,pieces = resolve(url)
            return model.objects.get(**pieces)
        lookup_func = default_lookup_func
    registered_models[model] = (regex, lookup_func)

def get_popular_items(model, num=5, days_ago=7
                      start_date=None, end_date=None):
    if model not in registered_models:
        raise ValueError('%s not in registry, call popular.register first' % model._meta.object_name)
    regex, lookup_func = registered_models[model]

    if end_date is None:
        end_date = datetime.datetime.now()
    if start_date is None:
        start_date = end_date - datetime.timedelta(days_ago)

    acct = get_analytics_account()
    data = acct.get_data(start_date=start_date, end_date=end_date,
                         dimensions=['pagePath'], metrics=['pageviews'],
                         filters=[['pagePath', '=~', regex]],
                         sort=['-pageviews'], max_results=num)

    objects = []
    for item in data:
        try:
            obj = lookup_func(item.dimension)
            objects.append((obj, item.metric))
        except model.DoesNotExist as e:
            pass
    return objects
