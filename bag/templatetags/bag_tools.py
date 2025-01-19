# bag/templatetags/bag_tools.py
from django import template

register = template.Library()

@register.filter
def calc_subtotal(price, quantity):
    return price * quantity


@register.filter
def mul(value, arg):
    """Multiply value and arg."""
    try:
        return float(value) * int(arg)
    except (ValueError, TypeError):
        return 0