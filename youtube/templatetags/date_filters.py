from django import template
from dateutil.parser import parse

register = template.Library()

@register.filter
def format_date(date):
    date_object = parse(date)
    return date_object