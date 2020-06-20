from django import template
from django.shortcuts import reverse

register = template.Library()
from django.http.request import QueryDict

@register.simple_tag
def reverse_url(request,name, *args, **kwargs):
    qd = QueryDict(mutable=True)

    url = request.get_full_path()
    qd['url'] = url

    return "{}?{}".format(reverse(name, args=args, kwargs=kwargs),qd.urlencode())
