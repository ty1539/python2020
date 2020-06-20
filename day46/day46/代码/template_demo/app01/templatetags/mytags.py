from django import template

register = template.Library()


@register.filter
def add_arg(value, arg):
    # 功能
    return "{}_{}".format(value, arg)
