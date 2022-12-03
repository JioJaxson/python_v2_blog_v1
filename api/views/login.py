from django import forms
from django.contrib import auth
from App01.models import UserInfo, Avatars
from django.views import View
from django.http import JsonResponse
import random


# CBV 模式  => class
# FBV 模式 => function

# 登陆注册共用
class LoginBaseForm(forms.Form):
    name = forms.CharField(error_messages={'required': '请输入用户名!'})
    pwd = forms.CharField(error_messages={'required': '请输入密码!'})
    code = forms.CharField(error_messages={'required': '请输入验证码!'})

    # 重写init 方法
    def __init__(self, *args, **kwargs):
        # 做自己的操作
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    # 局部钩子 校验验证码
    def clean_code(self):
        code: str = self.cleaned_data.get("code")
        valid_code: str = self.request.session.get('valid_code')
        # 校验验证码
        if code.upper() != valid_code.upper():
            self.add_error('code', '验证码错误!')
        return self.cleaned_data


# 登陆的字段验证
class LoginForm(LoginBaseForm):

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
class SignForm(LoginBaseForm):
    re_pwd = forms.CharField(error_messages={'required': '请输入确认密码!'})

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


# 登陆失败的复用函数
def clean_form(form):
    err_dict: dict = form.errors
    # 拿到所有的错误字段名字
    err_value = list(err_dict.keys())[0]
    # 拿到第一个字段的第一个错误信息
    err_msg = err_dict[err_value][0]
    return err_value, err_msg


# CBV
class LoginView(View):
    def post(self, request):
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


class SignView(View):
    def post(self, request):
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
        # 随机选择头像
        avatar_list = [i.nid for i in Avatars.objects.all()]
        user.avatar_id = random.choice(avatar_list)
        user.save()
        # 注册之后直接登陆
        auth.login(request, user)
        res['code'] = 0
        return JsonResponse(res)
