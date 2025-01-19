# bag/templatetags/bag_tools.py
from django import template

register = template.Library()

@register.filter
def calc_subtotal(price, quantity):
    return price * quantity
