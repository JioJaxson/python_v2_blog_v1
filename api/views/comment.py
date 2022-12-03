from django.views import View
from django.http import JsonResponse
from django import forms
from api.views.login import clean_form
from App01.models import Comment


class CommentView(View):
    # 发布评论
    def post(self, request, nid):
        # /api/article/2/comment/
        # 文章id  nid
        # 用户
        # 评论内容
        res = {
            'msg': '文章评论成功！',
            'code': 412,
            'self': None,
        }
        data = request.data
        if not request.user.username:
            res['msg'] = '请登陆！'
            return JsonResponse(res)
        content = data.get('content')
        if not content:
            res['msg'] = '请输入评论内容！'
            res['self'] = 'content'
            return JsonResponse(res)
        # 文章评论成功！
        Comment.objects.create(
            content=content,
            user=request.user,
            article_id=nid
        )
        res['code'] = 0
        return JsonResponse(res)
