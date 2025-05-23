from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotAllowed
from MainApp.forms import SnippetForm
from django.contrib import auth, messages


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


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
            return redirect("list-snip") #URL для списка сниппетов
        return render(request, "pages/snippet.html", context={"form": form})
    
def del_snippet(request, snip_id):
    # Найти сниппед по id или 404
    if request.method == "GET" or request.method == "POST":
        snippet = get_object_or_404(models.Snippet, id=snip_id)
        snippet.delete()
        messages.success(request, "Успешное удаление")
    return redirect('list-snip')


def edit_snippet(request, snip_id):
    snippet = get_object_or_404(models.Snippet, id=snip_id)
    if request.method == "GET":
        context = {
            'form': SnippetForm(instance=snippet), 
            'id': snip_id}
        return render(request,'pages/add_snippet.html',context)
    
    elif request.method == 'POST':
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            messages.success(request, "Сохранено успешно")
            return redirect('list-snip')
        else:
            return render(request,'pages/add_snippet.html',{'form':form})




def snippets_page(request):
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': models.Snippet.objects.all()
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
