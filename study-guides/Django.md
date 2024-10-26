# Django

## Puesta en marcha

1. Crear carpeta
```python
mkdir todo
cd todo
```
2. Crear entorno Virtual
```python
python -m venv .venv --prompt todo
```

3. Activar entorno Virtual
```python
source .venv/bin/activate
```

4. Intalar django
```python
pip instal django
```

5. Crear el proyecto
```python
django-admin startproject main .
```

6. Todo okey
```python
./manage.py check
```

7. Aplicar Migraciones
```python
./manage.py migrate
./manage.py runserver 
```

8. Crear usuario
```python
./manage.py createsuperuser 
```

## Crear la app

Por convención esta se crea el plural.
```python
./manage.py startapp posts 
```

- Instalar la app en settings.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts.apps.PostsConfig',
]
```

## Crear un modelo

dentro de models.py creamos el modelos que es basicamente un objeto que SIEMPRE hereda de models.Model.

```python
class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=120, unique=True)
    done = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    complete_before = models.DateTimeField(null=True, blank=True)
```

- SIEMPRE despues de crear o modificar el modelo creamos y aplicamos las migraciones

```python
./manage.py makemigrations
$ ./manage.py migrate
```

- Tipos de Campos que existen para el modelo

| Campo          | Descripción                                    | Parámetros relevantes          |
|----------------|------------------------------------------------|--------------------------------|
| BooleanField   | Representa un valor booleano.                  | default                        |
| CharField      | Representa una cadena de texto.                | max_length MOST!!              |
| DateField      | Representa una fecha.                          | auto_now_add, auto_now         |
| DateTimeField  | Representa una fecha/hora.                     | auto_now_add, auto_now         |
| DecimalField   | Representa un valor flotante (ideal para divisas). | max_digits, decimal_places |
| EmailField     | Representa un correo electrónico.              | max_length                     |
| FileField      | Representa un archivo (genérico).              | upload_to                      |
| FloatField     | Representa un valor flotante (genérico).       | default                        |
| ImageField     | Representa un archivo (de imagen).             | upload_to                      |
| IntegerField   | Representa un valor entero.                    | default                        |
| SlugField      | Representa un «slug».                          | max_length                     |
| TextField      | Representa una cadena de texto (amplia).       |                                |
| URLField       | Representa una «url».                          | max_length                     |

(Los max suelen ser potencias de 2 example: 32, 64, 128, 256, 512, 1024, ..)

- Campo unico
```python
unique = True
```

- Campos opcionales

| Campo          | Opcional con...            |
|----------------|----------------------------|
| CharField      | blank=True                 |
| EmailField     | blank=True                 |
| SlugField      | blank=True                 |
| TextField      | blank=True                 |
| Resto de campos| blank=True, null=True      |

## Registramos el admin del modelo

Para poder visualizarlo en la interfaz administrativa tenemos que creaalo en admin.py

```python
from .models import Task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'done', 'complete_before', 'description']
    prepopulated_fields = {'slug': ['name']}
```

(Recuerda importar el modelo‼️)

- El prepolated_fields permite rellenar campos automaticamente‼️ como en este caso seria el slug con el atributo name

## Añadir la app a las URL de primer nivel

añadir la url de la aplicación a los urls.py del **Main**

```python
from django.contrib import admin
from django.url import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls'))
]
```
(Recuerda importar el include‼️)

### Crea urls.py dentro de la app

Aquí iran todaslas urls de la app

```python
from django.urls import path

