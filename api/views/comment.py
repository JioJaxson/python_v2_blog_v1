from django.views import View
from django.http import JsonResponse
from django import forms
from api.views.login import clean_form
from App01.models import Comment, Articles
from django.db.models import F
from App01.utils.find_root_comment import find_root_comment
from App01.utils.sub_comment import find_root_sub_comment


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
        Articles.objects.filter(nid=nid).update(comment_count=F('comment_count') + 1)
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
        else:
            # 文章评论成功！
            Comment.objects.create(
                content=content,
                user=request.user,
                article_id=nid
            )
        res['code'] = 0
        return JsonResponse(res)

    # 删除评论
    def delete(self, request, nid):
        res = {
            'msg': '评论删除成功！',
            'code': 412,
        }
        # 登陆人
        login_user = request.user
        comment_query = Comment.objects.filter(nid=nid)

        # 评论人
        comment_user = comment_query.first().user
        # 文章id
        aid = request.data.get('aid')
        # 子评论的最终根id
        pid = request.data.get('pid')
        print(aid, pid, nid)
        if not (login_user == comment_user or login_user.is_superuser):
            # 登陆人不是评论人并且登陆人不是超级管理员
            res['msg'] = '用户验证失败！'
            return JsonResponse(res)

        if not pid:
            # 删除的是根评论
            # 算子评论数量
            lis = []
            find_root_sub_comment(comment_query.first(), lis)
            Articles.objects.filter(nid=aid).update(comment_count=F('comment_count') - len(lis)-1)

            pass
        else:
            # 可以删除
            # 一级根评论数同步
            Comment.objects.filter(nid=pid).update(comment_count=F('comment_count') - 1)
            # 文章总评论数-1
            Articles.objects.filter(nid=aid).update(comment_count=F('comment_count') - 1)
        comment_query.delete()
        res['code'] = 0

        return JsonResponse(res)
