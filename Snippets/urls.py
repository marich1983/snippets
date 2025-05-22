from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page),
    path('snippets/add', views.add_snippet_page, name="add-snip"),
    path('snippets/list', views.snippets_page, name="list-snip"),
    path('snippets/<int:snip_id>', views.snippet_page, name="snippet"),
    path('snippets/create', views.create_snippet, name="create-snippet"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
