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

## Subjects

### subjects.Subject
```python
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

class Subject(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey( 
        settings.AUTH_USER_MODEL,
        related_name= 'subjects',
        on_delete= models.PROTECT,
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='subjects.Enrollment',
        related_name= 'enrolled_subjects',
    )
    class Meta:
        ordering = ['code']
    
    def __str__(self):
        return f'{self.code}: {self.name}'

    def get_absolute_url(self):
        return reverse('subjects:subject-detail', kwargs={'subject_code': self.code})
```
Este modelo representa una asignatura en nuestra app, relacionada con estudiantes y profesores mediante mediante las relaciones de ForignKey y ManyToManyField 

### Teacher
1. settings.AUTH_USER_MODEL: La relación apunta al modelo de usuario configurado (que representa a los profesores).

2. related_name='subjects': Permite acceder a las asignaturas impartidas por un profesor con: **teacher.subjects**

3. on_delete=models.PROTECT: Protege contra la eliminación del profesor si tiene asignaturas asociadas.

### Students
1. Tipo: ManyToManyField.

2. Relación: Relaciona una asignatura con los estudiantes inscritos en ella.

3. Configuración:

    - settings.AUTH_USER_MODEL: Apunta al modelo de usuario que representa a los estudiantes.
    - through='subjects.Enrollment': Usa el modelo intermedio Enrollment para manejar la relación, permitiendo añadir información extra como la fecha de inscripción o calificaciones.
    - related_name='enrolled_subjects': Permite acceder a las asignaturas en las que un estudiante está inscrito usando: **student.enrolled_subjects**

### subjects.Lesson

```bash
class Lesson(models.Model):
    subject = models.ForeignKey(
        Subject,
        related_name= 'lessons',
        on_delete= models.CASCADE,
    )
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)

    class Meta: 
        ordering = ['title']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
            'subjects:lesson-detail', kwargs={'subject_code': self.subject.code, 'lesson_pk': self.pk}
        )
```
Representa una unidad de contenido asocido a una asignatura

### subject
- Tipo: ForeignKey.
- Relación: Relaciona la lección con una asignatura (Subject) específica.
- Configuración:

1. related_name='lessons': Permite acceder a todas las lecciones de una asignatura utilizando **subject.lessons**

2. on_delete=models.CASCADE: Si la asignatura relacionada se elimina, también se eliminarán las lecciones asociadas.

Ejemplo:
```bash
subject = Subject.objects.get(code='PHY')  # Relaciona la lección con la asignatura "Física".
```

### subjects.Enrollment

Representa la relacion entre una asignatura y un estudiante (la incripción), guardando a su vez información adicional como lo seria las nota o la fecha de inscripción.

```python
class Enrollment(models.Model):
    student = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name= 'enrollments',
    on_delete= models.CASCADE,
    )
    subject = models.ForeignKey(
        Subject,
        related_name= 'enrollments',
        on_delete= models.CASCADE,
    )
    enrolled_at = models.DateField(auto_now=True)
    mark = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators = [MinValueValidator(1), MaxValueValidator(10)],
    )
    def __str__(self):
        return f'{self.student} {self.subject} enrolled at {self.enrolled_at} {self.mark}'
```
### Campos

### student:
- Tipo: ForeignKey.
- Relación: Relaciona cada inscripción con un estudiante.
- Configuración:

1. settings.AUTH_USER_MODEL: Relaciona con el modelo de usuario (estudiante).

2. related_name='enrollments': Permite acceder a todas las inscripciones de un estudiante usando **student.enrollments**.

3. on_delete=models.CASCADE: Si el estudiante se elimina, se eliminarán también sus inscripciones.

Ejemplo:
```bash
student = User.objects.get(username='juan123')
enrollments = student.enrollments.all()  # Todas las inscripciones del estudiante "juan123".
```

### subject:
- Tipo: ForeignKey.
- Relación: Relaciona cada inscripción con una asignatura.
- Configuración:

