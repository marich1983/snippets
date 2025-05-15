from django.http import Http404
from django.shortcuts import render, redirect
from . import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': models.Snippet.objects.all()

        }
    return render(request, 'pages/view_snippets.html', context)

def snippet_page(request, snip_id):
    try:
        snippet = models.Snippet.objects.get(id=snip_id)
    except ObjectDoesNotExist:
        return render(request, HttpResponse('Не найдено'))


    context= {
        'pagename': 'Старница для сниппета',
        'snippet': snippet
        }
    return render(request, 'pages/snippet.html', context)

