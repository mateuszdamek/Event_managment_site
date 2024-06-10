from django import template
from ..models import Event_Registration

register = template.Library()

@register.filter
def is_registered(user, event):
    return Event_Registration.objects.filter(event_ID=event, user_ID=user).exists()

@register.filter
def is_not_registered(user, event):
    return not Event_Registration.objects.filter(event_ID=event, user_ID=user).exists()
