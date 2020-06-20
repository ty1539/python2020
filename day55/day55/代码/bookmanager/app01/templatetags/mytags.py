from django import template

register = template.Library()
from django.utils.safestring import mark_safe

# @register.simple_tag
# def pagination(num):
#     li_list  =  [ '<li><a href="#">{}</a></li>'.format(i) for i in range(1,num+1)  ]
#
#     return mark_safe("""
#     <nav aria-label="Page navigation">
#                     <ul class="pagination">
#                         <li>
#                             <a href="#" aria-label="Previous">
#                                 <span aria-hidden="true">&laquo;</span>
#                             </a>
#                         </li>
#                         {}
#                         <li>
#                             <a href="#" aria-label="Next">
#                                 <span aria-hidden="true">&raquo;</span>
#                             </a>
#                         </li>
#                     </ul>
#                 </nav>""".format(''.join(li_list)))


@register.inclusion_tag('page.html')
def pagination(num):
    return {'num': range(1, num + 1)}
