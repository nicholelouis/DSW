# Tribu

Tribu es una pequeña red social que permite a los usuarios interactuar a través de echos y waves. Cada usuario cuenta con un perfil personalizable, donde pueden editar su biografía y su avatar. La plataforma incluye páginas para la gestión de cuentas de usuario, signup, login, logout, y administración de echos y waves. Los usuarios también pueden crear, modificar y eliminar estos elementos según lo deseen.

## Puesta en marcha

Con los comandos que nos proporciona el profesor solo nos faltaria crear las apps correspondientes al ejercicio

```python
pypas get excercise
cd folder
just create-venv
source .venv/bin/activate
just setup
```

### Crear las apps

```python
./manage.py startapp
```

## Crear los modelos

Crear los modelos solicitados, en este caso

### echos.models

```python
from django.conf import settings
from django.db import models
from django.urls import reverse

class Echo(models.Model):
    content = models.TextField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    def __str__(self) -> str:
        return self.content

    def get_absolute_url(self):
        return reverse('echos:echo-detail', kwargs={'echo_pk': self.pk})

    class Meta:
        ordering = ['-created_at']
```

**get_absolute_url**: Función que devuelve la ruta absoluta de una instancia, en este caso seria el url del dtail de un echo en cuestión y sirve para los redirect de las view hacia un detail

```python
return redirect(echo)
```

**class Meta ordering**: Los modelos se orderan directamente por uno o más campos desde la base de datos

### waves.models

```python
from django.conf import settings
from django.db import models

class Wave(models.Model):
    content = models.TextField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    echo = models.ForeignKey(
        'echos.Echo', related_name='waves', on_delete=models.CASCADE, null=False
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ['-created_at']
```

- **ForeingKey**: Establece relación de uno a muchos entre modelos, aquí relacionamos un Wave a un solo Echo
  - **related_name**: NO OLVIDAR, con el llamamos a todos los waves que tiene un Echo especifico, plural
  ```python
      echo_instance.waves.all()
  ```
  - **on_delete=models.CASCADE**: Si se borra el Echo se borran todos los Waves asociados
  - **null=False**: Asegura que el campo no pueda ser nulo, osea sin un echo asociado no puede existir un wave

### users.models

Aqui creamos el modelo del profile que va asociado a cada usuario

```python
from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile',on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True, upload_to='avatars', default='avatars/noavatar.png')
    bio = models.TextField(blank=True)
```

- **OneToOneField**: Relación uno a uno, un perfil solo puede pertenecer a un usuario y viceversa, es una manera de extender el modelo user predeterminado de django asociandolo de esta manera con otro modelo.

  - **Acceso Bidirecional**: user.profile / profile.user

- **Avatar**: Campo para cargar una imagen
  - **upload_to**: define el donde se guadaran las imgs
  - **default**: Si no se sube img utiliza esa por defecto
    **HAY QUE AJUSTAR EL SETTINGS Y LAS URLS PARA QUE SE VEAN**

Se llaman así en las plantillas ⤵️

```python
    <img src="{{ user.profile.avatar.url }}" alt="Avatar" class="img-fluid rounded-circle shadow" style="width: 150px; height: 150px;">
```

En las urls de primer nivel ⤵️

```python
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

En los settings ⤵️

```python
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
```

### Instalar APPS, Migraciones y Cargar data

- Una vez terminados los modelos instalamos las apps en el settings.py

```python
INSTALLED_APPS = [
    'shared.apps.SharedConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'echos.apps.EchosConfig',
    'waves.apps.WavesConfig',
    'users.apps.UsersConfig',
    'accounts.apps.AccountsConfig',
]
```

**Shared va de primero**

- Realizamos la migraciones y cargamos la data al project

```python
just mm
just m
just load-data
```

## Shared app (si la necesitamos)

Creamos el template base.html dentro de templates/shared y el styles.css dentro de static/shared

Para cargar los staticos y los imagenes en las url de primer nivel:

```python
from django.conf.urls.static import static
from django.conf import settings


