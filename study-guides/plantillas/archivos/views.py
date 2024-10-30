from django.shortcuts import redirect, render
from django.utils.text import slugify

from tasks.forms import AddTaskForm, EditTaskForm
from tasks.models import Task


def home(request):
    num_task = Task.objects.count()
    tasks = Task.objects.all()
    return render(request, 'tasks/home.html', {'num_task': num_task, 'tasks': tasks})


def task_detail(request, task_slug):
    task = Task.objects.get(slug=task_slug)
    return render(request, 'tasks/task/detail.html', dict(task=task))


def done(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/done.html', {'tasks': tasks})


def pending(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/pending.html', {'tasks': tasks})


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


def task_delete(request, task_slug: str):
    task = Task.objects.get(slug=task_slug)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:home')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


def toggle_task(request, task_slug: str):
    task = Task.objects.get(slug=task_slug)
    task.done = not task.done
    task.save()
    return redirect('tasks:home')
