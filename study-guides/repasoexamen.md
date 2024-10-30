# Repaso ToDo app

## Modelo
```python
from django.db import models

class Task(models.Model):
    name = models.CharField(max_length= 100)
    description = models.TextField()
    slug = models.SlugField(max_length=120, unique=True)
    done = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    complete_before = models.DateTimeField(null=True, blank=True)
```

## Vistas
```python
from django.shortcuts import render, redirect
from .models import Task
from django.utils.text import slugify
from .forms import AddTaskForm, EditTaskForm

def home(request):
    tasks = Task.objects.all()
    num_task = Task.objects.count()
    return render(request, "tasks/home.html", {'num_task': num_task, 'tasks': tasks})

def task_detail(request, task_slug):
    task = Task.objects.get(slug=task_slug)
    return render(request, "tasks/task/detail.html", dict(task=task))

def done(request):
    tasks = Task.objects.filter(done=True)
    return render(request, "tasks/done.html", dict(tasks=tasks))

def add_task(request):
    if request.method == 'POST':
        if (form := AddTaskForm(request.POST)).is_valid():
            task = form.save(commit=False)
            task.slug = slugify(task.name)
            task.save()
            return redirect('tasks:home')
    else:
        form = AddTaskForm()
    return render(request, 'tasks/add.html', dict(form=form))
    

def edit_task(request, task_slug):
    task = Task.objects.get(slug=task_slug)

    if request.method == 'POST':
        if (form := EditTaskForm(request.POST, instance=task)).is_valid():
            task = form.save(commit=False)

            task.slug = slugify(task.name)

            task.save()

            return redirect('tasks:home')

    else:
        form = EditTaskForm(instance=task)

    return render(request, 'tasks/edit.html', dict(task=task, form=form))


def delete_task(request, task_slug):
    task = Task.objects.get(slug=task_slug)
    task.delete()
    return redirect("tasks:home")

def toggle_task(request, task_slug):
    task = Task.objects.get(slug=task_slug)
    task.done = not task.done
    task.save()
    return redirect('tasks:task-detail', task_slug=task.slug)
```
## URLS

### Primer nivel
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),

]
```

### Segundo nivel
```python
from django.urls import path

from . import views


app_name = 'tasks'

urlpatterns = [
    path('', views.home, name='home'),
    path('task/<task_slug>/', views.task_detail, name='task-detail'),
    path('done/', views.done, name='done'),
    path('add-task/', views.add_task, name='add-task'),
    path('task/<task_slug>/edit/', views.edit_task, name='edit-task'),
    path('task/<task_slug>/delete/', views.delete_task, name='delete-task'),
    path('task/<task_slug>/toggle/', views.toggle_task, name='toggle'),
    
    ]
```

## Forms
```python
from django import forms

from .models import Task


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'complete_before')

class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'complete_before')
```

## Templates

### Base
```python
{% load static %}
<!DOCTYPE html>
<html lang="en">
  <head>
        <meta charset="utf-8" />
        <meta http-equiv="x-ua-compatible" content="ie=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

    <title>{% block title %}Super ToDo{% endblock %}</title>

  </head>

  <body>
     {% block body %}{% endblock body %}
     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
  </body>
  <footer class="footer"> &copy 2024 Nichole Louis</footer>
</html>
```

### Home
```python
{%extends "tasks/base.html"%}
{%block body%}
{%for task in tasks%}
    {{task.name}} 
    <a href="{% url 'tasks:task-detail' task.slug%}">aquí más</a>
    <br>
    <a href="{% url 'tasks:edit-task' task.slug%}">editame</a>
{% endfor %}

<a href="{% url 'tasks:done'%}">dones</a>
<a href="{% url 'tasks:add-task'%}">añade</a>
{%endblock body%}
```
### Add
```python
{%extends "tasks/base.html"%}
{%block body%}
<form method="post" novalidate>
    {% csrf_token %}
    {{ form.as_p }}
    <div class="d-grid gap-2">
        <input type="submit" class="btn btn-primary btn-lg" style="background-color: #258626; border: none;" value="Create Task">
    </div>
</form>
{%endblock body%}
```

### Edit
```python
{%extends "tasks/base.html"%}
{%block body%}
<form method="post" novalidate>
    {% csrf_token %}
    {{ form.as_p }}
    <div class="d-grid gap-2">
        <input type="submit" class="btn btn-primary btn-lg" style="background-color: #258626; border: none;" value="Create Task">
    </div>
</form>
{%endblock body%}
```

### Detail
```python
{%extends "tasks/base.html"%}
{%block body%}
    {{task.name}}
    <br>
    {{task.description}}
    <br>
    <a href="{% url 'tasks:home'%}">back</a>
    <form action="{% url 'tasks:delete-task' task.slug %}" method="post" style="display:inline;">
        {% csrf_token %} <!-- Token CSRF para proteger contra ataques -->
        <button type="submit" onclick="return confirm('Are you sure you want to delete this task?');">Delete</button>
    </form>
    <form action="{% url 'tasks:toggle' task.slug %}" method="post" style="display:inline;">
        {% csrf_token %}
        <button type="submit">{{ task.done|yesno:"Mark as Pending, Mark as Done" }}</button>
    </form>
{%endblock body%}
```

### Done
```python
{%extends "tasks/base.html"%}
{%block body%}
{%for task in tasks%}
    {{task.name}} 
    <a href="{% url 'tasks:task-detail' task.slug%}">aquí más</a>

{%empty%}
{% endfor %}

<a href="{% url 'tasks:home'%}">back</a>
{%endblock body%}
```