+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

para usarlos en las plantillas:

```python
{% load static %} -> en el base

{% extends "shared/base.html" %} -> en las plantillas
{% block title %}Iniciar Sesión{% endblock %}
{% block body %}
{% endblock body %}
```

## Accounts app

Esta maneja el login, signin y el logout de cada usuario, como las urls no son account/login/ si no login/, a solas, estas urls tienen que ir en las de primer nivel, pero dentro de accounts iran las config de estas

Login usamos el que nos proporciona django, pero los otros los implementamos nosotros

### Templates

Dentro de **templates/registration** ‼️

### Views

```python
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from users.models import Profile
from .forms import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('echos:echo-list')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('echos:echo-list')
```

**Profile.objects.create(user=user)**: Cuando creamos un usuario en la vista de signup a su vez un creamos un profile vacio para que despues de error y sea mas facil manejarlo

### forms

```python
from django import forms
from django.contrib.auth import get_user_model

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
```

### urls PRIMER NIVEL

```python
from accounts.views import logout_view, signup
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

path('admin/', admin.site.urls),
path('login/', LoginView.as_view(), name='login'),
path('logout/', logout_view, name='logout'),
path('signup/', signup, name='signup'),
```

- Del login utilizamos el de Django y los otros los importamos desde nuesta app accounts

### Dentro del settings añade:

Que no se te olvide!

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'echos:echo-list'
LOGOUT_URL = 'logout'
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
```

## Echos app

### Views

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .decoradores import auth_user
from .forms import AddEchoForm, EditEchoForm
from .models import Echo

def get_echo(echo_pk):
    return Echo.objects.get(id=echo_pk)

@login_required
def echo_list(request):
    echos = Echo.objects.all()
    return render(request, 'echos/echo_list.html', {'echos': echos})

@login_required
def add_echo(request):
    if request.method == 'GET':
        form = AddEchoForm()
    else:
        if (form := AddEchoForm(data=request.POST)).is_valid():
            echo = form.save(commit=False)
            echo.user = request.user
            echo.save()
            return redirect('echos:echo-detail', echo_pk=echo.pk)
    return render(request, 'echos/add.html', dict(form=form))

@login_required
def echo_detail(request, echo_pk):
    echo = get_echo(echo_pk)
    all_waves = echo.waves.all()
    waves = all_waves[:5]
    waves_count = all_waves.count()
    return render(request, 'echos/detail.html', {'echo': echo, 'waves': waves, 'waves_count': waves_count})

@login_required
def echo_waves(request, echo_pk):
    echo = get_echo(echo_pk)
    waves = echo.waves.all()
    return render(request, 'echos/detail.html', {'echo': echo, 'waves': waves})

@login_required
@auth_user
def edit_echo(request, echo_pk):
    echo = get_echo(echo_pk)
    if request.method == 'POST':
        if (form := EditEchoForm(request.POST, instance=echo)).is_valid():
            echo = form.save(commit=False)
            echo.save()
            return redirect(echo)
    else:
        form = EditEchoForm(instance=echo)
    return render(request, 'echos/edit.html', dict(echo=echo, form=form))

@login_required
@auth_user
def echo_detele(request, echo_pk):
    echo = get_echo(echo_pk)
    echo.delete()
    return redirect('echos:echo-list')
```

**@loginrequired**: un decorador que nos proporciona django, el usuario tendra que estar loggeado para acceder a la vista que decore

**@auth_user**: un decorador creado por mi para verificar que el usuario que haga la petición sea el mismo sueño del echo al momento de modificarlo o borrarlo
echos/decoradores.py

```python
from django.http import HttpResponseForbidden
from .models import Echo

def auth_user(func):
    def wrapper(*args, **kwargs):
        user = args[0].user
        echo = Echo.objects.get(pk=kwargs['echo_pk'])
        if user != echo.user:
            return HttpResponseForbidden('No tienes permiso para editar este echo.')
        else:
            return func(*args, **kwargs)
    return wrapper
```

