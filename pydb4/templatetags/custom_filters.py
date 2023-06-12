from django import template

register = template.Library()

@register.filter
def is_iterable(value):
    try:
        iter(value)
        return True
    except TypeError:
        return False

@register.filter
def split_list_of_items(value):
    return value.split('-')
