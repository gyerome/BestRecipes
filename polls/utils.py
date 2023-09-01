from datetime import datetime
from zoneinfo import ZoneInfo
from .constants import UNITS

def calculate_time(date: datetime):
    delta = datetime.utcnow().astimezone(ZoneInfo(key='UTC')) - date

    if delta.days / 365 > 1:
        return (f'{round(delta.days / 365)} years ago', UNITS['year'])

    elif delta.days / 29.3 > 1:
        return (f'{round(delta.days / 29.3)} months ago', UNITS['month'])

    elif delta.days / 7 > 1:
        return (f'{round(delta.days / 7)} weeks ago', UNITS['week'])

    elif delta.days != 0:
        return (f'{delta.days} days ago', UNITS['day'])

    elif delta.seconds / 3600 > 1:
        return (f'{delta.seconds // 3600 + 1} hours ago', UNITS['hour'])

    else:
        return (f'{delta.seconds // 60 + 1} minutes ago', UNITS['minute'])
