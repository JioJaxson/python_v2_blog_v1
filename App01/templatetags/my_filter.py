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

# 判断是否有文章内容
@register.filter
def is_article_list(article_list):
    if len(article_list):
        return 'search_content'
    return 'no_content'
