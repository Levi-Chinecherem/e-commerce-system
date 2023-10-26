from django import template

register = template.Library()

@register.filter(name='floatmul')
def floatmul(value, arg):
    return float(value) * float(arg)
