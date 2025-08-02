# main/templatetags/__init__.py
# Create this empty file

# main/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplies the value by the argument."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def range_filter(value):
    """Returns a range from 1 to value."""
    try:
        return range(1, int(value) + 1)
    except (ValueError, TypeError):
        return range(0)