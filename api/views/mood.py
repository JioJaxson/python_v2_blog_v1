from django.views import View
from django.http import JsonResponse
from api.views.login import clean_form
from django.db.models import F
from django import forms
from App01.models import Avatars, Moods, MoodComment
import random

# 添加文章编辑文章的验证
class AddAMoodsForm(forms.Form):
    name = forms.CharField(error_messages={'required': '请输入用户名!'})
    content = forms.CharField(error_messages={'required': '请输入心情内容!'})
    avatar_id = forms.CharField(required=False)  # 不进行为空验证
    drawing = forms.CharField(required=False)  # 不进行为空验证

    def clean_avatar_id(self):
        avatar_id = self.cleaned_data.get('avatar_id')
        if avatar_id:
            return avatar_id
        #没选头像点击提交时随机选择头像
        avatar_list = [i.nid for i in Avatars.objects.all()]
        avatar_id = random.choice(avatar_list)
        return avatar_id

class MoodsView(View):
    def post(self, request):
        res = {
            'msg': '心情发布成功!',
            'code': 412,
            'self': None,
        }
        data = request.data
        print(data)
        form = AddAMoodsForm(data)
        if not form.is_valid():
            # 验证不通过
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        Moods.objects.create(**form.cleaned_data)
        res['code'] = 0
        return JsonResponse(res)