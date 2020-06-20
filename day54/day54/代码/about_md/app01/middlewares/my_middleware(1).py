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


visit_history = {
    # ip : [ 10:55:05 , 10:55:06 ,10:55:07]  —— 》  [ 10:55:12]
}
import time


class Throttle(MiddlewareMixin):

    def process_request(self, request):

        ip = request.META.get('REMOTE_ADDR')

        history = visit_history.get(ip, [])

        # 第一次  05 history  []
        # 第二次  06  history  [10:55:05]
        # 第三次  07 history  [10:55:05,10:55:06 ]
        # 第四次  08 history   [ 10:55:05 , 10:55:06 ,10:55:07]
        # 第五次  12  history   [ 10:55:05 , 10:55:06 ,10:55:07]

        now = time.time()
        new_history = []
        for i in history:
            if now - i < 5:
                new_history.append(i)

        visit_history[ip] = new_history
        if len(new_history) >= 3:
            return HttpResponse('你的手速太快了，需要歇一会')
        new_history.append(now)


# [ 10:55:07 , 10:55:06 ,]    10:55:11
class Throttle(MiddlewareMixin):

    def process_request(self, request):

        ip = request.META.get('REMOTE_ADDR')

        history = visit_history.get(ip, [])

        now = time.time()

        while history and now - history[-1] > 5:
            history.pop()

        if len(history) >= 3:
            return HttpResponse('你的手速太快了，需要歇一会')

        history.insert(0, now)
        visit_history[ip] = history
     
