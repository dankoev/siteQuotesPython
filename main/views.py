from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
import django.contrib.auth as dj_auth
from django.contrib.auth.models import User
from admininterface.models import Quotes, Logging
from .forms import LoginForm
from services.Pagination import Paginator
from services.LoggingClass import LoggingClass


def index(request):
    paginator = Paginator(Quotes)
    current_page = request.GET.get('page')
    pag_items = paginator.get_page_items(current_page)
    quotes = pag_items['page_objs']
    print(Quotes)
    context = {
        'title': 'Главная',
        'quotes': quotes,
        'pag_items': pag_items
    }
    return render(request, 'main/index.html', context)


def login(request):
    login_form = LoginForm()
    log_info = LoggingClass()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user and user.is_active:
                dj_auth.login(request, user)
                log_info.add_notice("login: " + username)
                return redirect('/')
            else:
                log_info.add_notice("Неудачная попытка входа пользователя: " + username)
                login_form.add_error(None, 'Неверное имя пользователя или пароль')
    context = {
        'title': 'Вход',
        'login_form': login_form
    }
    return render(request, 'main/login.html', context)


def logout(request):
    log_info = LoggingClass()
    log_info.add_notice("logout: " + str(dj_auth.get_user(request).username))
    dj_auth.logout(request)
    return redirect('/')


def about(request):
    return render(request, 'main/about.html')


def contact(request):
    return render(request, 'main/contact.html')


def search_result(request):
    search = request.GET.get('search')
    search.lower()
    log_info = LoggingClass()
    log_info.add_notice("Поиск цитаты с ключевым словом:  " + search)
    paginator = Paginator(Quotes, model_filter=search, filter_in='True')
    current_page = request.GET.get('page')
    pag_items = paginator.get_page_items(current_page)
    find_quotes = pag_items['page_objs']
    print(search)
    print(find_quotes)
    context = {
        'title': 'Результаты поиска',
        'quotes': find_quotes,
        'search_item': search,
        'pag_items': pag_items
    }
    return render(request, 'main/searchresult.html', context)
