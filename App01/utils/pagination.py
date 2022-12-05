import math


class Pagination:
    def __init__(self, current_page, all_count, base_url, query_params, per_page=20, pager_page_count=11):
        self.all_count = all_count
        self.per_page = per_page
        # 计算一共有多少页码
        # 1: 取余
        # div, p = divmod(all_count, per_page)
        # if p != 0:
        #     div += 1
        # self.current_count = div

        # 2 : 进位
        self.current_count = math.ceil(all_count / per_page)

        # 只能是满足条件的数字
        try:
            self.current_page = int(current_page)
            if not 0 < self.current_page <= self.current_count:
                self.current_page = 1
        except Exception:
            self.current_page = 1

        self.base_url = base_url
        self.query_params = query_params
        self.pager_page_count = pager_page_count

        print('当前页面:', self.current_page, '当前总页数:', self.current_count)

        # 分页 的中值
        self.half_pager_count = int(self.pager_page_count / 2)
        if self.current_count < self.pager_page_count:
            # 当前可分页页码<最大分页数  就让最大分页页变成可分页页码
            self.pager_page_count = self.current_count

    def page_html(self):
        # 计算页码的起始和结束
        start = self.current_page - self.half_pager_count
        end = self.current_page + self.half_pager_count
        if self.current_page <= self.half_pager_count:
            # 在最左侧
            start = 1
            end = self.pager_page_count
        if self.current_page + self.half_pager_count >= self.current_count:
            # 在最右侧
            start = self.current_count - self.pager_page_count
            end = self.current_count
        print(start, end)

        # 生成分页
        page_list = []

        # 上一页
        if self.current_page != 1:
            self.query_params['page'] = self.current_page - 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}">上一页</a></li>')

        # 数字部分
        for i in range(start, end + 1):
            self.query_params['page'] = i
            if self.current_page == i:
                li = f'<li class="active"><a href="{self.base_url}?{self.query_encode}">{i}</a></li>'
            else:
                li = f'<li><a href="{self.base_url}?{self.query_encode}">{i}</a></li>'
            page_list.append(li)

        # 下一页
        if self.current_page != self.current_count:
            self.query_params['page'] = self.current_page + 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}">下一页</a></li>')
        return ''.join(page_list)

    @property
    def query_encode(self):
        return self.query_params.urlencode()

    # 加 @property 后面调用可以不用加()
    @property
    def start(self):
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        return self.current_page * self.per_page


if __name__ == '__main__':
    pager = Pagination(
        current_page=20,
        all_count=100,
        base_url='/article',
        query_params={'tag': 'python'},
        per_page=5,
        pager_page_count=10
    )
    # print('页面开始索引值:', pager.start, '页面结束索引值:', pager.end)
    print(pager.page_html())
