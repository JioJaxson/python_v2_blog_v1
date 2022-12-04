from django import template

register = template.Library()


# 自定义过滤器
# 用户是否收藏了该文章
@register.filter
def is_user_collects(article, request):
    if str(request.user) == 'AnonymousUser':
        # 没有登陆
        return ''
    if article in request.user.collects.all():
        return 'show'
    return ''
