# Ejemplos de modelos y vistas

Ejemplo de TAG:

```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tag = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```


```python
from django.urls import path
from . import views

urlpatterns = [
    path('articles/<str:tag>/', views.articles_by_tag, name='articles-by-tag'),
]
```

```python
from django.shortcuts import render
from .models import Article

def articles_by_tag(request, tag):
    articles = Article.objects.filter(tag=tag)
    return render(request, 'articles/articles_by_tag.html', {'articles': articles, 'tag': tag})

```

Ejemplo de UUID: 

```python
from django.db import models
import uuid

class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

```python
from django.urls import path
from . import views

urlpatterns = [
    path('document/<uuid:uuid>/', views.document_detail, name='document-detail'),
]
```

```python
from django.shortcuts import render, get_object_or_404
from .models import Document

def document_detail(request, uuid):
    document = get_object_or_404(Document, uuid=uuid)
    return render(request, 'documents/detail.html', {'document': document})
```
