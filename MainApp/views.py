
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotAllowed
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

@login_required
def add_snippet_page(request):
    # Создаем пустую форму при запросе ГЕТ
    if request.method == "GET": 
        form = SnippetForm()
        context = {
            'pagename_add': 'Добавление нового сниппета',
            'pagename_edit': 'Редактирование сниппета',
            'form': form
            }
        return render(request, 'pages/add_snippet.html', context)
    
    # Получаем данные из формы и на их основе создаем новый сниппет, сохраняя в БД
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False) # получаем экземпляр класса Snippet
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            # GET/ Snippet/list
            return redirect("my-snippets") #URL для списка сниппетов
        return render(request, "pages/add_snippet.html", context={"form": form})
    
@login_required    
def del_snippet(request, snip_id):
    # Найти сниппед по id или 404
    if request.method == "GET" or request.method == "POST":
        snippet = get_object_or_404(models.Snippet.objects.filter(user=request.user), id=snip_id)
        snippet.delete()
        messages.success(request, "Успешное удаление")
    return redirect("my-snippets")

@login_required
def edit_snippet(request, snip_id):
    context = {'pagename': "Обновление сниппета"}
    snippet = get_object_or_404(models.Snippet.objects.filter(user=request.user), id=snip_id)
    # Создаем форму на основе данных сниппета при запросе ГЕТ
    if request.method == "GET":
        context['form'] = SnippetForm(instance=snippet)
        context['id'] = snip_id

        return render(request,'pages/add_snippet.html',context)
    
    # Получаем данные из формы и на их основе обновляем спиппет, сохраняя его в БД
    if request.method == 'POST':
        data_form = request.POST
        snippet.name = data_form['name']
        snippet.code = data_form['code']
        snippet.public = data_form.get('public', False)
        snippet.save()
        
        return redirect("my-snippets")




def snippets_page(request):
    snippets = models.Snippet.objects.filter(public=True)
    if request.user.is_authenticated:
        snippets = models.Snippet.objects.filter(Q(public=True) | Q(user=request.user))
    context = {
            'pagename': 'Просмотр всех сниппетов',
            'snippets': snippets
            }

    return render(request, 'pages/view_snippets.html', context)

@login_required
def my_snippets(request):
    snippets = models.Snippet.objects.filter(user=request.user)
    context = {
            'pagename': 'Мои сниппеты',
            'snippets': snippets
            }
    return render(request, 'pages/view_snippets.html', context)

    

def snippet_page(request, snip_id: int):
    context= {
        'pagename': 'Страница для сниппета'
        }
    try:
        snippet = models.Snippet.objects.get(id=snip_id)
    except ObjectDoesNotExist:
        return render(request, 'pages/errors.html', context | {"error": f"Snippet with id={snip_id} not found."})

    else:
        context['snippet'] = snippet
        context['comment_form'] = CommentForm()
        return render(request, 'pages/snippet.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                "pagename": "PythonBin",
                "errors": ["Wrong username or password"]
            }

            return render(request, "pages/index.html", context)
    return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect('home')

def register(request):
    context = {
            'pagename_add': 'Регистрация нового пользователя',
            }
    # Создаем пустую форму при запросе ГЕТ
    if request.method == "GET": 
        form = UserRegistrationForm()

    # Получаем данные из формы и на их основе создаем нового пользователя, сохраняя его в БД
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home") 
    context['form'] = form
    return render(request, "pages/registration.html", context)

@login_required
def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            snippet_id = request.POST.get("snippet_id")
            snippet = models.Snippet.objects.get(id=snippet_id)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()
       
        return redirect('snippet', snip_id=snippet.id)
    raise Http404