si este no es igual devuelve un **HttpResponseForbidden** un 403

### Forms

```python
from django import forms
from .models import Echo

class AddEchoForm(forms.ModelForm):
    class Meta:
        model = Echo
        fields = ('content',)

class EditEchoForm(forms.ModelForm):
    class Meta:
        model = Echo
        fields = ('content',)
```

### URLS

```python
from django.urls import path
from . import views
from waves.views import add_waves

app_name = 'echos'

urlpatterns = [
    path('', views.echo_list, name='echo-list'),
    path('add/', views.add_echo, name='add'),
    path('<int:echo_pk>/', views.echo_detail, name='echo-detail'),
    path('<int:echo_pk>/waves/', views.echo_waves, name='echo-waves'),
    path('<int:echo_pk>/edit/', views.edit_echo, name='edit-echo'),
    path('<int:echo_pk>/delete/', views.echo_detele, name='echo-delete'),
    path('<int:echo_pk>/waves/add/', add_waves, name='add-wave'),
]
```

**int:echo_pk**: Usamos el int como conver ya que estamos usando la pk del echo

- URL de primer nivel ⤵️

```python
path('echos/', include('echos.urls')),
```

**Recuerda activar el administrador**

```python
from django.contrib import admin
from .models import Echo

@admin.register(Echo)
class EchoAdmin(admin.ModelAdmin):
    list_display = ['content',]
```

## Waves app

### Views

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .decoradores import auth_user
from .forms import EditWaveForm, AddWaveForm
from .models import Wave
from echos.models import Echo

def get_wave(wave_pk):
    return Wave.objects.get(id=wave_pk)

@login_required
@auth_user
def edit_wave(request, wave_pk):
    wave = get_wave(wave_pk)
    if request.method == 'POST':
        if (form := EditWaveForm(request.POST, instance=wave)).is_valid():
            wave = form.save(commit=False)
            wave.save()
            return redirect('echos:echo-detail', echo_pk=wave.echo.pk)
    else:
        form = EditWaveForm(instance=wave)
    return render(request, 'echos/edit.html', dict(wave=wave, form=form))

@login_required
@auth_user
def wave_detele(request, wave_pk):
    wave = get_wave(wave_pk)
    wave.delete()
    return redirect('echos:echo-detail', echo_pk=wave.echo.pk)

@login_required
def add_waves(request, echo_pk):
    echo = Echo.objects.get(id=echo_pk)
    if request.method == 'POST':
        form = AddWaveForm(request.POST)
        if form.is_valid():
            wave = form.save(commit=False)
            wave.echo = echo
            wave.user = request.user
            wave.save()
            return redirect('echos:echo-detail', echo_pk=echo.pk)
    else:
        form = AddWaveForm()
    return render(request, 'echos/add.html', {'form': form, 'echo': echo})
```

**@auth_user**: decorador que hace lo mismo que el de arriba pero modificado para que funcione con las waves

```python
from django.http import HttpResponseForbidden
from .models import Wave

def auth_user(func):
    def wrapper(*args, **kwargs):
        user = args[0].user
        wave = Wave.objects.get(pk=kwargs['wave_pk'])
        if user != wave.user:
            return HttpResponseForbidden('No tienes permiso para editar este echo.')
        else:
            return func(*args, **kwargs)
    return wrapper
```

**Clave del echo desde el wave**: wave.echo.pk

### Forms

```python
from django import forms
from .models import Wave

class EditWaveForm(forms.ModelForm):
    class Meta:
        model = Wave
        fields = ('content',)

class AddWaveForm(forms.ModelForm):
    class Meta:
        model = Wave
        fields = ['content']
```

### URLS

```python
from django.urls import path
from . import views

app_name = 'waves'

