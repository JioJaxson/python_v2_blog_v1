from django.contrib import admin
from App01.models import Articles #导入文章表
from App01.models import Tags #导入文章表
from App01.models import Cover #导入文章表
# Register your models here.
# 注册
admin.site.register(Articles)
admin.site.register(Tags)
admin.site.register(Cover)