1. related_name='enrollments': Permite acceder a todas las inscripciones de una asignatura usando **subject.enrollments**.

2. on_delete=models.CASCADE: Si una asignatura se elimina, se eliminarán también las inscripciones asociadas.

Ejemplo:
```python
subject = Subject.objects.get(code='MAT')
enrollments = subject.enrollments.all()  # Todas las inscripciones a la asignatura "MAT".
```
### enrolled_at:
- Tipo: DateField.
- Descripción: Almacena la fecha en la que el estudiante se inscribió en la asignatura.
- Configuración:

1. auto_now=True: Actualiza automáticamente la fecha al momento de crear o modificar la inscripción.
Ejemplo:
```python
enrollment = Enrollment.objects.create(student=student, subject=subject)
print(enrollment.enrolled_at)  # Fecha actual (momento de la inscripción).
```

### mark:
- Tipo: PositiveSmallIntegerField.
- Descripción: Nota o calificación obtenida por el estudiante en la asignatura.
- Configuración:

blank=True, null=True: La calificación es opcional.

- Validadores:
MinValueValidator(1): La nota mínima permitida es 1.
MaxValueValidator(10): La nota máxima permitida es 10.
Ejemplo:
```python
enrollment.mark = 8  # Nota válida.
enrollment.save()
```

## Users

### users.Profile

Creamos este modelo como una extencion del modelo user predefinido por django, lo usamos para agregar su role entre otras cosas

```python
class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'S', 'student',
        TEACHER = 'T', 'teacher'

    role = models.CharField(
        max_length= 1,
        choices=Role,
        default=Role.STUDENT
        )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.CASCADE,
    )
    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to='cache',
        default='cache/noavatar.png',
    )
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.role}'

    def get_role(self):
        match self.role:
            case 'S':
                return 'Student'
            case 'T':
                return 'Teacher'
```

**Campos del modelo**

### role:
- Tipo: CharField.
- Descripción: Define el rol del usuario (por ejemplo, estudiante o profesor).
- Configuración:

1. max_length=1: Limita el valor del campo a un carácter.
2. choices=Role: Usa una enumeración (clase Role) para restringir las opciones del campo.
3. default=Role.STUDENT: El rol predeterminado es estudiante.

### Enumeración Role:

class Role(models.TextChoices):
    STUDENT = 'S', 'student'
    TEACHER = 'T', 'teacher'
Define dos posibles roles:
STUDENT con el valor 'S'.
TEACHER con el valor 'T'.
Ejemplo:
```python
profile.role = Profile.Role.TEACHER  # Asigna el rol de "teacher" al perfil.
```

### user:
- Tipo: OneToOneField.
- Relación: Cada perfil está asociado a exactamente un usuario del modelo settings.AUTH_USER_MODEL.
- Configuración:

1. related_name='profile': Permite acceder al perfil de un usuario mediante user.profile.
2. on_delete=models.CASCADE: Si el usuario es eliminado, también se elimina su perfil.
Ejemplo:
```python
user = User.objects.get(username='juan123')
profile = user.profile  # Obtiene el perfil asociado al usuario.
```
### avatar:
- Tipo: ImageField.
- Descripción: Imagen de perfil del usuario.
- Configuración:

1. blank=True, null=True: El avatar es opcional.

2. upload_to='cache': Las imágenes se almacenan en la carpeta cache dentro del sistema de almacenamiento configurado.

3. default='cache/noavatar.png': Si no se carga un avatar, se usará la imagen predeterminada (noavatar.png).

Ejemplo:
```python
profile.avatar = 'cache/avatar1.png'
profile.save()
```

### bio:
- Tipo: TextField.
- Descripción: Biografía o descripción personal del usuario.
- Configuración:

blank=True, null=True: El campo es opcional.

Ejemplo:
```python
profile.bio = "Profesor de matemáticas con 10 años de experiencia."
profile.save()
```

