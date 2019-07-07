from django import template

register = template.Library()

@register.filter
def at_index(l, i):
    try:
        return l[i]
    except:
        return None

@register.filter
def is_false(arg):
    return arg is False