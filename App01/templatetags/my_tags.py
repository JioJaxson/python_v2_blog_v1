from django import template
from App01.utils.search import Search
from django.utils.safestring import mark_safe

register = template.Library()


# 自定义过滤器
# @register.filter
# def add2(item):
#     return int(item) + 2

@register.inclusion_tag('my_tags/headers.html')
def banner(menu_name, article=None):
    # print(menu_name, article)
    img_list = [
        "http://127.0.0.1:8000/media/site_bg/31.jpg",
        "http://127.0.0.1:8000/media/site_bg/29.jpg",
    ]
    if article:
        # 拿到文章封面
        cover = article.cover.url.url
        # print(cover)
        img_list = [cover]
        pass
    return {'img_list': img_list}

@register.simple_tag
def generate_order_html(request):
    order = request.GET.get('order', '')
    query_params = request.GET.copy()
    order = Search(
        order=order,
        order_list=[
            ('-change_date', '综合排序'),
            ('-create_date', '最新发布'),
            ('-look_count', '最多浏览'),
            ('-digg_count', '最多点赞'),
            ('-collects_count', '最多收藏'),
            ('-comment_count', '最多评论')
        ],
        query_params=query_params
    )
    return mark_safe(order.order_html())