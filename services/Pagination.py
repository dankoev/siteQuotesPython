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
        if current_page:
            current_page = int(current_page)
            if current_page == 1:
                previous_page = None
                if current_page == self.number_pages:
                    next_page = None
                else:
                    next_page = 2
            elif current_page == self.number_pages:
                previous_page = self.number_pages - 1
                next_page = None
            else:
                previous_page = current_page - 1
                next_page = current_page + 1
        else:
            current_page = 1
            previous_page = None
            if current_page == self.number_pages:
                next_page = None
            else:
                next_page = 2
        if not self.model_filter:
            page_objs = self.model.objects.all()[sp_n * (current_page - 1):sp_n * current_page]
        else:
            page_objs = self.model.objects.filter(keys__keyword=self.model_filter)[sp_n * (current_page - 1):sp_n * current_page]
        items = {
            'pages': range(1, self.number_pages + 1),
            'page_objs': page_objs,
            'current_page': current_page,
            'next_page': next_page,
            'previous_page': previous_page,
        }
        return items
