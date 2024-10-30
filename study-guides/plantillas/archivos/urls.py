from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.home, name='home'),
    path('task/<task_slug>/', views.task_detail, name='task-detail'),
    path('done', views.done, name='done'),
    path('pending', views.pending, name='pending'),
    path('add', views.add_task, name='add-task'),
    path('task/<task_slug>/edit/', views.edit_task, name='edit-task'),
    path('task/<task_slug>/delete/', views.task_delete, name='task-delete'),
    path('task/<task_slug>', views.toggle_task, name='toggle'),
]
