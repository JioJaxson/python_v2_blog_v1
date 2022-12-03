import os

if __name__ == '__main__':
    # 加载django配置信息
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'V1_Blog.settings')
    # 导入Django 并启动Django项目
    import django

    django.setup()

    from App01.models import Articles, Comment


    # 思路：
    # 根据根评论递归查找所有子评论 并放到根评论的一个空间里

    def find_root_sub_comment(root_comment, sub_comment_list):
        for sub_comment in root_comment.comment_set.all():
            # 找根评论的子评论
            sub_comment_list.append(sub_comment)
            find_root_sub_comment(sub_comment, sub_comment_list)


    # 找到某个文章的所有评论
    comment_query = Comment.objects.filter(article_id=1)
    # 把评论存储到列表
    comment_list = []

    for comment in comment_query:
        if not comment.parent_comment:
            # 递归查找这个根评论下的所有子评论
            lis = []
            find_root_sub_comment(comment, lis)
            comment.sub_comment = lis
            comment_list.append(comment)
            continue
    for comment in comment_list:
        print(comment)
        for sub_comment in comment.sub_comment:
            print(sub_comment)
