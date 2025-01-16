from django.shortcuts import render
from django.http import HttpResponse
from tovari.models import Categories




def index(request):


    context: dict = {
        'title': 'Madi Главная',
        'content': 'Магазин мебели Мади',
    }
    return render(request, 'shop/index.html', context)

def about(request):
    context: dict = {
        'title': 'Madi про нас',
        'content': 'ОБО МНЕ',
        'text': 'Мади (имя): Имя "Мади" распространено в странах Центральной Азии, особенно в Казахстане. Оно может быть как самостоятельным именем, так и сокращением от других имен. В казахском языке оно ассоциируется с именами, которые включают корень "мад" или "мадияр", что может означать "помощник" или "человек, помогающий другим".'
    }
    return render(request, 'shop/about.html', context)


def contacts(request):
    context = {
        'title': 'КОНТАКТЫ',
        'content': 'КОНТАКТЫ',
        'text': 'ТЕЛЕФОН',
    }
    return render(request, 'shop/contacts.html', context)

