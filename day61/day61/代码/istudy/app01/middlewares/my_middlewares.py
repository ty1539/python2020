from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect,reverse,HttpResponse
import re
# from istudy import settings
from django.conf import global_settings,settings
from app01 import models
class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        # 需要登录后访问的地址 需要判断登录状态
        # 默认所有的地址都要登录才能访问
        # 设置一个白名单  不登录就能访问
        url = request.path_info

        # 校验登录状态
        is_login = request.session.get('is_login')
        if is_login:
            # 已经登录了  可以访问
            obj = models.User.objects.filter(pk=request.session['pk']).first()
            request.user_obj = obj  # 千万不要命名成  request.user

            # 不是管理员，不能访问地址
            for i in settings.PERMISSIONS_LIST:
                print()
                if re.match(i, url):
                    if request.user_obj.position != 'root':
                        return HttpResponse('没有访问权限')

            return

        # 白名单
        # 不需要登录就可以访问
        for i in settings.WHITE_LIST:
            if re.match(i, url):
                return




        # 没有登录 需要去登录
        return redirect("{}?url={}".format(reverse('login'),url))
