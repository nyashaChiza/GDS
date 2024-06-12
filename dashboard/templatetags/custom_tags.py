from django import template
from django.conf import settings


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