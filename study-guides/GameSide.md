# Gameside

Proyectos de apis para ventas de juesgos online. Contamos con `6 aplicaciones`

1. Shared
2. Games
3. Platforms
4. Categories
5. Orders
6. Users

## App Games

### Modelos

Dentro de games tenemos dos modelos 

#### games.Game

```python
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Game(models.Model):
    class Pegi(models.IntegerChoices):
        PEGI3 = 3
        PEGI7 = 7
        PEGI12 = 12
        PEGI16 = 16
        PEGI18 = 18

    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='covers', default='covers/default.jpg')
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    stock = models.IntegerField()
    released_at = models.DateField()
    pegi = models.IntegerField(
        choices=Pegi,
    )
    category = models.ForeignKey(
        'categories.Category',
        related_name='game_categories',
        on_delete=models.SET_NULL,
        null=True,
    )
    platforms = models.ManyToManyField(
        'platforms.Platform',
        related_name='game_platforms',
    )

    def __str__(self):
        return self.title
    
    def update_stock(self, num, action):
        match action:
            case 'add':
                self.stock += num
            case 'remove':
                self.stock += num

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('games:game-detail', kwargs={'game_slug': self.slug})
```

#### games.Review

```python
class Review(models.Model):
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=5),
        ]
    )
    game = models.ForeignKey(Game, related_name='game_reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_reviews',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('games:review-detail', kwargs={'review_pk': self.pk})
```

### Urls

```python
from django.urls import path

from . import views

app_name = 'games'


urlpatterns = [
    path('', views.game_list, name='game-list'),
    path('filter/', views.game_list, name='game-list'),
    path('<str:game_slug>/', views.game_detail, name='game-detail'),
    path('<str:game_slug>/reviews/', views.review_list, name='review-list'),
    path('reviews/<int:review_pk>/', views.review_detail, name='review-detail'),
    path('<str:game_slug>/reviews/add/', views.add_review, name='add-review'),
]
```

### Views

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import (
    check_json_body,
    method_required,
    required_fields,
    token_exists,
    valid_token,
)

from .helpers import game_exist, review_exist
from .models import Game, Review
from .serializer import GameSerializer, ReviewSerializer


@method_required('get')
def game_list(request):
    if category := request.GET.get('category'):
        games = Game.objects.filter(category__slug=category)
    if platform := request.GET.get('platform'):
        games = Game.objects.filter(platforms__slug=platform)
    if len(request.GET.keys()) == 2:
        category = request.GET.get('category')
        platform = request.GET.get('platform')
        games = Game.objects.filter(platforms__slug=platform, category__slug=category)
    else:
        games = Game.objects.all()

    games_json = GameSerializer(games, request=request)
    return games_json.json_response()


@method_required('get')
@game_exist
def game_detail(request, game_slug):
    game_json = GameSerializer(request.game, request=request)
    return game_json.json_response()


@method_required('get')
@game_exist
def review_list(request, game_slug):
    reviews = request.game.game_reviews.all()
    review_json = ReviewSerializer(reviews, request=request)
    return review_json.json_response()


@method_required('get')
@review_exist
def review_detail(request, review_pk):
    review_json = ReviewSerializer(request.review, request=request)
    return review_json.json_response()


@csrf_exempt
@method_required('post')
@check_json_body
@required_fields('rating', 'comment')
@valid_token
@token_exists
@game_exist
def add_review(request, game_slug):
    user = request.user
    print(user)
    rating = int(request.json_body['rating'])
    if rating < 1 or rating > 5:
        return JsonResponse({'error': 'Rating is out of range'}, status=400)
    review = Review.objects.create(
        game=request.game,
        author=user,
        rating=rating,
        comment=request.json_body['comment'],
    )
    return JsonResponse({'id': review.pk})
```

### Serializers

```python
from categories.serializer import CategorySerializer
from platforms.serializer import PlatformSerializer
from shared.serializers import BaseSerializer
from users.serializer import UserSerializer


class GameSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'title': instance.title,
            'slug': instance.slug,
            'description': instance.description,
            'cover': self.build_url(instance.cover.url),
            'price': float(instance.price),
            'released_at': instance.released_at.isoformat(),
            'pegi': instance.get_pegi_display(),
            'stock': instance.stock,
            'category': CategorySerializer(instance.category, request=self.request).serialize(),
            'platforms': PlatformSerializer(
                instance.platforms.all(), request=self.request
            ).serialize(),
        }


class ReviewSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'rating': instance.rating,
            'comment': instance.comment,
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'author': UserSerializer(instance.author, request=self.request).serialize(),
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
        }
```

* Usa ``.isoformat()`` para las fechas
* Cuando quieres pasar por un serializador un objeto serializable tienes que serializarlo tambien su serializador pertinente (pasale el request)
* usa el `get_..._display()` para los enum cuando quieres el valor como tal
* Al pasarle varias cosas al serializador usa el .all() para pasarselos a su serializados 
```python
'platforms': PlatformSerializer(
                instance.platforms.all(), request=self.request
            ).serialize(),
```

### Helpers.py

```python
from django.http import JsonResponse

from .models import Game, Review


def game_exist(func):
    def wrapper(*args, **kwargs):
        try:
            game = Game.objects.get(slug=kwargs['game_slug'])
            args[0].game = game
            return func(*args, **kwargs)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)

    return wrapper


def review_exist(func):
    def wrapper(*args, **kwargs):
        try:
            review = Review.objects.get(pk=kwargs['review_pk'])
            args[0].review = review
            return func(*args, **kwargs)
        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review not found'}, status=404)

    return wrapper
```

## App Orders

### Models

```python
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.


class Order(models.Model):
    class Status(models.IntegerChoices):
        INITIATED = 1, 'Initiated'
        CONFIRMED = 2, 'Confirmed'
        PAID = 3, 'Paid'
        CANCELLED = -1, 'Cancelled'

    status = models.IntegerField(choices=Status, default=Status.INITIATED)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_orders',
        on_delete=models.CASCADE,
    )
    games = models.ManyToManyField('games.Game', related_name='order_games', null=True)
    price = 0

    def get_absolute_url(self):
        return reverse('orders:order-detail', kwargs={'order_pk': self.pk})

    def __str__(self):
        return f'Order estado:{self.status}, User: {self.user}'

    def change_status(self, status: int):
        self.status = status

    def is_initiated(self):
        return self.status == 1

    def num_games_in_order(self):
        return self.games.all().count()

    def add_game(self, game):
        self.games.add(game)
        game.stock -= 1

    @property
    def get_price(self):
        self.price = sum([game.price for game in self.games.all()])
```

### Urls

```python
from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.add_order, name='add-order'),
    path('<int:order_pk>/', views.order_detail, name='order-detail'),
    path('<int:order_pk>/confirm/', views.confirm_order, name='confirm-order'),
    path('<int:order_pk>/cancel/', views.cancel_order, name='cancel-order'),
    path('<int:order_pk>/pay/', views.pay_order, name='pay-order'),
    path('<int:order_pk>/games/', views.order_game_list, name='order-game-list'),
    path(
        '<int:order_pk>/games/add/<str:game_slug>/',
        views.add_game_to_order,
        name='add-game-to-order',
    ),
]
```

### Views

```python
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from games.helpers import game_exist
from games.serializer import GameSerializer
from shared.decorators import (
    check_json_body,
    method_required,
    required_fields,
    user_owner,
    valid_token,
    token_exists,
)

from .helpers import order_exist, status_errors, validate_card
from .models import Order
from .serializer import OrderSerializer


@method_required('post')
@check_json_body
@valid_token
@token_exists
@csrf_exempt
def add_order(request):
    user = request.user
    order = Order.objects.create(user=user)
    order_json = OrderSerializer(order, request=request)
    return order_json.json_response()


@method_required('post')
@check_json_body
@valid_token
@token_exists
@order_exist
@csrf_exempt
@user_owner
def order_game_list(request, order_pk):
    game_json = GameSerializer(request.order.games.all(), request=request)
    return game_json.json_response()


@method_required('post')
@check_json_body
@valid_token
@token_exists
@order_exist
@csrf_exempt
@user_owner
def order_detail(request, order_pk):
    order_json = OrderSerializer(request.order, request=request)
    return order_json.json_response()


@method_required('post')
@check_json_body
@valid_token
@token_exists
@order_exist
@csrf_exempt
@user_owner
@status_errors('confirmed')
def confirm_order(request, order_pk):
    order = request.order
    order.change_status(2)
    order.save()
    return JsonResponse({'status': order.get_status_display()})


