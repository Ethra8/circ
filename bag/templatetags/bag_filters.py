from django import template

register = template.Library()

@register.filter
def is_in(value, arg_list):
    """
    Check if a value is in a list of arguments.
    Usage: {% if value|is_in:"arg1,arg2,arg3" %}
    """
    return value in arg_list.split(',')
