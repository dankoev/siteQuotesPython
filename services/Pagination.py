import math


class Paginator:
    number_pages = None
    split_number = None
    model = None
    model_filter = None
    filter_in = None

    def __init__(self, model, split_number=5, model_filter: str = '', filter_in: str = ''):
        self.split_number = split_number
        self.model_filter = model_filter
        self.model = model
        self.filter_in = filter_in
        print(self.filter_in)
        self.count_pages(self.split_number)

    def count_pages(self, split_number):
        if not self.model_filter:
            number_quotes = self.model.objects.count()
        else:
            number_quotes = self.model.objects.filter(keys__keyword=self.model_filter).count()
        pages = math.ceil(number_quotes / split_number)
        print('pag_pages:', pages)
        self.number_pages = pages

    def get_page_items(self, current_page):
        sp_n = self.split_number
        paginator = self.get_paginator(current_page)
        if not self.model_filter:
            page_objs = self.model.objects.all()[sp_n * (paginator['current'] - 1):sp_n * paginator['current']]
        else:
            page_objs = self.model.objects.filter(keys__keyword=self.model_filter)[
                        sp_n * (paginator['current'] - 1):sp_n * paginator['current']]
        items = {
            'pages': range(1, self.number_pages + 1),
            'page_objs': page_objs,
            'current_page': paginator['current'],
            'next_page': paginator['next'],
            'previous_page': paginator['previous'],
        }
        return items

    def get_paginator(self, current_page):

        paginator = {
            'current': None,
            'next': None,
            'previous': None,
        }
        print(current_page)
        if not current_page or current_page == '1':
            paginator['current'] = 1
            if current_page != self.number_pages:
                paginator['next'] = 2
            return paginator

        current_page = int(current_page)
        paginator['current'] = current_page
        if current_page == self.number_pages:
            paginator['previous'] = self.number_pages - 1
            return paginator

        paginator['previous'] = current_page - 1
        paginator['next'] = current_page + 1
        return paginator
