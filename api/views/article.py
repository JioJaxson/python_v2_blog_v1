import random

from django.views import View
from django.http import JsonResponse
from markdown import markdown
from pyquery import PyQuery
from App01.models import Articles, Tags, Cover
from django import forms
from api.views.login import clean_form
from django.db.models import F


# 添加文章编辑文章的验证
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
            abstract = PyQuery(markdown(content)).text()[:90]
            return abstract

    # 文章封面
    def clean_cover_id(self):
        cover_id = self.cleaned_data['cover_id']
        if cover_id:
            return cover_id
        cover_set = Cover.objects.all().values('nid')
        cover_id = random.choice(cover_set)['nid']
        return cover_id


# 给文章添加标签
def add_article_tags(tags, article_obj):
    for tag in tags:
        # for 循环就表明tag存在
        if tag.isdigit():
            # 存在 直接关联
            article_obj.tag.add(tag)
        else:
            # 不存在 先创建 再关联
            tag_obj = Tags.objects.create(title=tag)
            article_obj.tag.add(tag_obj.nid)


# 文章
class ArticleView(View):
    # 添加文章
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
        # 默认作者和来源
        form.cleaned_data['author'] = '沐沐'
        form.cleaned_data['source'] = '前端沐沐个人博客'
        article_obj = Articles.objects.create(**form.cleaned_data)
        tags = data.get('tags')
        # 调用添加标签
        add_article_tags(tags, article_obj)
        res['code'] = 0
        res['data'] = article_obj.nid
        return JsonResponse(res)

    # 编辑文章
    def put(self, request, nid):
        res = {
            'msg': '文章编辑成功!',
            'code': 412,
            'data': None,
        }
        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg'] = '请求错误!'
            return JsonResponse(res)
        data = request.data
        data['status'] = 1

        form = AddArticleForm(data)
        if not form.is_valid():
            # 验证不通过
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过
        # 默认作者和来源
        form.cleaned_data['author'] = '沐沐'
        form.cleaned_data['source'] = '前端沐沐个人博客'
        article_query.update(**form.cleaned_data)
        tags = data.get('tags')
        # 标签修改
        # 清空所有标签
        article_query.first().tag.clear()
        # 调用添加标签
        add_article_tags(tags, article_query.first())
        res['code'] = 0
        res['data'] = article_query.first().nid
        return JsonResponse(res)


# 文章点赞
class ArticleDiggView(View):
    def post(self, request, nid):
        # nid评论id
        res = {
            'msg': '点赞成功！',
            'code': 412,
            'data': 0,
        }

        comment_query = Articles.objects.filter(nid=nid)
        comment_query.update(digg_count=F('digg_count') + 1)
        digg_count = comment_query.first().digg_count

        res['code'] = 0
        res['data'] = digg_count
        return JsonResponse(res)


# 文章收藏
class ArticleCollectsView(View):
    def post(self, request, nid):
        res = {
            'msg': '文章收藏成功！',
            'code': 412,
            'isCollects': True,
            'data': 0,
        }
        if not request.user.username:
            res['msg'] = '请登陆后操作！'
            return JsonResponse(res)
        # 判断是否已收藏
        collects_flag = request.user.collects.filter(nid=nid)
        print(collects_flag)
        num = 1
        res['code'] = 0
        if collects_flag:
            # 已收藏过该文章 点击为取消收藏
            res['msg'] = '文章取消收藏成功!'
            res['isCollects'] = False
            request.user.collects.remove(nid)
            num = -1
        else:
            request.user.collects.add(nid)
        article_query = Articles.objects.filter(nid=nid)
        article_query.update(collects_count=F('collects_count') + num)
        collect_count = article_query.first().collects_count
        res['data'] = collect_count
        return JsonResponse(res)
