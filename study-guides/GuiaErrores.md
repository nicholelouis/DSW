# Guía de Errores Comunes en Django

Esta guía cubre algunos de los errores más frecuentes al desarrollar una página web con Django. Cada sección incluye una breve descripción del error, posibles causas y sus soluciones.

---

## 1. **Error: `ModuleNotFoundError: No module named 'app'`**

### Descripción
Ocurre cuando Django no encuentra el módulo o aplicación especificada.

### Causa
- La aplicación no está incluida en `INSTALLED_APPS` dentro del archivo `settings.py`.
- El nombre del módulo o aplicación está mal escrito.

### Solución
1. Verificar que la aplicación está agregada correctamente en `INSTALLED_APPS` de `settings.py`:
    ```python
    INSTALLED_APPS = [
        ...
        'mi_app',
    ]
    ```
2. Revisar que el nombre de la aplicación esté correctamente escrito y sin errores tipográficos.

---

## 2. **Error: `TemplateDoesNotExist`**

### Descripción
Django no puede encontrar la plantilla (template) solicitada.

### Causa
- El archivo de plantilla no está en el directorio correcto.
- La configuración de directorios de plantillas en `settings.py` es incorrecta.
- Error en el nombre del archivo o extensión incorrecta (por ejemplo, `.html` en vez de `.htm`).

### Solución
1. Verificar que la plantilla existe en la carpeta de templates configurada.
2. Asegurarse de que el archivo `settings.py` tenga configurado el directorio de templates:
    ```python
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
            ...
        },
    ]
    ```
3. Confirmar que el nombre del archivo en el `render()` del view esté correctamente escrito:
    ```python
    return render(request, 'nombre_plantilla.html')
    ```

---

## 3. **Error: `ProgrammingError: relation "<nombre_de_tabla>" does not exist`**

### Descripción
Este error indica que Django no encuentra una tabla de base de datos.

### Causa
- Falta ejecutar las migraciones necesarias en la base de datos.
- La tabla no fue creada debido a errores previos en las migraciones.

### Solución
1. Ejecutar las migraciones:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
2. Si el problema persiste, verificar el historial de migraciones o eliminar y rehacer migraciones (con precaución en producción).

---

## 4. **Error: `FieldError: Unknown field(s) (field_name) specified for Model`**

### Descripción
Django intenta acceder a un campo que no existe en el modelo especificado.

### Causa
- Nombre incorrecto del campo en el modelo.
- El campo fue eliminado del modelo, pero aún está en uso en alguna vista o plantilla.

### Solución
1. Revisar que el nombre del campo exista en el modelo y esté correctamente escrito.
2. Asegurarse de que todos los cambios en el modelo están migrados con:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

---

## 5. **Error: `ImportError: Could not import settings '<nombre_proyecto>.settings'`**

### Descripción
Django no puede encontrar o importar el archivo de configuración `settings.py`.

### Causa
- El archivo `settings.py` no existe o está mal ubicado.
- Error de configuración en el archivo `manage.py` o `wsgi.py`.

### Solución
1. Asegurarse de que el archivo `settings.py` esté en el directorio del proyecto.
2. Revisar que en `manage.py` y `wsgi.py` se esté referenciando correctamente:
    ```python
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nombre_proyecto.settings')
    ```

---

## 6. **Error: `OperationalError: no such table: django_session`**

### Descripción
Indica que Django no encuentra la tabla `django_session`, que se usa para el manejo de sesiones.

### Causa
- Falta la migración inicial para crear las tablas de la base de datos.
- La base de datos ha sido modificada o eliminada.

### Solución
1. Ejecutar migraciones para asegurarse de que las tablas estén creadas:
    ```bash
    python manage.py migrate
    ```
2. Si el error persiste, puede ser necesario reiniciar la base de datos (precaución en producción).

---

## 7. **Error: `TypeError: __init__() got an unexpected keyword argument 'nombre_argumento'`**

### Descripción
Django intenta usar un argumento en un modelo o vista que no es válido.

### Causa
- Error en el modelo, vista o formulario donde se está pasando un argumento incorrecto.

### Solución
1. Verificar la definición del modelo o función afectada.
2. Eliminar o corregir el argumento problemático.

---

## 8. **Error: `IntegrityError: UNIQUE constraint failed`**

### Descripción
Se produce cuando Django intenta guardar un valor duplicado en un campo único.

### Causa
- Intenta insertarse un valor duplicado en un campo que tiene restricciones `unique=True`.

### Solución
1. Verificar que los datos cumplen con las restricciones únicas.
2. Utilizar `get_or_create()` en vez de `create()` si el objeto puede existir previamente.

---

## 9. **Error: `DisallowedHost: Invalid HTTP_HOST header`**

### Descripción
Ocurre cuando el dominio o host de la solicitud no está en la lista de hosts permitidos.

### Causa
- El dominio o IP no está en la lista `ALLOWED_HOSTS` de `settings.py`.

### Solución
1. Añadir el dominio/IP en `ALLOWED_HOSTS`:
    ```python
    ALLOWED_HOSTS = ['mi_dominio.com', 'localhost']
    ```

---

## 10. **Error: `CSRF verification failed`**

### Descripción
Django bloquea la solicitud debido a una verificación CSRF fallida.

### Causa
- La vista está intentando procesar un formulario POST sin el token CSRF correcto.

### Solución
1. Asegurarse de que la plantilla incluye el token CSRF:
    ```html
    <form method="POST">
        {% csrf_token %}
        ...
    </form>
    ```
2. Para APIs o vistas sin formularios HTML, se puede deshabilitar temporalmente la verificación CSRF usando el decorador:
    ```python
    from django.views.decorators.csrf import csrf_exempt

    @csrf_exempt
    def mi_vista(request):
        ...
    ```
---

## Conclusión

Estos son algunos de los errores más comunes al desarrollar una página web con Django. Si encuentras otros errores, consulta la documentación oficial de Django o utiliza `stack trace` del error para diagnosticar y solucionar el problema.
