from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse


class MD1(MiddlewareMixin):
    def process_request(self, request):
        # print(id(request))
        # request.xxx = '我太南了'

        print('MD1 process_request')
        # return HttpResponse('MD1 process_request')

    def process_response(self, request, response):
        print('MD1 process_response')
        # print('index', id(response))

        # ret = HttpResponse('xxxx')
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # print(view_func)
        # print(view_args)
        # print(view_kwargs)
        print('MD1 process_view')

        # return HttpResponse('MD1 process_view')

    def process_exception(self, request, exception):
        print('MD1 process_exception')
        # print(type(exception))

    def process_template_response(self, request, response):
        print('MD1 process_template_response')
        return response


class MD2(MiddlewareMixin):
    def process_request(self, request):
        print('MD2 process_request')

    def process_response(self, request, response):
        print('MD2 process_response')

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('MD2 process_view')

    def process_exception(self, request, exception):
        print('MD2 process_exception')
        return HttpResponse('异常处理好了')

    def process_template_response(self, request, response):
        print('MD2 process_template_response')

        response.template_name = 'index1.html'
        response.context_data['user'] = '天然'

        return response