urlpatterns = [
    path('<int:wave_pk>/edit/', views.edit_wave, name='edit-wave'),
    path('<int:wave_pk>/delete/', views.wave_detele, name='delete-wave'),
]
```

- Urls de primer nivel

```python
path('waves/', include('waves.urls')),
```

**Recuerda activar el administrador**

```python
from django.contrib import admin
from .models import Wave

@admin.register(Wave)
class WaveAdmin(admin.ModelAdmin):
    list_display = ['content',]
```

## Users app

### View

```python
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from echos.models import Echo
from .forms import EditProfileForm
from .models import Profile
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .decoradores import auth_user

def get_user(username):
    return User.objects.get(username=username)

def get_echos(user):
    return Echo.objects.filter(user=user)

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

@login_required
def user_detail(request, username):
    user = get_user(username)
    echos = get_echos(user)
    total_echos = echos.count()
    return render(request, 'users/user_detail.html', {'user': user, 'echos': echos[:5], 'total_echos': total_echos})

@login_required
@auth_user
def edit_profile(request, username):
    user = get_user(username)
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        if (form := EditProfileForm(request.POST, request.FILES, instance=profile)).is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect(reverse('users:user-detail', kwargs={'username': username}))
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'users/edit.html', dict(profile=profile, form=form))

@login_required
def user_echos(request, username):
    user = get_user(username)
    echos = get_echos(user)
    return render(request, 'users/user_detail.html', {'user': user, 'echos': echos})

@login_required
def logged_user(request):
    return redirect('users:user-detail', username=request.user.username)
```

- **Echos de un User**: Echo.objects.filter(user=user)

- **Edit profile**: request.FILES Para poder subir o cambiar la foto de perfil

- **get_object_or_404**: si no encuentra el objeto devuelve un 404

- **@auth_user**: users/decoradores.py ⤵️

```python
from django.http import HttpResponseForbidden

def auth_user(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        user = request.user
        username = kwargs.get('username')
        if user.username != username:
            return HttpResponseForbidden('No tienes permiso para editar este perfil.')
        return func(*args, **kwargs)
    return wrapper
```

### Forms

```python
from django import forms
from .models import Profile

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'style': 'margin-bottom: 20px;',
            'label': '',
}),}
```

### URLS

```python
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_list, name='user-list'),
    path('@me/', views.logged_user, name= 'logged-user'),
    path('<str:username>/', views.user_detail, name= 'user-detail'),
    path('<str:username>/edit/', views.edit_profile, name= 'edit-profile'),
    path('<str:username>/echos/', views.user_echos, name= 'user-echos'),
]
```

**@me/**: esta url que redirige al detail del user autenticado tiene que estar por encima del user detail porque si no da error!

**Recuerda activar el administrador**

```python
from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
```

### Autentica que el usuario es el dueño del echo sin decorador

```python
def edit_echo(request, echo_pk):
    echo = get_object_or_404(Echo, pk=echo_pk)

    if request.user != echo.user:
        return HttpResponseForbidden('No tienes permiso para editar este echo.')

    if request.method == 'POST':
        form = EditEchoForm(request.POST, instance=echo)
        if form.is_valid():
            echo = form.save(commit=False)
            echo.save()
            return redirect(echo)
    else:
        form = EditEchoForm(instance=echo)

    return render(request, 'echos/edit.html', {'echo': echo, 'form': form})
```

## Revisa lo que te dijo sergio‼️

- Hacer el login con la infraestructura de Django y hacer logout/signup con la infraestructura propia me parece algo "extraño". O todo de una manera o todo de la otra.

- Como buena práctica, todos los modelos deberían tener un **str**()

- Un campo TextField() admite una cantidad arbitraria de texto. Si indicamos un max_length sólo servirá para el Textarea correspondiente.

- null=False no se utiliza. Todos los campos son obligatorios hasta que se indique lo contrario.

- Falta "related_name" es las claves ajenas al modelo User de Django.

- Funciones como get_user() o get_echo() no deben estar en views.py, en todo caso en models.py o en otro fichero auxiliar.

- No uses nombres en español: decoradores.py
