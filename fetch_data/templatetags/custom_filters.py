from django import template

from django.utils.timesince import timesince
from django.utils.timezone import now
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def dashify(value):
    return value.lower().replace(' ', '-')


@register.filter
def timefilter(value):
    """Returns a human-readable string representing the time until or since the given datetime object."""
    if not isinstance(value, datetime):
        return ""
    
    # Ensure that both datetime objects are aware
    if timezone.is_naive(value):
        value = timezone.make_aware(value, timezone.get_current_timezone())
    
    now_time = now()
    
    if timezone.is_naive(now_time):
        now_time = timezone.make_aware(now_time, timezone.get_current_timezone())
    
    if value > now_time:
        # Future date
        return f"{timesince(now_time, value)} left"
    else:
        # Past date
        return f"{timesince(value, now_time)} ago"
