from django.contrib import admin
from App01.models import *
from django.utils.safestring import mark_safe


# Register your models here.
# 注册

class ArticleAdmin(admin.ModelAdmin):
    def get_cover(self):
        if self.cover:
            return  mark_safe(f'<img src="{self.cover.url.url}" style="height:60px; width:100px; border-radius:5px">')
        return
    get_cover.short_description ='文章封面'

    def get_tags(self):
        tag_list = ', '.join([i.title for i in self.tag.all()])
        return tag_list
    get_tags.short_description ='文章标签'

    def get_title(self):
        return mark_safe(f'<a href="/article/{self.nid}/" target="_blank">{self.title}</a>')
    get_title.short_description ='文章'

    def get_edit_delete_btn(self):
        return mark_safe(f"""
        <a href="/backstage/edit_article/{self.nid}/" target="_blank">编辑</a>
        <a href="/admin/App01/articles/{self.nid}/delete/">删除</a>
        """)

    get_edit_delete_btn.short_description = '操作'

    def action_word(self,request,queryset):
        for obj in queryset:
            word = len(obj.content)
            obj.word = word
            obj.save()

    action_word.short_description='获取文章字数'
    actions = [action_word]


    list_display = [get_title, get_cover, get_tags, 'category',
                    'look_count', 'digg_count', 'comment_count',
                    'collects_count', 'word', 'change_date',
                    get_edit_delete_btn]




admin.site.register(Articles,ArticleAdmin)
admin.site.register(Tags)
admin.site.register(Cover)
admin.site.register(Comment)
admin.site.register(Avatars)
admin.site.register(UserInfo)
