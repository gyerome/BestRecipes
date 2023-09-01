from . import constants
from django.db.models.query import QuerySet
from .constants import CHUNK_SIZE
from django.views.defaults import bad_request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from .models import Recipe, Category, Forum, Comment, UserSubscribes, Forum_theme
from user.models import User
from django.core.mail import send_mail

def index(request: HttpRequest):
    return render(request, 'index.html', context={'categories': Category.objects.all(),
                                                  'state': request.GET.get('s')})

def forums(request: HttpRequest):
    if request.GET.get('question') is not None:
        return render(request, 'question.html')

    return render(request, 'forums.html', context={'themes':Forum_theme.objects.all()})

def user_page(request: HttpRequest, user_id: int):
    try:
        context = {
            'user': User.objects.get(id=user_id),
            'categories': Category.objects.all()
        }

    except User.DoesNotExist as e:
        return HttpResponseNotFound('Пользователя не существует')

    return render(request, 'UserPage.html', context=context)

@login_required(login_url='/?s=login')
def my_page(request: HttpRequest):
    return render(request, 'UserPage.html', context={'categories': Category.objects.all(),
                                                     'user': request.user})


def authors(request: HttpRequest):
    return render(request, 'authors.html')


def get_chunk(model):
    '''Generate function for returning posts, users, forums'''
    def decorator(function, model=model):
        def wrapper(request: HttpRequest):
            chunks_quantity = request.GET.get('chunks_quantity')
            search = request.GET.get('search')

            try: chunks_quantity = int(chunks_quantity)
            except (ValueError, TypeError) as e: bad_request(request, e)

            first_id = chunks_quantity*constants.CHUNK_SIZE
            last_id = (chunks_quantity+1)*constants.CHUNK_SIZE
            if search is not None: queryset = model.objects.filter(name__icontains=search)
            else: queryset = model.objects

            print(queryset)
            chunk_data = function(request, queryset, first_id, last_id)

            return chunk_data

        return wrapper
    return decorator

@get_chunk(Recipe)
def get_recipes(request: HttpRequest, queryset: QuerySet, first_id, last_id):
    filters = {'isBlocked':False}
    category = request.GET.get('category')
    user = request.GET.get('user')
    type = request.GET.get('type')
    try:
        if category is not None:
            category = int(category)
            category = Category.objects.get(id=category)
            filters['category'] = category

        if user is not None:
            user = int(user)
            user = User.objects.get(id=user)
            filters['author'] = user

    except (Category.DoesNotExist, User.DoesNotExist, TypeError) as e: return bad_request(request, e)

    if type is not None:
        filters['author__in'] = UserSubscribes.objects.filter(subscriber=request.user).values('author')

    chunk_data = queryset.filter(**filters).order_by('-views')[first_id:last_id]
    #desc(- в начале строки) для даты и рейтинга работает, но при добавлении нового может возникнуть ошибка

    if len(chunk_data) == 0:
        return HttpResponse(status=404)

    return render(request, 'recipe.html', context={'recipes':chunk_data})


@get_chunk(User)
def get_authors(request: HttpRequest, queryset: QuerySet, first_id, last_id):
    chunk_data = queryset.exclude(id=request.user.id).filter(is_staff=False, is_active=True).order_by('-rating')[first_id:last_id]

    if len(chunk_data) == 0:
        return HttpResponse(status=404)

    loaded_authors = request.GET.get('chunks_quantity')*CHUNK_SIZE
    return render(request, 'author.html', context={'authors':chunk_data,
                                                   'loaded_authors': loaded_authors})



@get_chunk(Forum)
def get_forums(request: HttpRequest, queryset: QuerySet, first_id, last_id):
    sorting = request.GET.get('order_by')
    category = request.GET.get('category')
    if sorting is None: sorting = constants.POPULAR

    chunk_data = queryset

    if sorting == constants.SUBSCRIBES:
        subscribes = UserSubscribes.objects.filter(subscriber=request.user).values('author')
        chunk_data = chunk_data.filter(theme__id=category).filter(author__in=subscribes).order_by('-date')[first_id:last_id]

    else:
        chunk_data = chunk_data.filter(theme__id=category).order_by(f'-{sorting}')[first_id:last_id]


    if len(chunk_data) == 0:
        return HttpResponseNotFound('Такой страницы не существует')

    return render(request, 'forumCard.html', context={'forums':chunk_data})

def question(request: HttpRequest, forum_id):
    try:
        context = {
            'forum': Forum.objects.get(id=forum_id),
            'comments': Comment.objects.filter(forum__id=forum_id).order_by('-date')
        }
    except Forum.DoesNotExist as e:
        return HttpResponse(status=404)


    return render(request, 'question.html', context=context)


def recipe_page(request: HttpRequest, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    if request.user != recipe.author:
        recipe.add_view()

    context = {
        'recipe': recipe,
    }

    send_mail('test', 'Is message sent?', 'limon20049@mail.ru', ['limjnger@gmail.com',], fail_silently=False)

    print('sent?')
    return render(request, 'recipePage.html', context)


