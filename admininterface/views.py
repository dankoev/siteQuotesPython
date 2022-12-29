from django.shortcuts import render, redirect
from .models import Quotes, KeysWords
from .forms import QuotesForm, KeysWordsForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from services.Pagination import Paginator
from services.LoggingClass import LoggingClass
from .models import Logging


@login_required(login_url='login')
def index(request):
    paginator = Paginator(Quotes)
    current_page = request.GET.get('page')
    pag_items = paginator.get_page_items(current_page)
    quotes = pag_items['page_objs']
    context = {
        'title': 'Администрирование',
        'quotes': quotes,
        'pag_items': pag_items
    }
    return render(request, 'admininterface/index.html', context)


@login_required(login_url='login')
def create(request):
    keywords_list = []
    quote_form = QuotesForm()
    keyword_form = KeysWordsForm()
    if request.method == 'POST':
        keyword_form = KeysWordsForm(request.POST)
        quote_form = QuotesForm(request.POST)
        button = request.POST.get('Delete')
        if button:
            keywords_list = delete_keyword(request)
        else:
            if keyword_form.is_valid():
                keywords_list = create_keyword(request, keyword_form)
                quote_form = QuotesForm(request.POST)
            if quote_form.is_valid():
                keywords_list = request.POST.getlist('keywords_list')
                if not keywords_list:
                    messages.error(request, 'Добавьте хотя бы одно ключевое слово')
                else:
                    create_quote(keywords_list, quote_form)
                    print('quote created')
                    return redirect('admin')
    context = {
        'title': 'Создание цитаты',
        'quote_form': quote_form,
        'keyword_form': keyword_form,
        'keywords_list': keywords_list,
    }
    return render(request, 'admininterface/create.html', context)


def delete_keyword(request):
    keyword_delete = request.POST.get('Delete')
    keywords_list = request.POST.getlist('keywords_list')
    keywords_list.remove(keyword_delete)
    return keywords_list


def create_keyword(request, keyword_form):
    new_keyword = keyword_form.cleaned_data['keyword'].lower()
    keyword, created = KeysWords.objects.get_or_create(keyword=new_keyword)
    keywords_list = request.POST.getlist('keywords_list')
    if keywords_list.count(keyword.keyword):
        messages.error(request, 'Такое слово уже добавлено')
    else:
        keywords_list.append(keyword.keyword)
    return keywords_list


def create_quote(keywords_list, quote_form):
    quote_data = quote_form.cleaned_data
    quote = Quotes()
    quote.author = quote_data['author']
    quote.content = quote_data['content']
    quote.save()
    keywords = KeysWords.objects.filter(keyword__in=keywords_list)
    quote.keys.set(keywords)
    log_info = LoggingClass()
    log_info.add_notice("Пользователь добавил запись " + str(quote.id))


def edit_quote(keywords_list, quote_form, quote_id):
    quote_data = quote_form.cleaned_data
    quote = Quotes.objects.get(id=quote_id)
    quote.author = quote_data['author']
    quote.content = quote_data['content']
    quote.save()
    log_info = LoggingClass()
    log_info.add_notice("Пользователь отредактировал запись " + str(quote.id))
    keywords = KeysWords.objects.filter(keyword__in=keywords_list)
    quote.keys.set(keywords)


@login_required(login_url='login')
def delete(request):
    quote_id = request.GET.get('quote_id')
    quote = Quotes.objects.get(id=quote_id)
    if request.method == 'POST':
        log_info = LoggingClass()
        log_info.add_notice("Пользователь удалил запись" + str(quote.id))
        quote.delete()
        return redirect('admin')
    context = {
        'title': 'Удаление',
        'quote': quote
    }
    return render(request, 'admininterface/delete.html', context)


@login_required(login_url='login')
def edit(request):
    keyword_form = KeysWordsForm()
    keywords_list = []
    quote_id = request.GET.get('quote_id')
    quote = Quotes.objects.get(id=quote_id)
    for item in quote.keys.all():
        keywords_list.append(item.keyword)
    if request.method == 'POST':
        keyword_form = KeysWordsForm(request.POST)
        quote_form = QuotesForm(request.POST)
        button = request.POST.get('Delete')
        if button:
            keywords_list = delete_keyword(request)
        else:
            if keyword_form.is_valid():
                keywords_list = create_keyword(request, keyword_form)
            if quote_form.is_valid():
                keywords_list = request.POST.getlist('keywords_list')
                if not keywords_list:
                    messages.error(request, 'Добавьте хотя бы одно ключевое слово')
                else:
                    edit_quote(keywords_list, quote_form, quote_id)
                    print('quote created')
                    return redirect('admin')
    quote_form = QuotesForm(instance=quote)
    context = {
        'title': 'Создание цитаты',
        'quote_form': quote_form,
        'keyword_form': keyword_form,
        'keywords_list': keywords_list,
    }
    return render(request, 'admininterface/edit.html', context)


@login_required(login_url='login')
def logging(request):
    logging_info = Logging.objects.all()

    context = {
        'title': 'Информация о логировании',
        'logging_info': logging_info,
    }
    return render(request, 'admininterface/logging.html', context)