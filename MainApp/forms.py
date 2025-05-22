from django.forms import ModelForm
from MainApp.models import Snippet


class SnippetForm(ModelForm):
    class Meta:
       model = Snippet
       # Описываем поля, которые будем заполнять в форме
       fields = ['name', 'lang', 'code']
    
    # def clean_name(self):
    #     """Метод для проверки длины поля name"""
    #     snippet_name = self.changed_data.get("name")
    #     if snippet_name is not None and len(snippet_name) > 3:
    #         return snippet_name
    #     raise ValueError("Snippet's name is too short")
       

