from django.views import View
from django.http import JsonResponse
from api.views.login import clean_form
from django.db.models import F
from django import forms
from App01.models import Avatars, Moods, MoodComment
import random
from api.utils.get_user_info import get_ip, get_address_info

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

# 心情
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

        ip = get_ip(request)
        addr = get_address_info(ip)
        print(ip)
        print(addr)
        form.cleaned_data['ip'] = ip
        form.cleaned_data['addr'] = addr
        Moods.objects.create(**form.cleaned_data)
        res['code'] = 0
        return JsonResponse(res)

    def delete(self, request, nid):
        res = {
            'msg': '心情删除成功!',
            'code': 412,
        }
        if not (request.user.is_superuser):
            # 登陆人不是评论人并且登陆人不是超级管理员
            res['msg'] = '用户验证失败！'
            return JsonResponse(res)
        mood_query = Moods.objects.filter(nid=nid)
        if not mood_query:
            res['msg'] = '该心情不存在'
            return JsonResponse(res)
        mood_query.delete()
        res['code'] = 0
        return JsonResponse(res)

# 心情评论
class MoodCommentsView(View):
    def post(self, request, nid):
        res = {
            'msg': '心情评论成功!',
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

        ip = get_ip(request)
        addr = get_address_info(ip)

        form.cleaned_data['ip'] = ip
        form.cleaned_data['addr'] = addr
        form.cleaned_data['mood_id'] = nid
        form.cleaned_data.pop('drawing')
        MoodComment.objects.create(**form.cleaned_data)

        Moods.objects.filter(nid=nid).update(comment_count=F('comment_count') + 1)
        res['code'] = 0
        return JsonResponse(res)

    def delete(self, request, nid):
        res = {
            'msg': '评论删除成功!',
            'code': 412,
        }
        if not request.user.is_superuser:
            # 登陆人不是评论人并且登陆人不是超级管理员
            res['msg'] = '用户验证失败！'
            return JsonResponse(res)
        mood_id = request.get('mood_id')
        # mood_id = request.post('mood_id')
        MoodComment.objects.filter(nid=nid).delete()
        # print('nid', nid, mood_id)
        Moods.objects.filter(nid=mood_id).update(comment_count=F('comment_count') - 1)
        res['code'] = 0
        return JsonResponse(res)

