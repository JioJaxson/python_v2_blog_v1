from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from App01.utils.random_code import random_code


# 类似router
# Create your views here.
def index(request):
    return render(request, 'index.html')


def news(request):
    return render(request, 'news.html')


def login(request):
    if request.method == 'POST':
        res = {
            'code': 888,
            'msg': "登陆成功",
            'self': None
        }
        data = request.data
        name = data.get('name')
        if not name:
            res['msg'] = "请输入用户名!"
            res['self'] = 'name'
            return JsonResponse(res)
        pwd = data.get('pwd')
        if not pwd:
            res['msg'] = "请输入密码!"
            res['self'] = 'pwd'
            return JsonResponse(res)
        code = data.get('code')
        if not code:
            res['msg'] = "请输入验证码!"
            res['self'] = 'code'
            return JsonResponse(res)
        valid_code: str = request.session.get('valid_code')
        print(valid_code, data)
        if valid_code.upper() != code.upper():
            res['msg'] = '验证码输入错误!'
            res['self'] = 'code'
            return JsonResponse(res)
        # 校验用户名密码
        if name != 'mumu' or pwd != '1234':
            res['msg'] = '用户名或密码错误!'
            res['self'] = 'pwd'
            return JsonResponse(res)

        res['code'] = 0
        return JsonResponse(res)
    return render(request, 'login.html')


# def login(request):
#     if request.method == 'POST':
#         data = request.data
#         return JsonResponse(data)
#     return render(request, 'login.html')


# 获取随机验证码
def get_random_code(request):
    # fp = open(r'E:\code\V1_Blog\App01\utils\new_img.png', 'rb')
    # data = fp.read()
    # fp.close()
    data, valid_code = random_code()
    # 将random_code返回的验证码写入session
    request.session['valid_code'] = valid_code
    return HttpResponse(data)


def sign(request):
    return render(request, 'sign.html')
