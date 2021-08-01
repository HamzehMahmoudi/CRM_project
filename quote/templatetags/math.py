from django import template

register = template.Library()


@register.filter
def sub(value, arg):
    if value is None and arg is None:
        return 0
    return value - arg
