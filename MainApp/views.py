from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotAllowed
from MainApp.forms import SnippetForm
from django.contrib import auth


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    # Создаем пустую форму при запросе ГЕТ
    if request.method == "GET": 
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
            }
        return render(request, 'pages/add_snippet.html', context)
    
    # Получаем данные из формы и на их основе создаем новый сниппет, сохраняя в БД
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            # GET/ Snippet/list
            return redirect("list-snip") #URL для списка сниппетов
        return render(request, "pages/snippet.html", context={"form": form})
    
def del_snippet(request, snip_id):
    context = {
        'pagename': 'Удаление сниппета',
        }
    # Найти сниппед по id или 404
    if request.method == "GET" or request.method == "POST":
        snippet =get_object_or_404(models.Snippet, id=snip_id)
        snippet.delete()
    return redirect('list-snip')


def edit_snippet(request, snip_id):
    context = {
        'pagename': 'Редактирование сниппета',
        }
    return render(request, "pages/edit_snippet.html", context)


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

# def create_snippet(request):
#     if request.method == "POST":
#         form = SnippetForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # GET/ Snippet/list
#             return redirect("list-snip") #URL для списка сниппетов
#         return render(request, "pages/snippet.html", context={"form": form})
#     return HttpResponseNotAllowed(["POST"], "Something wrong")

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print("username =", username)
        # print("password =", password)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            pass
    return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect('home')
