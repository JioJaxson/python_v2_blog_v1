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
        data = request.data
        valid_code: str = request.session.get('valid_code')
        print(valid_code, data)
        if valid_code.upper() == data.get('code').upper():
            print('验证码输入正确')
        else:
            print('验证码输入错误')
        return JsonResponse(data)
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
