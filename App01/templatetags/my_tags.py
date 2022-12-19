from django import template
from App01.utils.search import Search
from django.utils.safestring import mark_safe
from App01.models import Tags

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
def generate_order_html(request, key):
    order = request.GET.get(key, '')
    order_list = []
    if key == 'order':
        order_list = [
            ('', '综合排序'),
            ('-create_date', '最新发布'),
            ('-look_count', '最多浏览'),
            ('-digg_count', '最多点赞'),
            ('-collects_count', '最多收藏'),
            ('-comment_count', '最多评论')
        ]
    elif key == 'word':
        order = request.GET.getlist(key, '')
        if order == '':
            order = ['']
        order_list = [
            ([''], '全部文章'),
            (['0', '100'], '100字以内'),
            (['100', '500'], '500字以内'),
            (['500', '1000'], '1000字以内'),
            (['1000', '3000'], '3000字以内'),
            (['3000', '5000'], '5000字以内'),
            (['5000', '10000'], '10000字以内'),
            (['10000', '999999999'], '10000字以上'),
        ]
    elif key == 'tag':
        tag_list = Tags.objects.exclude(articles__isnull=True)
        order_list.append(('', '全部标签'))
        for tag in tag_list:
            order_list.append((tag.title, tag.title))
    query_params = request.GET.copy()


    order = Search(
        key=key,
        order=order,
        order_list=order_list,
        query_params=query_params
    )
    return mark_safe(order.order_html())