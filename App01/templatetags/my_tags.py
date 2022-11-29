from django import template

register = template.Library()


# 自定义过滤器
@register.filter
def add2(item):
    return int(item) + 2
