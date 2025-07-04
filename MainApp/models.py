from django.db import models
from django.contrib.auth.models import User

LANGS = (
    ("py", "Python"),
    ("js", "JavaScript"),
    ("go", "Golang"),
    ("cpp", "C++"),
    ("html", "HTML"),
)




class Snippet(models.Model):
    class Meta:
        ordering = ['name', 'lang']   # Для сортировки по имени и языку

    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANGS)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    public = models.BooleanField(default=True) # True = public, False = private

    def __repr__(self):
        return f'Snippet({self.name},{self.lang})'


class Comment(models.Model):
    text = models.TimeField(max_length=1000, verbose_name="Текст комментария")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Автор")
    snippet = models.ForeignKey(to=Snippet, on_delete=models.CASCADE, verbose_name="Сниппет", related_name='comments')