@method_required('post')
@check_json_body
@valid_token
@token_exists
@order_exist
@csrf_exempt
@user_owner
@status_errors('cancelled')
def cancel_order(request, order_pk):
    order = request.order
    order.change_status(-1)
    order.save()
    for game in order.games.all():
        game.update_stock(1, 'add')
        game.save()
    return JsonResponse({'status': order.get_status_display()})


@method_required('post')
@check_json_body
@required_fields('card-number', 'exp-date', 'cvc')
@valid_token
@token_exists
@order_exist
@csrf_exempt
@user_owner
@status_errors('paid')
@validate_card
def pay_order(request, order_pk):
    order = request.order
    order.change_status(3)
    order.save()
    return JsonResponse({'status': order.get_status_display()})


@method_required('post')
@check_json_body
@valid_token
@token_exists
@order_exist
@game_exist
@csrf_exempt
@user_owner
def add_game_to_order(request, order_pk, game_slug):
    order = request.order
    game = request.game
    order.add_game(game)
    return JsonResponse({'num-games-in-order': order.num_games_in_order()})
```

### Serializer

```python
from games.serializer import GameSerializer
from shared.serializers import BaseSerializer
from users.serializer import UserSerializer


class OrderSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'status': instance.get_status_display(),
            'user': UserSerializer(instance.user, request=self.request).serialize(),
            'key': instance.key if instance.status == 3 else None,
            'games': GameSerializer(instance.games.all(), request=self.request).serialize(),
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
            'price': float(instance.price),
        }
```

### Helpers

```python
import re
from datetime import datetime

from django.http import JsonResponse

from .models import Order


def order_exist(func):
    def wrapper(request, *args, **kwargs):
        try:
            order = Order.objects.get(pk=kwargs['order_pk'])
            request.order = order
            return func(request, *args, **kwargs)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

    return wrapper


def regex_validator(key: str, regex: str, request) -> bool:
    return re.match(regex, request.json_body[key]) is None


def validate_card(func):
    def wrapper(request, *args, **kwargs):
        regex_num_card = r'^[0-9]{4}(-[0-9]{4}){3}$'
        regex_exp_date = r'^(0[1-9]|1[0-2])/\d{4}$'
        regex_cvc = r'^\d{3}$'

        error = None
        if regex_validator(key='card-number', regex=regex_num_card, request=request):
            error = 'Invalid card number'
        if regex_validator(key='exp-date', regex=regex_exp_date, request=request):
            error = 'Invalid expiration date'
        if regex_validator(key='cvc', regex=regex_cvc, request=request):
            error = 'Invalid CVC'
        try:
            card_date = datetime.strptime(request.json_body['exp-date'] , '%m/%Y')
            current_date = datetime.now()
            if current_date >= card_date:
                error = 'Card expired'
        except ValueError:
            None

        if error:
            return JsonResponse({'error': f'{error}'}, status=400)

        return func(request, *args, **kwargs)

    return wrapper


def status_errors(status):
    status = status.upper()

    def decorator(func):
        def wrapper(request, *args, **kwargs):
            order = request.order
            match status:
                case 'CONFIRMED':
                    if order.is_initiated():
                        return func(request, *args, **kwargs)
                    return JsonResponse(
                        {'error': 'Orders can only be confirmed when initiated'}, status=400
                    )
                case 'CANCELLED':
                    if order.is_initiated():
                        return func(request, *args, **kwargs)
                    return JsonResponse(
                        {'error': 'Orders can only be cancelled when initiated'}, status=400
                    )
                case 'PAID':
                    if order.status == 2:
                        return func(request, *args, **kwargs)
                    return JsonResponse(
                        {'error': 'Orders can only be paid when confirmed'}, status=400
                    )

        return wrapper

    return decorator
```

## App Users

### Models

Modelo para guardar el token de autenticacion de cada usuario.
```python
import uuid

from django.conf import settings
from django.db import models

class Token(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='token',
        on_delete=models.CASCADE,
    )
    key = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

```

### Urls

```python
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.auth, name='auth'),
]
```

### Views

```python
from django.http import JsonResponse

from shared.decorators import auth_required, check_json_body, method_required, required_fields


@method_required('post')
@check_json_body
@required_fields('username', 'password')
@auth_required
def auth(request):
    print(request.user)
    return JsonResponse({'token': request.user.token.key})
```

### Serializer

```python
from shared.serializers import BaseSerializer

class UserSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
        }

class TokenSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'key': instance.key,
            'created_at': instance.created_at.isoformat(),
        }
```

Hay que hacer el serializer del user

## Shared ‼️

### Serializador base

```python
import json
from abc import ABC
from typing import Iterable

from django.http import HttpRequest, JsonResponse


class BaseSerializer(ABC):
    def __init__(
        self,
        to_serialize: object | Iterable[object],
        *,
        fields: Iterable[str] = [],
        request: HttpRequest = None,
    ):
        self.to_serialize = to_serialize
        self.fields = fields
        self.request = request

    def build_url(self, path: str) -> str:
        return self.request.build_absolute_uri(path) if self.request else path

    # To be implemented by subclasses
    def serialize_instance(self, instance: object) -> dict:
        raise NotImplementedError

    def __serialize_instance(self, instance: object) -> dict:
        serialized = self.serialize_instance(instance)
        return {f: v for f, v in serialized.items() if not self.fields or f in self.fields}

    def serialize(self) -> dict | list[dict]:
        if not isinstance(self.to_serialize, Iterable):
            return self.__serialize_instance(self.to_serialize)
        return [self.__serialize_instance(instance) for instance in self.to_serialize]

    def to_json(self) -> str:
        return json.dumps(self.serialize())

    def json_response(self) -> str:
        return JsonResponse(self.serialize(), safe=False)
```

### Decoradores

```python
import json
import re
from json.decoder import JSONDecodeError

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse

from orders.models import Order
from users.models import Token

from .helpers import get_token

""" 
def auth_required(func):
    def wrapper(request, *args, **kwargs):
        json_post = json.loads(request.body)
        print(json_post)
        user = get_user_model()
        try:
            user = user.objects.get(token__key=json_post['token'])
            request.json_post = json_post
            return func(request, *args, **kwargs)
        except user.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=401)

    return wrapper """


def auth_required(func):
    def wrapper(request, *args, **kwargs):
        if user := authenticate(
            username=request.json_body['username'], password=request.json_body['password']
        ):
            request.user = user
            return func(request, *args, **kwargs)
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return wrapper


def token_exists(func):
    def wrapper(request, *args, **kwargs):
        try:
            request.user = User.objects.get(token__key=request.token)
            return func(request, *args, **kwargs)
        except:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

    return wrapper


def valid_token(func):
    def wrapper(request, *args, **kwargs):
        auth = request.headers.get('Authorization', 'no existe')
        regexp = 'Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
        if auth_value := re.fullmatch(regexp, auth):
            request.token = auth_value["token"]
            return func(request, *args, **kwargs)
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)

    return wrapper


def method_required(method):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method == method.upper():
                return func(request, *args, **kwargs)
            return JsonResponse({'error': 'Method not allowed'}, status=405)

        return wrapper

    return decorator


def check_json_body(func):
    def wrapper(request, *args, **kwargs):
        try:
            json_body = json.loads(request.body)
            request.json_body = json_body
            return func(request, *args, **kwargs)
        except JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    return wrapper


def user_owner(func):
    def wrapper(request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['order_pk'])
        user = request.user
        if order.user == user:
            return func(request, *args, **kwargs)
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

    return wrapper


def required_fields(*fields):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            json_body = json.loads(request.body)
            for field in fields:
                if field not in json_body:
                    return JsonResponse({'error': 'Missing required fields'}, status=400)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
```

### Helpers

```python
import re


def get_token(value: str):
    regexp = 'Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
    if auth_value := re.fullmatch(regexp, value):
        return auth_value['token']
    return False
```

## Forma más pythonica de hacer un filter en la url

```python
from django.db.models import Q

@method_required('get')
def game_list(request):
    category = request.GET.get('category')
    platform = request.GET.get('platform')

    filters = Q()
    if category:
        filters &= Q(category__slug=category)
    if platform:
        filters &= Q(platforms__slug=platform)

    games = Game.objects.filter(filters) if filters else Game.objects.all()
    
    games_json = GameSerializer(games, request=request)
    return games_json.json_response()
```

Q es una clase de Django que permite construir consultas dinámicas y más complejas usando operadores lógicos (& para "AND", | para "OR", ~ para "NOT"). Se encuentra en django.db.models.

Se usa cuando necesitas combinar múltiples condiciones en una consulta de base de datos de forma flexible.

