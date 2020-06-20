class Pagination:

    def __init__(self, request, data_length, per_num=10, max_show=11):
        try:
            page = int(request.GET.get('page', 1))
            if page <= 0:
                page = 1
        except Exception:
            page = 1

        # 每页显示的数据条数

        # per_num = 10

        # 总的页码数
        total_num, more = divmod(data_length, per_num)
        if more:
            total_num += 1

        # 要显示的页码数
        # max_show = 11
        half_show = max_show // 2
        if total_num <= max_show:
            # 页码的起始值
            page_start = 1
            # 页码的终止值
            page_end = total_num
        else:
            # 处理左边的极值
            if page - half_show <= 0:
                page_start = 1
                page_end = max_show
            elif page + half_show >= total_num:
                page_start = total_num - max_show + 1
                page_end = total_num
            else:
                page_start = page - half_show
                page_end = page + half_show

        page_list = ['<nav aria-label="Page navigation"><ul class="pagination">']

        if page == 1:

            page_list.append(
                '<li class="disabled"><a ><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            page_list.append(
                '<li><a href="?page={}" ><span aria-hidden="true">&laquo;</span></a></li>'.format(page - 1))

        for i in range(page_start, page_end + 1):

            if i == page:
                page_list.append('<li class="active"><a href="?page={}">{}</a></li>'.format(i, i))
            else:
                page_list.append('<li><a href="?page={}">{}</a></li>'.format(i, i))

        if page == total_num:

            page_list.append(
                '<li class="disabled"><a ><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            page_list.append(
                '<li><a href="?page={}" ><span aria-hidden="true">&raquo;</span></a></li>'.format(page + 1))

        page_list.append('</ul></nav>')
        self.page_html = ''.join(page_list)

        # 切片的起始值
        self.start = (page - 1) * per_num
        # 切片的终止值
        self.end = page * per_num
