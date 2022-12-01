from django import template

register = template.Library()


# 自定义过滤器
# @register.filter
# def add2(item):
#     return int(item) + 2

@register.inclusion_tag('my_tags/headers.html')
def banner(menu_name, article=None):
    print(menu_name, article)
    img_list = [
        "http://127.0.0.1:8000/media/site_bg/31.jpg",
        "http://127.0.0.1:8000/media/site_bg/29.jpg",
    ]
    if article:
        # 拿到文章封面
        cover = article.cover.url.url
        print(cover)
        img_list = [cover]
        pass
    return {'img_list': img_list}
