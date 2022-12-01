from django.shortcuts import render, HttpResponse, redirect
from App01.utils.random_code import random_code
from django import forms
from django.contrib import auth
from App01.models import UserInfo
from App01.models import Articles


# from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


# 类似router
# Create your views here.
def index(request):
    return render(request, 'index.html', {'request': request})


# 文章
def article(request, nid):
    article_query = Articles.objects.filter(nid=nid)
    if not article_query:
        return redirect('/')
    article = article_query.first()
    return render(request, 'article.html', locals())


def news(request):
    return render(request, 'news.html')


def login(request):
    return render(request, 'login.html')


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


def logout(request):
    # 注销
    auth.logout(request)
    # 跳转
    return redirect('/')


# 后台
def backstage(request):
    return render(request, 'backstage/backstage.html')