from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('<post_slug>/', views.post_detail, name='post-detail'),
]
```
**Importante siempre terminan en -> '/'** ‼️‼️

Estas pueden contener parametros variables, se colocan dentro de < --- > y existen conversores que podemos utilizar para cada tipo de dato

| Conversor                  | Ejemplo                       | Explicación                      |
|----------------------------|-------------------------------|----------------------------------|
| `path('<username>', ...)`        | `/guido/`                      | Por defecto se convierte a `str` |
| `path('<tag:str>', ...)`         | `/python/`                     | Conversión explícita a `str`     |
| `path('<post_id:int>', ...)`     | `/4673/`                       | Conversión explícita a `int`     |
| `path('<product_slug:slug>', ...)` | `/display-23-inches/`         | Conversión explícita a `str`     |
| `path('<token:uuid>', ...)`      | `/075194d3-6885-417e-a8a8-6c931e272f00/` | Conversión explícita a `UUID` |

- Ejemplo de urls
```python
urlpatterns = [
    path('', views.home, name='home'),
    path('task/<task_slug>/', views.task_detail, name='task-detail'),
    path('done/', views.done, name='done'),
    path('pending/', views.pending, name='pending'),
    path('add/', views.add_task, name='add-task'),
    path('task/<task_slug>/edit/', views.edit_task, name='edit-task'),
    path('task/<task_slug>/delete/', views.task_delete, name='task-delete'),
    path('task/<task_slug>/', views.toggle_task, name='toggle'),
]
```

## VIEWS

- Ejemplo de la view de un Home donde le estamos pasando un contexto con las variables que vamos a usar dentro de ella (num_tasks y tasks)
```python
def home(request):
    num_task = Task.objects.count()
    tasks = Task.objects.all()
    return render(request, 'tasks/home.html', {'num_task': num_task, 'tasks': tasks})
```

- Ejemplo de un detail
```python
def task_detail(request, task_slug):
    task = Task.objects.get(slug=task_slug)
    return render(request, 'tasks/task/detail.html', dict(task=task))
