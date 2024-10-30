# Ejemplos de modelos y vistas

## Ejemplos de recuperaciones en las vistas

### Stock disponible
```python
def products_in_stock(request):
    products = Product.objects.filter(stock__gt=0)
    return render(request, "products/in_stock.html", dict(products=products))
```

### Por cliente
```python
def customer_orders(request, customer_id):
    orders = Order.objects.filter(customer_id=customer_id)
    return render(request, "orders/customer_orders.html", dict(orders=orders))
```

### Usuario activo
```python
def active_users(request):
    users = UserProfile.objects.filter(is_active=True)
    return render(request, "users/active.html", dict(users=users))
```

### Por liente
```python
def customer_orders(request, customer_id):
    orders = Order.objects.filter(customer_id=customer_id)
    return render(request, "orders/customer_orders.html", dict(orders=orders))
```

### Post de la ultima semana
```python
def recent_posts(request):
    one_week_ago = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=one_week_ago)
    return render(request, "posts/recent.html", dict(posts=posts))
```

### Tareas de un usuario
```python
def user_tasks(request, user_id):
    tasks = Task.objects.filter(assigned_to_id=user_id)
    return render(request, "tasks/user_tasks.html", dict(tasks=tasks))
```

### Productos con descuento
```python
def discounted_products(request):
    products = Product.objects.filter(discount__gt=0)
    return render(request, "products/discounted.html", dict(products=products))
```

### Pedidos entregados
```python
def delivered_orders(request):
    orders = Order.objects.filter(status="delivered")
    return render(request, "orders/delivered.html", dict(orders=orders))
```

### Usuarios registrados el ultimo mes
```python
def recent_users(request):
    one_month_ago = timezone.now() - timedelta(days=30)
    users = UserProfile.objects.filter(date_joined__gte=one_month_ago)
    return render(request, "users/recent.html", dict(users=users))
```

### Tareas con prioridad
```python
def high_priority_tasks(request):
    tasks = Task.objects.filter(priority="high")
    return render(request, "tasks/high_priority.html", dict(tasks=tasks))
```

### Usando Order by

- ascendente
```python
def task_list(request):
    tasks = Task.objects.all().order_by('created_at')
    return render(request, "tasks/list.html", {'tasks': tasks})
```

- descendente
```python
def task_list_desc(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, "tasks/list_desc.html", {'tasks': tasks})
```

- Múltiples Campos
```python
def task_list_multi_order(request):
    tasks = Task.objects.all().order_by('-priority', 'created_at')
    return render(request, "tasks/list_multi_order.html", {'tasks': tasks})
```

- Dinámico
```python
def task_list_dynamic_order(request):
    order_by_field = request.GET.get('order_by', 'created_at')
    tasks = Task.objects.all().order_by(order_by_field)
    return render(request, "tasks/list_dynamic_order.html", {'tasks': tasks})
```

## Ejemplo TAG:

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

## Ejemplo UUID: 

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

## Uso de los forloops


```html
<h1>Proyectos y Tareas</h1>

<ul>
    {% for project in projects %}
        <!-- Usamos forloop.counter para numerar cada proyecto -->
        <li>
            <h2>Proyecto {{ forloop.counter }}: {{ project.name }}</h2>
            <p>Descripción: {{ project.description }}</p>

            <!-- Diferenciamos el primer proyecto con forloop.first -->
            {% if forloop.first %}
                <p><strong>¡Proyecto Destacado!</strong></p>
            {% endif %}

            <!-- Agregamos una lista de tareas asociadas al proyecto -->
            <ul>
                {% for task in project.tasks %}
                    <li>
                        <!-- Usamos forloop.counter0 para numerar tareas desde cero -->
                        {{ forloop.counter0 }} - {{ task.name }} ({{ task.status }})

                        <!-- Indicamos si es la primera o última tarea del proyecto -->
                        {% if forloop.first %}
                            <span>(Primera Tarea)</span>
                        {% elif forloop.last %}
                            <span>(Última Tarea)</span>
                        {% endif %}

                        <!-- Usamos forloop.revcounter para contar las tareas desde el final -->
                        <span> - (Contador inverso: {{ forloop.revcounter }})</span>
                        
                        <!-- Si la tarea es parte de un proyecto destacado, aplicamos estilo especial -->
                        {% if forloop.parentloop.first %}
                            <span style="color: green;">[Proyecto Destacado]</span>
                        {% endif %}
                    </li>
                {% endfor %}
            </ul>

            <!-- Indicamos el índice de cada proyecto en el conteo inverso -->
            <p>Proyecto en la posición inversa {{ forloop.revcounter }} del total.</p>
            
            <!-- Si es el último proyecto, le damos un estilo especial -->
            {% if forloop.last %}
                <p><strong>Último proyecto en la lista.</strong></p>
            {% endif %}
        </li>
    {% endfor %}
</ul>
```
- forloop.counter: Numeramos cada proyecto desde 1.
- forloop.first: Resaltamos el primer proyecto con un mensaje de "¡Proyecto Destacado!" y aplicamos un mensaje especial a la primera tarea en cada proyecto.
- forloop.counter0: Numeramos las tareas desde 0 en lugar de 1.
- forloop.revcounter: Mostramos el contador en orden inverso tanto para los proyectos como para las tareas.
- forloop.last: Agregamos un mensaje especial al último proyecto y última tarea de cada lista.
- forloop.parentloop: Dentro del bucle anidado de tareas, verificamos si el proyecto actual es el primero, para resaltar que sus tareas pertenecen a un "Proyecto Destacado".

### Yes or No

- El modelo del ejemplo
```python
class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
```

- Primero desde la vista le pasamos un valor
```python
def user_status(request, user_id):
    user_profile = UserProfile.objects.get(id=user_id)
    return render(request, 'example/user_status.html', {'is_active': user_profile.is_active, 'user_name': user_profile.name})

# Otra forma de recuperar
# user_profile = get_object_or_404(UserProfile, id=user_id)
```

- La vista seria tal que
```python
<p>El usuario está: {{ is_active|yesno:"activo,inactivo" }}</p>
```

## Botones

View
```python
from django.shortcuts import render
from .models import Post

def post_list(request):
    order = request.GET.get('order', 'desc')
    
    if order == 'asc':
        posts = Post.objects.all().order_by('created_at')  
    else:
        posts = Post.objects.all().order_by('-created_at') 


    return render(request, 'post_list.html', {'posts': posts})
```

template
```python

    <!-- Botones para ordenar -->
    <a href="?order=desc">Ordenar por Más Reciente</a>
    <a href="?order=asc">Ordenar por Más Antiguo</a>
```

url
```python
from django.urls import path
from .views import post_list

urlpatterns = [
    path('', post_list, name='post_list'),
]
```

Modelo
```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```