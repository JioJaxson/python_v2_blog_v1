from django.views import View
from django.http import JsonResponse
from markdown import markdown
from pyquery import PyQuery
from App01.models import Articles, Tags, Cover


class ArticleView(View):
    # 发布文章
    def post(self, request):
        res = {
            'msg': '文章发布成功!',
            'code': 412,
            'data': None,
        }
        data: dict = request.data
        print(data)
        title = data.get('title')
        # 校验标题
        if not title:
            res['msg'] = '请输入文章标题!'
            return JsonResponse(res)

        content = data.get('content')
        # 文章内容判断
        if not content:
            res['msg'] = '请输入文章内容!'
            return JsonResponse(res)

        recommend = data.get('recommend')

        # 必填项
        extra = {
            'title': title,
            'content': content,
            'recommend': recommend,
            'status': 1
        }

        abstract = data.get('abstract')
        # 简介判断
        if not abstract:
            # 解析文本前30内容
            abstract = PyQuery(markdown(content)).text()[:30]  # PyQuery解析文本内容 markdown解析markdown格式的内容
        extra['abstract'] = abstract

        category = data.get('category_id')
        if category:
            extra['category'] = category

        cover_id = data.get('cover_id')
        if cover_id:
            extra['cover_id'] = cover_id
        else:
            # 未上传封面 默认上次value为1的那张
            extra['cover_id'] = 1

        pwd = data.get('pwd')
        if pwd:
            extra['pwd'] = pwd
        # 添加文章
        article_obj = Articles.objects.create(**extra)
        # 标签
        tags = data.get('tags')
        if tags:
            for tag in tags:
                if not tag.isdigit():
                    tag_obj = Tags.objects.create(title=tag)
                    article_obj.tag.add(tag_obj)
                else:
                    article_obj.tag.add(tag)
        res['code'] = 0
        res['data'] = article_obj.nid
        return JsonResponse(res)
