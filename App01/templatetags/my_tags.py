from django import template

register = template.Library()


# 自定义过滤器
# @register.filter
# def add2(item):
#     return int(item) + 2

@register.inclusion_tag('my_tags/headers.html')
def banner(menu_name):
    print(menu_name)
    img_list = [
        "http://127.0.0.1:8000/media/site_bg/31.jpg",
        "http://127.0.0.1:8000/media/site_bg/29.jpg",
    ]
    return {'img_list': img_list}
