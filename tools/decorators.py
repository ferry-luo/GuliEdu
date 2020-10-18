from django.shortcuts import redirect,reverse
from django.http import JsonResponse
#“开始学习”、“收藏”用到了login_decorator这个装饰器
def login_decorator(func):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            if request.is_ajax():   #“收藏”等功能，是ajax请求。未登录时点收藏则返回'status':'no login'
                return JsonResponse({
                    'status':'no login'
                })
            # 拿到目前访问的完整url，不只是路径部分
            url = request.get_full_path()
            ret = redirect(reverse('users:user_login'))
            ret.set_cookie('url',url)
            return ret
    return inner
