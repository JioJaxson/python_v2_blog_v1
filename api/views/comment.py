from django.views import View
from django.http import JsonResponse
from django import forms
from api.views.login import clean_form
from App01.models import Comment, Articles
from django.db.models import F
from App01.utils.find_root_comment import find_root_comment


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

        pid = data.get('pid')
        # 文章评论数加1
        Articles.objects.filter(nid=pid).update(comment_count=F('comment_count') + 1)
        if pid:
            # 不是根评论
            comment_obj = Comment.objects.create(
                content=content,
                user=request.user,
                article_id=nid,
                parent_comment_id=pid,
            )
            # 根评论数加1
            # 找到最终根评论
            root_comment_obj = find_root_comment(comment_obj)
            root_comment_obj.comment_count += 1
            root_comment_obj.save()
            # Comment.objects.filter(nid=pid).update(comment_count=F('comment_count') + 1)
        else:
            # 文章评论成功！
            Comment.objects.create(
                content=content,
                user=request.user,
                article_id=nid
            )
        res['code'] = 0
        return JsonResponse(res)
