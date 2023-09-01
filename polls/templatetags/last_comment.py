from django.template.defaultfilters import register
from polls.models import Forum, Comment
from django.template import defaultfilters
from datetime import datetime
from zoneinfo import ZoneInfo

@register.filter(name='last_comment')
def get_last_comment(forum: Forum):
    try:
        last_comment = Comment.objects.filter(forum=forum).order_by('-date')[0]
    except: last_comment = None


    return last_comment

@register.filter(name='calculate_date')
def calculate_date(date: datetime):
    delta = datetime.utcnow().astimezone(ZoneInfo(key='UTC')) - date

    if delta.days / 365 > 1:
        return f'{round(delta.days / 365)} years ago'

    elif delta.days / 29.3 > 1:
        return f'{round(delta.days / 29.3)} months ago'

    elif delta.days / 7 > 1:
        return f'{round(delta.days / 7)} weeks ago'

    elif delta.days != 0:
        return f'{delta.days} days ago'

    elif delta.seconds / 3600 > 1:
        return f'{delta.seconds // 3600 + 1} hours ago'

    else:
        return f'{delta.seconds // 60 + 1} minutes ago'
