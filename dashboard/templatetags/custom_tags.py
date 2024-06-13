from django import template
from django.conf import settings
from django.contrib.auth.models import Group


register = template.Library()
 
@register.filter
def format_amount(value):
    """
    Formats a number with thousands separators and two decimal places.
    """
    try:
        return "{:,.2f}".format(float(value))
    except Exception as e:
        settings.LOGGER.error(e)
        return 0.00
    
@register.filter
def has_role(user, role):
    group = Group.objects.filter(name=role).first()
    return group in user.groups.all() 