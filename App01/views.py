from django.shortcuts import render, HttpResponse, redirect
from App01.utils.random_code import random_code
from django import forms
from django.contrib import auth
from App01.models import UserInfo
from App01.models import Articles, Tags, Cover


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
    if not request.user.username:
        # 未登录
        return redirect('/')

    return render(request, 'backstage/backstage.html', locals())


# 添加文章
def add_article(request):
    # 拿到所有的分类,标签,封面
    category_list = Articles.category_choice
    tag_list = Tags.objects.all()
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            'url': cover.url.url,
            'nid': cover.nid,
        })
    return render(request, 'backstage/add_article.html', locals())


# 修改头像
def edit_avatar(request):
    return render(request, 'backstage/edit_avatar.html', locals())


# 重置密码
def reset_password(request):
    return render(request, 'backstage/reset_password.html', locals())


# 编辑文章
def edit_article(request, nid):
    article_obj = Articles.objects.get(nid=nid)
    tags = [str(tag.nid) for tag in article_obj.tag.all()]
    # 拿到所有的分类,标签,封面
    tag_list = Tags.objects.all()
    category_list = Articles.category_choice
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            'url': cover.url.url,
            'nid': cover.nid,
        })

    return render(request, 'backstage/edit_article.html', locals())