```

- Ejemplo de un done
```python
def done(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/done.html', {'tasks': tasks})
```

- Ejemplo de un add donde utilizamos formularios (revisa la parte de formularios!)
```python
def add_task(request):
    if request.method == 'GET':
        form = AddTaskForm()
    else:
        if (form := AddTaskForm(data=request.POST)).is_valid():
            task = form.save(commit=False)
            task.slug = slugify(task.name)
            task.save()
            return redirect('tasks:home')
    return render(request, 'tasks/add.html', dict(form=form))
```
(se puede retornar un render de una plantilla o un redirect hacia otra‼️)

- Ejemplo de un edit utilizando un formulario
```python
def edit_task(request, task_slug: str):
    task = Task.objects.get(slug=task_slug)
    if request.method == 'POST':
        if (form := EditTaskForm(request.POST, instance=task)).is_valid():
            task = form.save(commit=False)
            task.slug = slugify(task.name)
            task.save()
            return redirect('tasks:home')
    else:
        form = EditTaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', dict(task=task, form=form))
```

- Ejemplo de un delete utilizando formularios
```python
def task_delete(request, task_slug: str):
    task = Task.objects.get(slug=task_slug)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:home')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
```

- Ejemplo de un toggle 
```python
def toggle_task(request, task_slug: str):
    task = Task.objects.get(slug=task_slug)
    task.done = not task.done
    task.save()
    return redirect('tasks:home')
```

- Ejemplo de una view utilizando un try except para errores
```python
def toggle_task(request, task_slug: str):
    try:
        task = Task.objects.get(slug=task_slug)
    except Task.DoesNotExist:
        return HttpResponseNotFound("La tarea solicitada no existe.")
    task.done = not task.done
    task.save()
    messages.success(request, f"La tarea '{task.name}' ha sido actualizada.")
    return redirect('tasks:home')
```

primero pregunta si el objeto con ese slug existe de no ser así devuelve una respuesta 404, en cambio, si este existe le cambia el estado, lo salva en la base de datos, da un mensaje positivo y redirect al home

## TEMPLATES

- Creamos dos carpetas anidadas dentro de nuestra app **templates/app** (el nombre de nuestra app)

- Creamos el fichero base.html, que como su nombre lo indica, sera la base de todas nuestras plantillas
```python
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta http-equiv="x-ua-compatible" content="ie=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <title>{% block title %}TaskTrack{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'tasks/custom.css' %}">

  </head>

  <body>
     {% block body %}{% endblock body %}
     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
  </body>
  <footer class="footer"> &copy 2024 Nichole Louis</footer>
</html>
```

- Para poder usar nuestro base.html en nuestras otras plantillas hay que indicarselo de la siguiente manera

    - al princio hay que colocar **{% extends "tasks/base.html" %}**
    - abrir y cerrar nuestro bloque body **{% block body %}  {% endblock body %}**
```python
{% extends "tasks/base.html" %}
{% block title %}TaskTrack | Home{% endblock title %}
{% block body %}

Todo lo que querramos que vaya dentro de nuestro body

{% endblock body %}
```

- Variables usando {{}}
```python
<h1>{{ post.title }}</h1>
<p>{{ post.content }}</p>
```
(Previamente pasadas desde las view correspondiente)

- Bucle for
```python
<ul>
    {% for post in posts %}
        <li>{{ post }}</li>
    {% endfor %}
</ul>
```

se puede desempaquetar
```python
<div class="points">
{% for x, y in points %}
    <p>{{ x }},{{ y }}</p>
{% endfor %}
</div>
```

- Podemos usar el empty cuando, en caso de no tener ninguna data que mostar en nuestra nustra template no queremos que quede en blanco

```python
<ul>
    {% for post in posts %}
        <li>{{ post }}</li>
    {% empty %}
        <p>No posts so far!</p>
    {% endfor %}
</ul>
```

- condicionales
```python
<span class=
{% if post.num_visits > 1000 %}
    "highlight">Interesting!
{% else %}
    "regular">Not bad
{% endif %}
</span>
```

- Exiten filtro que nos ofrecen algunas funcionalidades en las plantillas

| Filtro                | Ejemplo                                               | Descripción                                                                                                                                                       |
|-----------------------|-------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `add`                 | `value = 5`<br>`{{ value|add:"2" }}` → `7`            | Suma el argumento al valor.                                                                                                                                       |
| `capfirst`            | `value = 'django'`<br>`{{ value|capfirst }}` → `Django` | Pasa a mayúsculas el primer carácter del valor.                                                                                                                   |
| `date`                | `value = datetime.date(2024, 10, 17)`<br>`{{ value|date:"d/m/Y" }}` → `17/10/2024` | Formatea un objeto de tipo fecha.                                                                          |
| `default`             | `value = None`<br>`{{ value|default:"empty" }}` → `empty` | Muestra el argumento si el valor es falso.                                                                               |
| `dictsort`            | `value = [{'name': 'Carry', 'age': 32}, {'name': 'Mike', 'age': 21}]`<br>`{{ value|dictsort:"age" }}` | Ordena una lista de diccionarios por la clave indicada.      |
| `divisibleby`         | `value = 15`<br>`{{ value|divisibleby:"5" }}` → `True` | Devuelve `True` si el valor es divisible por el argumento.                                                                 |
| `filesizeformat`      | `value = 123456789`<br>`{{ value|filesizeformat }}` → `117.7 MB` | Formatea el valor como tamaño de archivo legible.                                                                 |
| `first`               | `value = [6, 4, 8]`<br>`{{ value|first }}` → `6`      | Devuelve el primer elemento de una lista.                                                                                                                        |
| `get_digit`           | `value = 123456789`<br>`{{ value|get_digit:"2" }}` → `8` | Devuelve el dígito en la posición del argumento (de derecha a izquierda).                                                |
| `join`                | `value = ['x', 'y', 'z']`<br>`{{ value|join:"|" }}` → `x|y|z` | Une la lista usando el argumento.                                                                                       |
| `last`                | `value = [6, 4, 8]`<br>`{{ value|last }}` → `8`       | Devuelve el último elemento de una lista.                                                                                                                       |
| `length`              | `value = ['a', 'b', 'c']`<br>`{{ value|length }}` → `3` | Devuelve la longitud del valor.                                                                                           |
| `linebreaks`          | `value = 'Django is\nawesome'`<br>`{{ value|linebreaks }}` → `<p>Django is<br>awesome</p>` | Reemplaza los saltos de línea por el HTML `<p>`.                   |
| `linebreaksbr`        | `value = 'Django is\nawesome'`<br>`{{ value|linebreaksbr }}` → `Django is<br>awesome` | Reemplaza saltos de línea por `<br>`.                                          |
| `lower`               | `value = 'DJANGO IS AWESOME'`<br>`{{ value|lower }}` → `django is awesome` | Convierte el valor a minúsculas.                                      |
| `pluralize`           | `value = 2`<br>`{{ value|pluralize }}` → `s`          | Devuelve un sufijo plural cuando el valor es mayor que 1.                                                                                            |
| `random`              | `value = [6, 4, 8]`<br>`{{ value|random }}` → `4`     | Devuelve un elemento aleatorio de la lista dada.                                                                                                               |
| `slice`               | `value = [9, 3, 7, 2]`<br>`{{ value|slice:":2" }}` → `[9, 3]` | Devuelve un trozo de la lista.                                                                                        |
| `slugify`             | `value = 'Become a slug!'`<br>`{{ value|slugify }}` → `become-a-slug` | Convierte el valor a un `slug`.                                                   |
| `stringformat`        | `value = '3.141516'`<br>`{{ value|stringformat:".3f" }}` → `3.142` | Formatea el valor de acuerdo al argumento.                                         |
| `time`                | `value = datetime.now()`<br>`{{ value|time:"H:i" }}` → `04:32` | Formatea un objeto de tipo hora.                                                   |
| `timesince`           | `value = datetime.datetime()`<br>`{{ value|timesince }}` → `4 days, 6 hours` | Indica el tiempo pasado desde el valor.                           |
| `timeuntil`           | `value = datetime.datetime()`<br>`{{ value|timeuntil }}` → `6 days, 4 hours` | Indica el tiempo que falta hasta el valor.                         |
| `title`               | `value = 'django is awesome'`<br>`{{ value|title }}` → `Django Is Awesome` | Pone el valor en formato de título.                         |
| `truncatechars`       | `value = 'Welcome to our flight to Python World'`<br>`{{ value|truncatechars:7 }}` → `Welcome...` | Trunca el valor al número de caracteres dado.  |
| `truncatechars_html`  | `value = '<p>Welcome to Python World</p>'`<br>`{{ value|truncatechars_html:7 }}` → `<p>Welcome...</p>` | Igual, respetando etiquetas HTML.      |
| `truncatewords`       | `value = 'Welcome to our flight to Python World'`<br>`{{ value|truncatewords:4 }}` → `Welcome to our flight...` | Trunca el valor al número de palabras. |
| `truncatewords_html`  | `value = '<p>Welcome to Python World</p>'`<br>`{{ value|truncatewords_html:4 }}` → `<p>Welcome to our flight...</p>` | Igual, respetando etiquetas HTML.      |
| `upper`               | `value = 'django is awesome'`<br>`{{ value|upper }}` → `DJANGO IS AWESOME` | Convierte el valor a mayúsculas.                                       |
| `urlize`              | `value = 'Check out https://python.org'`<br>`{{ value|urlize }}` → `Check out <a href="https://python.org">python.org</a>` | Convierte el texto a enlace HTML.  |
| `wordcount`           | `value = 'Django is awesome!'`<br>`{{ value|wordcount }}` → `3` | Devuelve el número de palabras.                                                                         |
| `yesno`               | `value = 1`<br>`{{ value|yesno:"good,bad,regular" }}` → `good` | Devuelve el primer argumento si `True`, el segundo si `False`, el tercero si `None`.|

## FORMS

Permiten que el usuario pueda introducir información

### Formularios de MODELO

Estos se diseñan specificando al modelo al que estan vinculados

- Creamos un archivo dentro de nuestra app llamado forms.py

```python
from django import forms

from .models import Post


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'complete_before')
```

Siempre heredan de forms.ModelForm‼️

así se veria su template
``` python
<form method="post" novalidate>
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Enviar">
</form>
```
**No olvidel el novalidate**‼️
(Siempre llevan el {% csrf_token %})‼️

- Ejemplo de un form de edición (la vista esta en las views 🆙)
```python
class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'complete_before')
```

## Static

En caso de quere añadir un estatico (archivos css, img, ...)

1. Añadirlo en las urls.py de primer nivel osea las del main
```python
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

2. Creamos dos carpetas anidadas dentro de nuestra app **static/app** (nombre de la app)

3. Agregamos la siguiente linea en el principio de nuestro fichero base.html
```python
{% load static %}
```


