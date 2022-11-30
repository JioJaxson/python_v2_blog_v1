from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from App01.utils.random_code import random_code
from django import forms
from django.contrib import auth
from App01.models import UserInfo


# from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


# 类似router
# Create your views here.
def index(request):
    return render(request, 'index.html')


def news(request):
    return render(request, 'news.html')


# 登陆的字段验证
class LoginForm(forms.Form):
    name = forms.CharField(error_messages={'required': '请输入用户名!'})
    pwd = forms.CharField(error_messages={'required': '请输入密码!'})
    code = forms.CharField(error_messages={'required': '请输入验证码!'})

    # 重写init 方法
    def __init__(self, *args, **kwargs):
        # 做自己的操作
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    # 局部钩子

    def clean_code(self):
        code: str = self.cleaned_data.get("code")
        valid_code: str = self.request.session.get('valid_code')
        # 校验验证码
        if code.upper() != valid_code.upper():
            self.add_error('code', '验证码错误!')
        return self.cleaned_data

    # 全局钩子
    def clean(self):
        name = self.cleaned_data.get("name")
        pwd = self.cleaned_data.get("pwd")

        user = auth.authenticate(username=name, password=pwd)
        print(user)
        # 校验用户密码
        if not user:
            self.add_error('name', '用户名或密码错误')
            return self.cleaned_data

        # 把用户对象放cleaned_data中
        self.cleaned_data['user'] = user
        return self.cleaned_data


# 注册的字段验证
class SignForm(forms.Form):
    name = forms.CharField(error_messages={'required': '请输入用户名!'})
    pwd = forms.CharField(error_messages={'required': '请输入密码!'})
    re_pwd = forms.CharField(error_messages={'required': '请输入确认密码!'})
    code = forms.CharField(error_messages={'required': '请输入验证码!'})

    # 重写init 方法
    def __init__(self, *args, **kwargs):
        # 做自己的操作
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    # 全局钩子 校验密码与再次密码
    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")
        if pwd != re_pwd:
            self.add_error('re_pwd', '两次密码不一致!')
        return self.cleaned_data

    # 校验用户名全局唯一
    def clean_name(self):
        name = self.cleaned_data.get('name')
        user_query = UserInfo.objects.filter(username=name)
        if user_query:
            self.add_error('name', '该用户已注册!')
        return self.cleaned_data

    # 局部钩子 校验验证码
    def clean_code(self):
        code: str = self.cleaned_data.get("code")
        valid_code: str = self.request.session.get('valid_code')
        # 校验验证码
        if code.upper() != valid_code.upper():
            self.add_error('code', '验证码错误!')
        return self.cleaned_data


# 登陆失败的复用函数
def clean_form(form):
    err_dict: dict = form.errors
    # 拿到所有的错误字段名字
    err_value = list(err_dict.keys())[0]
    # 拿到第一个字段的第一个错误信息
    err_msg = err_dict[err_value][0]
    return err_value, err_msg


def login(request):
    if request.method == 'POST':
        res = {
            'code': 888,
            'msg': "登陆成功",
            'self': None
        }
        form = LoginForm(request.data, request=request)
        if not form.is_valid():
            # 验证不通过
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 执行登陆操作
        # print(form.cleaned_data.get('user'))
        user = form.cleaned_data.get('user')
        auth.login(request, user)
        res['code'] = 0
        return JsonResponse(res)
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
    if request.method == 'POST':
        res = {
            'code': 888,
            'msg': "注册成功",
            'self': None
        }
        form = SignForm(request.data, request=request)
        print(request.data)
        if not form.is_valid():
            # 验证不通过
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 注册成功
        user = UserInfo.objects.create_user(
            username=request.data.get('name'),
            password=request.data.get('pwd')
        )
        # 注册之后直接登陆
        auth.login(request, user)
        res['code'] = 0
        return JsonResponse(res)
    return render(request, 'sign.html')
