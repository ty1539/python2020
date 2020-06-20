from django import template

register = template.Library()


@register.filter
def add_arg(value, arg):
    # 功能
    return "{}_{}".format(value, arg)


@register.filter
def cheng(a, b):
    # 功能
    return int(a) * int(b)


@register.filter
def chu(a, b):
    # 功能
    return int(a) / int(b)


from django.utils.safestring import mark_safe


@register.filter
def show_a(name, url):
    return mark_safe('<a href="http://{}">{}</a>'.format(url, name))


@register.simple_tag
def str_join(*args, **kwargs):
    return "{}_{}".format('_'.join(args), '*'.join(kwargs.values()))
