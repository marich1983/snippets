from django.http import Http404
from django.shortcuts import render, redirect
from . import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotAllowed
from MainApp.forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    form = SnippetForm()
    context = {
        'pagename': 'Добавление нового сниппета',
        'form': form
        }
   
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': models.Snippet.objects.all()

        }
    return render(request, 'pages/view_snippets.html', context)

def snippet_page(request, snip_id: int):
    try:
        snippet = models.Snippet.objects.get(id=snip_id)
    except ObjectDoesNotExist:
        return HttpResponse('Не найдено')


    context= {
        'pagename': 'Страница для сниппета',
        'snippet': snippet
        }
    return render(request, 'pages/snippet.html', context)

def create_snippet(request):
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list-snip") #URL для списка сниппетов
        return render(request, "pages/snippet.html", context={"form": form})
    return HttpResponseNotAllowed(["POST"], "Something wrong")