**Métodos del modelo**

__str__:
Devuelve una representación en texto del objeto Profile.
Incluye:
El nombre de usuario del usuario asociado (self.user.username).
El rol del perfil (self.role).
Ejemplo:
```python
profile = Profile.objects.get(id=1)
print(profile)  # Output: "juan123 - S"
```

### get_role:
Devuelve el rol del usuario como una cadena más descriptiva.
Utiliza la sentencia match (Python 3.10+) para mapear los valores de self.role a cadenas descriptivas:
'S' → "Student".
'T' → "Teacher".
Ejemplo:
```python
profile = Profile.objects.get(id=1)
print(profile.get_role())  # Output: "Student" o "Teacher"
```

**Relaciones importantes**

### Relación con User:
Este modelo amplía el modelo de usuario base mediante una relación OneToOneField. Esto significa que cada usuario tiene exactamente un perfil asociado.
Se utiliza frecuentemente para añadir información personalizada que no pertenece al modelo de usuario base.
Ejemplo:

user = User.objects.get(username='juan123')
profile = Profile.objects.create(user=user, role=Profile.Role.TEACHER)
Uso del modelo

### Creación de un perfil:
```python
user = User.objects.create_user(username='maria', password='securepassword')
profile = Profile.objects.create(user=user, role=Profile.Role.STUDENT, bio='Estudiante de historia.')
```

### Acceso al perfil desde un usuario:
```python
user = User.objects.get(username='maria')
profile = user.profile  # Accede al perfil asociado al usuario.
print(profile.bio)  # Output: "Estudiante de historia."
```

### Actualización del avatar:
```python
profile.avatar = 'cache/avatar2.png'
profile.save()
```

### Consultar el rol del usuario:
```python
profile = Profile.objects.get(user=user)
print(profile.get_role())  # Output: "Student" o "Teacher"
```

Ejemplo práctico

1. Creación de un usuario y su perfil:
```python
user = User.objects.create_user(username='profesor1', password='securepassword')
profile = Profile.objects.create(user=user, role=Profile.Role.TEACHER, bio="Profesor de física.")
```

2. Acceso y uso del perfil:
```python
print(profile)  # Output: "profesor1 - T"
print(profile.get_role())  # Output: "Teacher"
print(profile.bio)  # Output: "Profesor de física."
```

