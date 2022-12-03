def find_root_comment(comment):
    # 找comment中的根评论
    if comment.parent_comment:
        # 有父级,说明还不是根评论
        # 递归
        return find_root_comment(comment.parent_comment)
    # 是根评论,返回
    return comment
