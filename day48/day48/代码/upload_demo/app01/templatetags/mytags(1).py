from django import template

register = template.Library()


@register.inclusion_tag('dropdown.html')
def sqr_list(num):
    print([[i, '{}的平方是{}'.format(i, i ** 2)] for i in range(1, num + 1)])
    return {'data': [[i, '{}的平方是{}'.format(i, i ** 2)] for i in range(1, num + 1)]}
