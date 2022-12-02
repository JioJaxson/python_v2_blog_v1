import random

from django.views import View
from django.http import JsonResponse
from markdown import markdown
from pyquery import PyQuery
from App01.models import Articles, Tags, Cover
from django import forms
from api.views.login import clean_form


class AddArticleForm(forms.Form):
    title = forms.CharField(error_messages={'required': '请输入文章标题!'})
    content = forms.CharField(error_messages={'required': '请输入文章内容!'})
    abstract = forms.CharField(required=False)  # 不进行为空验证
    cover_id = forms.IntegerField(required=False)  # 不进行为空验证
    category = forms.IntegerField(required=False)  # 不进行为空验证
    status = forms.IntegerField(required=False)  # 不进行为空验证
    pwd = forms.CharField(required=False)  # 不进行为空验证
    recommend = forms.BooleanField(required=False)  # 不进行为空验证

    # 全局钩子 校验分类和密码
    def clean(self):
        category = self.cleaned_data['category']
        if not category:
            self.cleaned_data.pop('category')

        pwd = self.cleaned_data['pwd']
        if not pwd:
            self.cleaned_data.pop('pwd')

    # 文章简介
    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']
        if abstract:
            return abstract
        # 解析文本前30内容
        content = self.cleaned_data.get('content')
        if content:
            abstract = PyQuery(markdown(content)).text()[:30]
            return abstract

    # 文章封面
    def clean_cover_id(self):
        cover_id = self.cleaned_data['cover_id']
        if cover_id:
            return cover_id
        cover_set = Cover.objects.all().values('nid')
        cover_id = random.choice(cover_set)['nid']
        return cover_id


class ArticleView(View):
    def post(self, request):
        res = {
            'msg': '文章发布成功!',
            'code': 412,
            'data': None,
        }
        data = request.data
        data['status'] = 1
        form = AddArticleForm(data)
        if not form.is_valid():
            # 验证不通过
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过
        article_obj = Articles.objects.create(**form.cleaned_data)
        tags = data.get('tags')
        print(tags)
        for tag in tags:
            # for 循环就表明tag存在
            if tag.isdigit():
                # 存在 直接关联
                article_obj.tag.add(tag)
            else:
                # 不存在 先创建 再关联
                tag_obj = Tags.objects.create(title=tag)
                article_obj.tag.add(tag_obj.nid)
        res['code'] = 0
        res['data'] = article_obj.nid
        return JsonResponse(res)

# class ArticleView(View):
#     # 发布文章
#     def post(self, request):
#         res = {
#             'msg': '文章发布成功!',
#             'code': 412,
#             'data': None,
#         }
#         data: dict = request.data
#         print(data)
#         title = data.get('title')
#         # 校验标题
#         if not title:
#             res['msg'] = '请输入文章标题!'
#             return JsonResponse(res)
#
#         content = data.get('content')
#         # 文章内容判断
#         if not content:
#             res['msg'] = '请输入文章内容!'
#             return JsonResponse(res)
#
#         recommend = data.get('recommend')
#
#         # 必填项
#         extra = {
#             'title': title,
#             'content': content,
#             'recommend': recommend,
#             'status': 1
#         }
#
#         abstract = data.get('abstract')
#         # 简介判断
#         if not abstract:
#             # 解析文本前30内容
#             abstract = PyQuery(markdown(content)).text()[:30]  # PyQuery解析文本内容 markdown解析markdown格式的内容
#         extra['abstract'] = abstract
#
#         category = data.get('category')
#         if category:
#             extra['category'] = category
#
#         cover_id = data.get('cover_id')
#         if cover_id:
#             extra['cover_id'] = cover_id
#         else:
#             # 未上传封面 默认上次value为1的那张
#             extra['cover_id'] = 1
#
#         pwd = data.get('pwd')
#         if pwd:
#             extra['pwd'] = pwd
#         # 添加文章
#         article_obj = Articles.objects.create(**extra)
#         # 标签
#         tags = data.get('tags')
#         if tags:
#             for tag in tags:
#                 if not tag.isdigit():
#                     tag_obj = Tags.objects.create(title=tag)
#                     article_obj.tag.add(tag_obj)
#                 else:
#                     article_obj.tag.add(tag)
#         res['code'] = 0
#         res['data'] = article_obj.nid
#         return JsonResponse(res)