3. Listado de todos los perfiles de estudiantes:
```python
students = Profile.objects.filter(role=Profile.Role.STUDENT)
for student in students:
    print(student.user.username, student.bio)
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

## Métodos de .object.

| **Método**          | **Descripción**                                                                                   | **Ejemplo**                                                                                                                                                         |
|----------------------|---------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`all()`**          | Devuelve todos los objetos del modelo.                                                           | `profiles = Profile.objects.all()`<br>Itera por todos los perfiles: `for profile in profiles: print(profile.user.username)`                                       |
| **`filter()`**       | Devuelve un queryset con los objetos que cumplen las condiciones especificadas.                   | `teachers = Profile.objects.filter(role='T')`<br>Obtiene todos los perfiles con el rol "Teacher".                                                                |
| **`exclude()`**      | Devuelve un queryset con los objetos que **no** cumplen las condiciones especificadas.            | `non_teachers = Profile.objects.exclude(role='T')`<br>Obtiene todos los perfiles que **no** son profesores.                                                      |
| **`get()`**          | Devuelve un único objeto que cumple las condiciones especificadas. Lanza error si no hay o hay más de uno. | `profile = Profile.objects.get(user__username='juan123')`<br>Obtiene el perfil de un usuario con el nombre de usuario "juan123".                                   |
| **`create()`**       | Crea y guarda un nuevo objeto en la base de datos.                                               | `profile = Profile.objects.create(user=user, role='S', bio='Estudiante de matemáticas.')`<br>Crea un perfil para el usuario especificado.                         |
| **`update()`**       | Actualiza los objetos existentes que cumplen las condiciones especificadas.                       | `Profile.objects.filter(role='S').update(bio='Actualización masiva de estudiantes.')`<br>Actualiza la biografía de todos los estudiantes.                        |
| **`count()`**        | Devuelve el número total de objetos en el queryset.                                              | `total_profiles = Profile.objects.count()`<br>Obtiene el número total de perfiles.                                                                                |
| **`first()`**        | Devuelve el primer objeto en el queryset o `None` si no hay objetos.                             | `first_profile = Profile.objects.first()`<br>Obtiene el primer perfil creado.                                                                                     |
| **`last()`**         | Devuelve el último objeto en el queryset o `None` si no hay objetos.                             | `last_profile = Profile.objects.last()`<br>Obtiene el último perfil creado.                                                                                       |
| **`exists()`**       | Devuelve `True` si el queryset contiene objetos, de lo contrario devuelve `False`.                | `has_teachers = Profile.objects.filter(role='T').exists()`<br>Devuelve `True` si hay profesores en la base de datos.                                             |
| **`delete()`**       | Elimina los objetos que cumplen las condiciones especificadas.                                    | `Profile.objects.filter(role='S').delete()`<br>Elimina todos los perfiles de estudiantes.                                                                         |
| **`values()`**       | Devuelve un queryset con diccionarios de los campos especificados.                                | `profiles = Profile.objects.values('user__username', 'role')`<br>Obtiene una lista de diccionarios con los nombres de usuario y roles de los perfiles.            |
| **`values_list()`**  | Devuelve un queryset con listas o tuplas de los valores especificados.                            | `usernames = Profile.objects.values_list('user__username', flat=True)`<br>Obtiene una lista con todos los nombres de usuario.                                      |
| **`order_by()`**     | Ordena los resultados por los campos especificados.                                               | `profiles = Profile.objects.order_by('user__username')`<br>Ordena los perfiles alfabéticamente por el nombre de usuario.                                          |
| **`distinct()`**     | Elimina los duplicados en el queryset.                                                            | `roles = Profile.objects.values_list('role', flat=True).distinct()`<br>Obtiene una lista única de roles existentes (sin duplicados).                              |
| **`aggregate()`**    | Realiza operaciones agregadas como `Sum`, `Avg`, `Count`, etc. en el queryset.                    | `from django.db.models import Count`<br>`total_teachers = Profile.objects.filter(role='T').aggregate(Count('id'))`<br>Cuenta cuántos profesores hay.             |
| **`annotate()`**     | Añade campos calculados a cada objeto del queryset.                                               | `from django.db.models import Count`<br>`profiles = Profile.objects.annotate(total_subjects=Count('user__subjects'))`<br>Añade el total de asignaturas a cada perfil. |
| **`get_or_create()`**| Busca un objeto que cumpla con las condiciones. Si no lo encuentra, lo crea.                      | `profile, created = Profile.objects.get_or_create(user=user, defaults={'role': 'S'})`<br>Obtiene o crea un perfil para el usuario.                                |
| **`update_or_create()`**| Busca un objeto y lo actualiza. Si no existe, lo crea.                                         | `profile, created = Profile.objects.update_or_create(user=user, defaults={'role': 'T'})`<br>Actualiza o crea un perfil con el rol de "Teacher".                  |
| **`raw()`**          | Ejecuta una consulta SQL cruda y devuelve los objetos correspondientes.                          | `profiles = Profile.objects.raw('SELECT * FROM app_profile WHERE role = "S"')`<br>Ejecuta una consulta SQL directamente.                                          |
| **`bulk_create()`**  | Inserta múltiples objetos en la base de datos en una sola operación.                              | `Profile.objects.bulk_create([Profile(user=u, role='S') for u in users])`<br>Crea perfiles para una lista de usuarios en una sola operación.                     |
| **`bulk_update()`**  | Actualiza múltiples objetos en una sola operación.                                                | `Profile.objects.bulk_update(profiles, ['bio'])`<br>Actualiza el campo `bio` en múltiples perfiles a la vez.                                                     |

# Cosas que dijo sergio

**Añadir 1 elemento intermedio de cada vez**
Esto se refiere a cómo añadir manualmente un registro al modelo intermedio. Esto no se hace directamente desde el campo ManyToManyField, sino que se interactúa con el modelo intermedio:

### Crear instancias de Student y Course
```python
student = Student.objects.create(name="Juan")
course = Course.objects.create(title="Matemáticas")
```

### Añadir un registro en el modelo intermedio
```python
Enrollment.objects.create(student=student, course=course, grade=9)
```

**Añadir 1 Enrollment de cada vez**
Este es un caso práctico de usar el modelo intermedio con un formulario para añadir un registro de Enrollment. Ejemplo de vista y formulario:

### Formulario:
```python
from django import forms

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'grade']
```

### Vista:
```python
from django.shortcuts import render, redirect
from .forms import EnrollmentForm

