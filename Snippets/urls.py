from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name="add-snip"),
    path('snippets/<user>', views.snippets_page, name="list-snip"),
    path('snippets/<int:snip_id>', views.snippet_page, name="snippet"),
    path('snippets/<int:snip_id>/delete', views.del_snippet, name="del-snippet"),
    path('snippets/<int:snip_id>/edit', views.edit_snippet, name="edit-snippet"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
