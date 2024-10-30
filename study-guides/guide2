# Índice

- [Iniciar entorno virtual](#iniciar-entorno-virtual)
- [Activar el entorno virtual](#activar-el-entorno-virtual)
- [Instalar dependencias de Django](#instalar-las-dependencias-de-django-en-el-proyecto)
- [Creación del proyecto](#creación-del-proyecto)
- [Crear superusuario](#después-de-crear-el-proyecto-deberemos-de-crear-un-superusuario)
- [Crear el archivo `.gitignore`](#si-sergio-no-nos-da-el-gitignore-lo-crearemos-introduciendo-esto)
- [Crear aplicaciones](#hacer-las-aplicaciones)
  - [Instalar aplicaciones en settings.py](#instalar-las-aplicaciones-en-la-configuración-de-django)
  - [Crear aplicación compartida `shared`](#importante-crear-una-aplicación-shared-para-los-usos-compartidos-entre-varias-aplicaciones)
- [Modelos](#modelos)
  - [Crear un modelo en una aplicación](#crear-un-modelo-en-una-aplicación)
  - [Migraciones](#migraciones)
  - [Panel administrativo](#panel-administrativo)
- [URLs](#urls)
  - [URLs de primer nivel](#urls-de-primer-nivel)
  - [URLs de segundo nivel](#urls-de-segundo-nivel)
- [Vistas](#vistas)
  - [Ejemplo de vistas de `tasks`](#ejemplo-exteso-de-task)
  - [Consejos sobre vistas](#acordarse)
- [Plantillas o Templates](#plantillas-o-templates)
  - [Herencia de plantillas](#incluir-plantillas)
  - [Usar variables](#para-usar-variables-en-nuestra-plantilla)
  - [Bucles](#bucles)
  - [Condicionales](#condicionales)
  - [Filtros](#filtros)
  - [Estáticos y CSS](#estáticos-css)
- [Formularios](#formularios)
  - [Formulario de creación](#formulario-de-creación)
  - [Formulario de clase](#formulario-de-clase)
  - [Formulario de modelo](#formulario-de-modelo)
  - [Formulario de edición](#formularios-de-edición)




---





# Iniciar entorno virtual

```bash  
python -m venv .venv --prompt (Nombre del proyecto)
```

# Activar el entorno virtual

```bash
source .venv/bin/activate
```
Aunque en la máquina virtual usaremos a o d para desactivar.

# Instalar las dependencias de django en el proyecto

``` bash
pip install django
```

# Creación del proyecto

```bash
django-admin startproject main .
```
Usaremos el punto para generar una carpeta en el mismo directorio en el que estamos.

Si no tenemos justfile, usaremos los siguientes comandos importantes:

```bash

./manage.py check

./manage.py migrate

./manage.py runserver

```

**Lo que hay que poner el documento justfile**:
```justfile

runserver:
    ./manage.py runserver

mm:
    ./manage.py makemigrations

m:
    ./manage.py migrate

c:
    ./manage.py check

sh:
    ./manage.py shell

apps app="":
    ./manage.py startapp {{app}} 

```

# Después de crear el proyecto deberemos de crear un superusuario

```bash

$ ./manage.py createsuperuser
Username (leave blank to use 'sdelquin'): admin
Email address: admin@example.com
Password:
Password (again):
Superuser created successfully.


```

Usar siempre admin admin, para que los test pasen.

# Si sergio no nos da el .gitignore, lo crearemos introduciendo esto:

```
.venv
db.sqlite3
*.pyc
.mypy_cache

```

----

# Hacer las aplicaciones.

Comando básico para crear las aplicaciones

```bash

./manage.py startapp (nombre-de-la-aplicacion)

```

## Instalar las aplicaciones en la configuración de Django

Iremos al fichero settings.py de main. Buscaremos INSTALLED_APPS y pondremos lo siguiente:

'nombredelaapp.apps.NombreAplicacionConfig'

Si tenemos dudas, entraremos en el ficheo apps.py de la aplicación.

## Importante, crear una aplicación shared para los usos compartidos entre varias aplicaciones

```bash

./manage.py startapp shared

```

----

# Modelos

## Crear un modelo en una aplicación.

Vamos a la carpeta models.py de la aplicación y empezamos a generar los modelos necesarios para que la aplicación funcione

Nota a tener en cuenta, poner en singular el modelo, pues en el panel de administrador nos lo pondra con la s.

#### Ejemplo de Post del profe:

```python

from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField(max_length=256)

```

#### Ejemplo de task:
```python

from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    description = models.TextField(max_length=250, blank=True)
    done = models.BooleanField(default=False)
    complete_before = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

```

Tener en consideración los slug para su posterior indentificación en las urls.
Es interesante poner algún campo único que lo utilizamos, para ello solo tendremos que poner unique=true.

> Si queremos campos opcionales deberemos de poner null=True, blank=True

## Migraciones

Una vez creados los modelos, tendremos que migrarlos para que Django las introduzca en nuestra base de datos.

Ejecutamos este comando, sino tenemos un justfile:

```bash

./manage.py makemigrations

```

y después el siguiente:

```bash

./manage.py migrate

```

Tenemos también la opción de ejecutarlo solo para una aplicación en concreto poniendo el nombre al final del comando.



## Panel administrativo

Deberemos entrar en el fichro admin.py de nuestra apliación y pondremos esto:

```python
from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

```

Si queremso que solo se muestren unos campos en concreto pondremos esto:

```python

from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'contents')

```


# Urls

Un paso de vital importancia, ponerle mucha atención. Este paso va ligado con las vistas.

> Consejo: Ir creando las vistas a la vez y poner el pass en vez de return, para poder tener una mayor organización.


## Urls de primer nivel

Estarán por defecto en la carpeta main de nuestro proyecto.

Para incluir las urls de segundo nivel a nuestro proyecto principal tendremos que utilizar include. que este se importa desde django.url

Ejemplo:

```python

from django.contrib import admin
from django.url import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls'))
]

```

Ejemplo más extenso con task:



## Urls de segundo nivel

Las urls que integrarán cada una de las aplicaciones.

Ejemplo de post:

```python

from django.urls import path

from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('<post_slug>', views.post_detail, name='post-detail'),
]

```
Ejemplo más extenso con task:

```python

from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.task_list, name='task-list'),
    path('done/', views.complete_tasks, name='complete-tasks'),
    path('pending/', views.pending_tasks, name='pending-tasks'),
    path('add/', views.add_task, name='add-task'),
    path('task/<task_slug>/', views.task_detail, name='task-detail'),
    path('task/<task_slug>/delete/', views.delete_task, name='delete-task'),
    path('task/<task_slug>/edit/', views.edit_task, name='edit-task'),
    path('task/<task_slug>/toggle/', views.toggle_status, name='toggle-status'),
]


```


>[!IMPORTANT]
> Las aplicaciones por defecto no tendrán el archivo urls.py creado, tendremos que crearlo. Además, en ese fichero deberemos de introducir un app_name=nombredelaplicacion

Para poder utilizar las vistas de nuestra aplicación, utilizaremos from . import views. Utilizamos el punto para indicar que es el mismo directorio que se encuentre urls.py

>Consejo: utilizar en el nombre de las vistas - en vez de _


# Vistas

Esto es lo que nos dará la posibilidad de controlar el contenido que queremos enviar como respuesta a una petición por parte del usuario (navegador) en el que nos encontremos.
Para ello crearemos funciones en el archivo views.py de la aplicación para crear la disposición que se nos indique.

Ejemplo exteso de task:

```python

def task_list(request):
    tasks = Task.objects.order_by('done')
    return render(request, 'tasks/task_list.html', dict(tasks=tasks, num_task=tasks.count()))


def complete_tasks(request):
    tasks = Task.objects.filter(done=True)
    title = 'Complete'
    return render(request, 'tasks/task_list.html', dict(tasks=tasks, title=title, complete=True))


def pending_tasks(request):
    tasks = Task.objects.filter(done=False)
    title = 'Pending'
    return render(request, 'tasks/task_list.html', dict(tasks=tasks, title=title, complete=False))


def add_task(request):
    if request.method == 'POST':
        if (form := AddTaskForm(request.POST)).is_valid():
            task = form.save(commit=False)
            task.slug = slugify(task.name)
            print('funciona')
            task.save()
            return redirect('tasks:task-list')
    else:
        form = AddTaskForm()
    return render(request, 'tasks/modifiers/add.html', dict(form=form))


def delete_task(request, task_slug: str):
    task = Task.objects.get(slug=task_slug)
    task.delete()
    return render(request, 'tasks/modifiers/delete.html')


def edit_task(request, task_slug: str):
    task = Task.objects.get(slug=task_slug)

    if request.method == 'POST':
        if (form := EditPostForm(request.POST, instance=task)).is_valid():
            task = form.save(commit=False)

            task.slug = slugify(task.name)

            task.save()

            return redirect('tasks:task-list')

    else:
        form = EditPostForm(instance=task)

    return render(request, 'tasks/modifiers/edit.html', dict(task=task, form=form))


def toggle_status(request, task_slug: str):
    task = Task.objects.get(slug=task_slug)
    task.done = not task.done
    task.save()
    return redirect('tasks:task-list')


def task_detail(request, task_slug: str):
    task = Task.objects.get(slug=task_slug)
    return render(request, 'tasks/task/detail.html', dict(task=task))


```

Es importante destacar de que las vistas reciben SIEMPRE una request. Por tanto, deberemos de pasarsela, si nuestra vista necesita otro parámetro como lo es el slug se lo pasaremos también.

> Tener en consideración: Si necesitamos que nuestra plantilla disponga de inyección de código se lo tendremos que pasar por contexto. Hay dos formas mediante dict() o hacer nosotros el diccionario a mano.

> Tener en consideración: La ruta de la plantilla que vamos a ejecutar tiene que tener la ruta del templates de la aplicación.

> Tener en consideración: Los nombre las vistas son importantes para después en nuestro proyecto usar url de django para solo poner el nombre de la app : el de la vista


## Acordarse.

Para derivar de una plantilla a una vista, utilizar url con el nombre de la vista a ejecutar y si necesitamos pasar parámetros utilizar espacio y añadirlo

Ejemplo:

```python

<a type="button" class="btn-close d-flex justify-content-end" href="{% url "tasks:delete-task" task.slug %}"></a>

```
En este ejemplo, utilizamos el contexto que se le paso a la plantilla, ejecutamos un bucle for y con la iteracción capturada (task) cojemos su slug.

---

# Plantillas o templates

Esta será una carpeta que tendremos que crear en nuestra aplicación. Así mismo, dentro de esta deberémos de crear otra carpeta con el mismo nombre que la aplicación.

Esto se hace para evitar que existan otras aplicaciones en nuestro proyecto que tengan los mismos nombre de plantillas y así ejecutemos la correcta en todo momento.

> Tip: Por lo general, se crea un archivo llamado base.html que dispondrá de todos los componentes generales que tendrá nuestro poyecto y este será heredado por las demás plantillas.

Para poder ejecutar la plantilla base en las otras tendremos que definir en base.html block que nos dispone django. En el ejemplo de más abajo se ve claro.

Ejemplo de que poner siempre:

Plantilla base:

```python

<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{% if title %}{{ title }} | {% endif %}Blog</title>
  </head>

  <body>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
  </body>
</html>


```

Plantilla que hereda:

```python

{% extends "base.html" %}

{% block content %}
    {% for post in posts %}
        <h3>{{ post }}</h3>
        <p>Read more <a href="{% url 'posts:post-detail' post.id %}">here</a></p>
    {% endfor %}
{% endblock %}


```

## Inclusión
Django nos permite externalizar partes de una plantilla a un fichero, para luego incluirlo desde la propia plantilla. Para ello se utiliza la etiqueta {% include %}.

Supongamos por ejemplo que disponemos de la siguiente plantilla para mostrar la cabecera de un «blog»:

shared/templates/header.html
```python
<div class="header">
    <h1>The ultimate blog</h1>
    <h2>{{ subtitle }}</h1>
</div>
```

Django nos ofrece dos modos de incluir la plantilla anterior:


Inclusión directa 
Inclusión con argumentos 
Se incluye la plantilla utilizando el contexto que viene desde la vista en el que tendremos algo como: {'subtitle': 'Check out our last posts!'}:

```python
{% include "header.html" %} 
```


## Para usar variables en nuestra plantilla

Mediante el contexto que le hemos pasado en la vista, accederemos a esos datos usando las llaves {}

Ejemplo con post:

```python

<h1>{{ post.title }}</h1>
<p>{{ post.content }}</p>

```

### Bucles

Utilizaremos la estructura de {%%} que nos ofrece django

Ejemplo de bucle:

```python
<ul>
    {% for post in posts %}
        <li>{{ post }}</li>
    {% endfor %}
</ul>

```
Podemos utilizar una cláusula de {%empty%} que se dispondra dentro del bucle for, después de lo que queremos hacer si este viene vacío.

Ejemplo:

```python

<ul>
    {% for post in posts %}
        <li>{{ post }}</li>
    {% empty %}
        <p>No posts so far!</p>
    {% endfor %}
</ul>

```

### Condicionales

Ejemplo básico:

```python

<span class=
{% if post.num_visits > 1000 %}
    "highlight">Interesting!
{% else %}
    "regular">Not bad
{% endif %}
</span>

```
Ejemplo extenso:

```python

{% block body %}
{% for task in tasks %}
<div class="container text-center mt-4 w-50">
  <div class="row">
    <div class="col">
      <div class="card text-start">
        <div class="card-header d-flex justify-content-between">
          {% if task.done %}
          <div class="text-decoration-line-through"><b>{{task.name}}</b></div>
          {% else %}
          <div><b>{{task.name}}</b></div>
          {% endif %}
          <a type="button" class="btn-close d-flex justify-content-end" href="{% url "tasks:delete-task" task.slug %}"></a>
        </div>
        <div class="card-body">
          <p class="card-text">{{task.description|truncatewords:20}}</p>
          
          <a href="{% url "tasks:task-detail" task.slug %}" class="btn btn-outline-primary "> Leer más</a>
          <a href="{% url "tasks:edit-task" task.slug %}" class="btn btn-outline-secondary"> Editar tarea</a>
        </div>
        <div class="card-footer text-body-secondary d-flex justify-content-between">
          <div class="d-inline p-x-12 p-y-8">
            {{task.created_at}}
          </div>
          <p class="status d-flex-start-end">
            {% if task.done %} 
            <a href="{% url "tasks:toggle-status" task.slug %}" class="btn btn-success">Completada ✅ </a>
            {% else %} 
            <a href="{% url "tasks:toggle-status" task.slug %}" class="btn btn-danger">Pendiente ❌</a>
            {% endif %}
        </a>
        </p>
        </div>
      </div>
      </div>
    </div>
</div>
{% empty %}
  {% if complete %}
    <h1 class="mt-4">No haz completado ninguna tarea 👨‍🏭</h1>
    <a href="{% url "tasks:pending-tasks" %}" class="btn btn-success mt-2">Completa alguna de tus tareas pendientes</a>
  {% else %}
    <h1 class="mt-4">Felicidades!! Haz completado todas tus tareas 🎉</h1>
    <a href="{% url "tasks:add-task" %}" class="btn btn-success mt-2">Inicia alguna tarea</a>
  {% endif %}
{% endfor %}

{% endblock body %}


```

> Tip: Los operadores son iguale sque en python

### Filtros

Tenemos todos los filtros en la tabla de sergio:

https://mkdocs.aprendepython.es/third-party/webdev/django/templates/#filtros


## Estáticos/CSS

Deberemos de crear un directorio dentro de la aplicación que se llame static y dentro otro que se llame como la aplicación que utilizamos. Seguiría el mismo parámetro como en templates.

En el main/urls.py deberemos de introducir lo siguiente:

```python

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

```

### Para acceder al css

Lo intersante de esto es utilizar load static de django en el lugar donde queremos aplicarlo. Por lo general, se dispone en base.html

```python

{% load static %}

<img src="<% static 'blog.svg' %>"/>
<img src="<% static 'posts/blog.svg' %>"/>

```


----


# Formularios

Deberemos de crear un fichero llamado forms.py en nuestra aplicación.

**Importante**: usar el formulario de modelo.

## Formulario de creación

### Formularios de plantillas

Este sería el formulario generado por el programador:

Ejemplo de sergio:

Este sería el html de la plantilla

```python

<form method="post">
    {% csrf_token %}
    <input type="text" name="post-title">
    <textarea name="post-content"></textarea>
    <input type="submit" value="Enviar">
</form>

```

codigo de la vista:

```python

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.text import slugify

from .models import Post

def add_post(request):
    if request.method == 'POST':
        post_title = request.POST.get('post-title')
        post_content = request.POST.get('post-content')
        if post_title and post_content:
            post_slug = slugify(post_title)
            Post.objects.create(
                title=post_title,
                content=post_content,
                slug=post_slug
            )
            return redirect('posts:post-list')
        else:
            return HttpResponse('Title and content are required!')
    return render(request, 'posts/add_post.html')

```

### Formulario de clase

Dentro del fichero forms.py que hemos creado deberemos de introducir lo siguiente:

```python

from django import forms

class AddPostForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

```
html:

```python

<form method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Enviar">
</form>

```

vista:

```python

from django.utils.text import slugify
from django.shortcuts import render, redirect

from .forms import AddPostForm
from .models import Post


def add_post(request):
    if request.method == 'POST':
        if (form := AddPostForm(request.POST)).is_valid():
            post_title = form.cleaned_data['title']
            post_content = form.cleaned_data['content']
            post_slug = slugify(post_title)
            Post.objects.create(
                title=post_title,
                content=post_content,
                slug=post_slug
            )
            return redirect('posts:post-list')
    else:
        form = AddPostForm()
    return render(request, 'posts/add_post.html', dict(form=form))


```

### Formulario de modelo

Dentro de forms.py

```python

from django import forms

from .models import Post


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')

```

Usaremos los modelos que dispondremos, esto es un ejemplo. **Cuidado con los nombres**

La plantilla:

```python

<form method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Enviar">
</form>

```

La vista:

```python


from django.shortcuts import redirect, render
from django.utils.text import slugify

from .forms import AddPostForm


def add_post(request):
    if request.method == 'POST':
        if (form := AddPostForm(request.POST)).is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.save()
            return redirect('posts:post-list')
    else:
        form = AddPostForm()
    return render(request, 'posts/add_post.html', dict(form=form))

```

## Formularios de edición

Realmente no es un formulario solo por sí, sino una modificación de los anteriores. Usaremos el de modelo.


En forms.py:

```python

from django import forms

from .models import Post


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')

```

En el html:

```python

<h1>Editando post "{{ post.title }}"</h1>

<form method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Guardar">
</form>

```

Donde todo cambia, en la vista:

```python

from django.shortcuts import redirect, render
from django.utils.text import slugify

from .forms import EditPostForm
from .models import Post


def edit_post(request, post_slug: str):
    post = Post.objects.get(slug=post_slug)
    if request.method == 'POST':
        if (form := EditPostForm(request.POST, instance=post)).is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.save()
            return redirect('posts:post-list')
    else:
        form = EditPostForm(instance=post)
    return render(request, 'posts/edit_post.html', dict(post=post, form=form))

```

## Widgets

Si necesitas añadir widgets a nuestros formularios ir a este enlace:
https://mkdocs.aprendepython.es/third-party/webdev/django/forms/#widgets


---

Importante:

1. Crear los modelos.
2. Poner lo del panel de administrador.
3. Crear las urls con las vistas.
4. Crea las vistas con los nombres y pass al final. Este pase y el anterior accerlo a la vez. Ir uno por uno.
5. Crear el template con sus respectivas plantillas html.
6. Ir rellenando las vistas una por una y probando si funcionan. **No hacerlas todas juntas!!!**
7. Comprobar los errores. Por lo general, son errores en los links.