def add_enrollment(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirigir tras añadir
    else:
        form = EnrollmentForm()
    return render(request, 'add_enrollment.html', {'form': form})
```

### Template:
```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Add Enrollment</button>
</form>
```

## Guía de validadores

1. Validaciones Básicas en Modelos

Los modelos de Django incluyen validaciones automáticas basadas en los argumentos de los campos.

Ejemplo de Validaciones en un Modelo:
```python
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator

class Student(models.Model):
    name = models.CharField(max_length=50)  # Limita el texto a 50 caracteres
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)]  # Edad entre 18 y 100
    )
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()]  # Verifica que el formato del correo sea válido
    )
    registration_date = models.DateField()

    def __str__(self):
        return self.name
```
Qué pasa aquí?
max_length=50: Limita la longitud del texto.
PositiveIntegerField: Solo permite valores enteros positivos.
validators: Define validaciones adicionales para restricciones más específicas.
unique=True: Asegura que el correo electrónico sea único.

2. Validaciones en Formularios

Django permite validar datos al procesar formularios (usando forms.Form o forms.ModelForm).

Ejemplo de Validaciones en un Formulario:
```python
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'email', 'registration_date']

    def clean_age(self):  # Validación personalizada para el campo "age"
        age = self.cleaned_data.get('age')
        if age < 18:
            raise forms.ValidationError('La edad debe ser al menos 18 años.')
        return age

    def clean(self):  # Validación a nivel de formulario (campos relacionados)
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email and not email.endswith('@example.com'):
            raise forms.ValidationError('El correo debe ser del dominio @example.com.')
        return cleaned_data
```

Cómo Funciona?
clean_<campo>: Valida un campo específico (en este caso, age).
clean: Valida múltiples campos relacionados o lógica compleja.

3. Validaciones Personalizadas

Django permite agregar validaciones personalizadas a nivel de modelos y formularios.

Ejemplo de Validación Personalizada en Modelos:
```python
from django.core.exceptions import ValidationError

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(f'{value} no es un número par.')

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_even])  # Solo precios pares
```
Cómo se utiliza?
Define una función de validación (validate_even).
Añádela al argumento validators del campo.

4. Validaciones en Vistas

Si usas vistas para manejar formularios, también puedes realizar validaciones personalizadas antes de guardar los datos.

Ejemplo:
```python
from django.shortcuts import render
from django.http import HttpResponse
from .forms import StudentForm

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():  # Validaciones automáticas del formulario
            student = form.save(commit=False)
            if student.age < 18:
                return HttpResponse("El estudiante debe ser mayor de edad.")
            student.save()
            return HttpResponse("Estudiante añadido correctamente.")
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})
```

6. Validadores Incorporados de Django

Django incluye varios validadores listos para usar que puedes aplicar a los campos.

Validador	Descripción
MaxValueValidator	-> Valida que el valor no sea mayor que el máximo.
MinValueValidator	-> Valida que el valor no sea menor que el mínimo.
EmailValidator	-> Valida que el formato sea un correo válido.
RegexValidator	-> Valida que el valor coincida con una expresión regular.
URLValidator	-> Valida que el valor sea una URL válida.
FileExtensionValidator	-> Valida las extensiones de archivo permitidas.

Ejemplo con RegexValidator:

```python
from django.core.validators import RegexValidator

phone_validator = RegexValidator(r'^\+?1?\d{9,15}$', 'Número de teléfono inválido.')

class Contact(models.Model):
    phone_number = models.CharField(validators=[phone_validator], max_length=16)
```
## Guia de procesadores de contexto

- Ejemplo 1: Agregar un mensaje global
Crea un archivo para tus procesadores de contexto, por ejemplo: context_processors.py.

```python
# context_processors.py
def global_message(request):
    return {
        'global_message': '¡Bienvenido a nuestra plataforma!'
    }
En este caso, el mensaje "¡Bienvenido a nuestra plataforma!" estará disponible en todas las plantillas como {{ global_message }}.
```

- Ejemplo 2: Agregar datos dinámicos
Si necesitas enviar datos dinámicos (por ejemplo, todas las materias disponibles), puedes hacer esto:

```python
# context_processors.py
from subjects.models import Subject

def available_subjects(request):
    subjects = Subject.objects.all()
    return {
        'subjects': subjects
    }
En este caso, la lista de materias estará disponible en todas las plantillas como {{ subjects }}.
```

3. Registrar un Procesador de Contexto

Para que Django utilice tu procesador de contexto, debes registrarlo en la configuración del proyecto, en el archivo settings.py:
```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Directorios de plantillas
        'APP_DIRS': True,  # Activa la búsqueda de plantillas en cada app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Necesario para usar {{ request }}
                'django.contrib.auth.context_processors.auth',  # Para {{ user }}
                'django.contrib.messages.context_processors.messages',
                'subjects.context_processors.available_subjects',  # Tu procesador
                'subjects.context_processors.global_message',  # Otro procesador
            ],
        },
    },
]
```
4. Uso en Plantillas

Una vez registrado, puedes acceder a los datos del procesador en cualquier plantilla:
```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Mi Sitio</title>
</head>
<body>
    <p>{{ global_message }}</p>

    <h2>Materias disponibles:</h2>
    <ul>
        {% for subject in subjects %}
            <li>{{ subject.name }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```
5. Ejemplo Avanzado: Procesador Basado en Roles

Puedes usar un procesador de contexto para mostrar información dependiendo del rol del usuario:
```python
# context_processors.py

def user_role_context(request):
    if request.user.is_authenticated:
        role = request.user.profile.role
        return {
            'is_teacher': role == 'T',
            'is_student': role == 'S',
        }
    return {
        'is_teacher': False,
        'is_student': False,
    }
Uso en Plantillas:
<!-- dashboard.html -->
<h1>Dashboard</h1>
{% if is_teacher %}
    <p>Bienvenido, profesor. Aquí están tus cursos:</p>
{% elif is_student %}
    <p>Bienvenido, estudiante. Aquí están tus materias:</p>
{% else %}
    <p>Por favor, inicia sesión para acceder a la plataforma.</p>
{% endif %}
``` 

## Guia de Tags

Crear Tags Personalizados

- Paso 1: Crear un Archivo para Tags
Dentro de tu app, crea un directorio llamado templatetags.
Dentro de este directorio, crea un archivo __init__.py (para que sea un paquete).
Crea otro archivo, por ejemplo, custom_tags.py.
Tu estructura debería verse así:

myapp/
    templatetags/
        __init__.py
        custom_tags.py

- Paso 2: Registrar los Tags
En el archivo custom_tags.py, importa las herramientas necesarias y registra tu biblioteca de tags:
```python
from django import template

register = template.Library()
```

Ahora puedes crear tags personalizados.

3. Crear un Tag Simple
Un tag simple ejecuta una función y devuelve un valor directamente.

Ejemplo: Capitalizar un Texto
```python
# templatetags/custom_tags.py

@register.simple_tag
def capitalize(text):
    """Convierte el texto a mayúsculas."""
    return text.upper()
```
En tu plantilla:
```python
{% load custom_tags %}

<p>{% capitalize "hola mundo" %}</p>
Salida:

<p>HOLA MUNDO</p>
```

- 4. Crear un Tag con Lógica Compleja
Para lógica más avanzada, usa @register.inclusion_tag. Este tipo de tag renderiza un fragmento de plantilla y puede pasarle un contexto específico.

Ejemplo: Mostrar Lista de Materias

```python
# templatetags/custom_tags.py

from subjects.models import Subject

@register.inclusion_tag('subjects/subject_list.html')
def show_subjects(limit=5):
    """Muestra las materias disponibles, con un límite opcional."""
    subjects = Subject.objects.all()[:limit]
    return {'subjects': subjects}
```
Archivo de plantilla templates/subjects/subject_list.html:
```python
<ul>
    {% for subject in subjects %}
        <li>{{ subject.code }} - {{ subject.name }}</li>
    {% endfor %}
</ul>
```
En tu plantilla principal:
```python
{% load custom_tags %}

<h1>Materias Disponibles</h1>
{% show_subjects limit=3 %}
```
Esto generará una lista con las 3 primeras materias.

- 5. Crear Filtros Personalizados
Un filtro personalizado permite transformar un valor en otro. Por ejemplo, puedes crear un filtro que acorte el texto a una cantidad máxima de caracteres.

Ejemplo: Acortar Texto
```python
# templatetags/custom_tags.py

@register.filter
def truncate_chars(value, max_length):
    """Acorta un texto a una longitud máxima."""
    if len(value) > max_length:
        return value[:max_length] + "..."
    return value
```
En tu plantilla:
```python
{% load custom_tags %}

<p>{{ "Este es un texto muy largo" | truncate_chars:10 }}</p>
Salida:

<p>Este es...</p>
```
- 6. Agregar Variables al Tag

Puedes pasarle múltiples argumentos a los tags.

Ejemplo: Formatear Nombres
```python
# templatetags/custom_tags.py

@register.simple_tag
def format_name(first_name, last_name):
    """Formatea un nombre completo."""
    return f"{first_name.capitalize()} {last_name.capitalize()}"
```
En tu plantilla:
```python
{% load custom_tags %}

<p>{% format_name "juan" "perez" %}</p>
Salida:

<p>Juan Perez</p>
```
### Ejemplo Completo
```python
# templatetags/custom_tags.py

from django import template
from subjects.models import Subject

register = template.Library()

@register.simple_tag
def capitalize(text):
    """Convierte el texto a mayúsculas."""
    return text.upper()

@register.filter
def truncate_chars(value, max_length):
    """Acorta un texto a una longitud máxima."""
    if len(value) > max_length:
        return value[:max_length] + "..."
    return value

@register.inclusion_tag('subjects/subject_list.html')
def show_subjects(limit=5):
    """Muestra las materias disponibles, con un límite opcional."""
    subjects = Subject.objects.all()[:limit]
    return {'subjects': subjects}
```
Archivo de plantilla templates/subjects/subject_list.html:
```python
<ul>
    {% for subject in subjects %}
        <li>{{ subject.code }} - {{ subject.name }}</li>
    {% endfor %}
</ul>
```
En tu plantilla principal:
```python
{% load custom_tags %}

<h1>Materias Disponibles</h1>
<p>{% capitalize "hola mundo" %}</p>
<p>{{ "Texto muy largo para mostrar" | truncate_chars:15 }}</p>
{% show_subjects limit=3 %}
```

## Guía de señales

Señales Incorporadas en Django
Django proporciona señales predefinidas como:

- post_save: Enviada después de que se guarda un modelo.
- pre_save: Enviada antes de que se guarde un modelo.
- post_delete: Enviada después de que se elimina un modelo.
- pre_delete: Enviada antes de que se elimine un modelo.
- m2m_changed: Enviada cuando cambian relaciones Many-to-Many.

3. Crear una Señal

- Paso 1: Crear la Función de la Señal
Primero, define una función que se ejecutará cuando se dispare la señal.
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea un perfil automáticamente cuando se crea un usuario."""
    if created:
        Profile.objects.create(user=instance)
```

- Paso 2: Conectar la Señal
Django conecta automáticamente las señales cuando usas el decorador @receiver. Sin embargo, si prefieres, puedes conectarla manualmente:
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
```
4. ¿Dónde Colocar las Señales?

Es una buena práctica colocar las señales en un archivo llamado signals.py dentro de tu aplicación. Luego, importa el archivo en el método ready() de la configuración de la aplicación (apps.py) para asegurarte de que las señales estén registradas.

Estructura del Proyecto
myapp/
    apps.py
    models.py
    signals.py
Ejemplo: Registrar Señales en apps.py
```python
# apps.py
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        import myapp.signals
```
5. Señales Comunes y Ejemplos

- 5.1. Señal: post_save
Usada para ejecutar código después de guardar un modelo.
```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment

@receiver(post_save, sender=Enrollment)
def notify_student_enrollment(sender, instance, created, **kwargs):
    """Notifica al estudiante después de que se inscribe en una materia."""
    if created:
        print(f"Estudiante {instance.student} inscrito en {instance.subject}")
```

- 5.2. Señal: pre_save
Usada para realizar acciones antes de guardar un modelo.
```python
# signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Subject

@receiver(pre_save, sender=Subject)
def capitalize_subject_name(sender, instance, **kwargs):
    """Asegúrate de que el nombre del Subject esté capitalizado antes de guardarlo."""
    instance.name = instance.name.capitalize()
```

- 5.3. Señal: post_delete
Usada para ejecutar código después de eliminar un modelo.
```python
# signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Profile

@receiver(post_delete, sender=Profile)
def cleanup_user(sender, instance, **kwargs):
    """Elimina al usuario relacionado cuando se borra el perfil."""
    instance.user.delete()
```

- 5.4. Señal: m2m_changed
Usada para monitorear cambios en relaciones Many-to-Many.
```python
# signals.py
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Enrollment

@receiver(m2m_changed, sender=Enrollment)
def track_enrollment_changes(sender, instance, action, **kwargs):
    """Imprime un mensaje cuando cambian las inscripciones."""
    if action == 'post_add':
        print(f"Se añadieron estudiantes a {instance.subject}")
```

6. Crear Señales Personalizadas

Puedes definir tus propias señales y usarlas donde necesites.

Ejemplo: Señal Personalizada
Define la Señal:
```python
from django.dispatch import Signal

# Define una señal personalizada
student_enrolled = Signal()
```
Conecta la Señal:
```python
from django.dispatch import receiver
from .signals import student_enrolled

@receiver(student_enrolled)
def notify_teacher(sender, **kwargs):
    """Notifica al profesor cuando un estudiante se inscribe."""
    print(f"Estudiante inscrito: {kwargs['student_name']} en {kwargs['subject_name']}")
```
Envía la Señal:
```python
from .signals import student_enrolled

# Envía la señal en algún lugar de tu código
student_enrolled.send(sender=None, student_name="Juan Pérez", subject_name="Matemáticas")
```
### Ejemplo Completo

Modelo:
```python
# models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
```
Señal:
```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Crea automáticamente un perfil cuando se crea un usuario."""
    if created:
        Profile.objects.create(user=instance)
```
Registrar Señales:
```python
# apps.py
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        import myapp.signals
```