from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('forum', views.forums, name='forum'),
    path('authors', views.authors, name='authors'),
    path('chunks/recipes', views.get_recipes),
    path('chunks/authors', views.get_authors),
    path('chunks/forums', views.get_forums),
    path('authors/<int:user_id>/', views.user_page),
    path('me/', views.my_page),
    path('authors/me', views.my_page),
    path('forum/<int:forum_id>/', views.question),
    path('recipe/<int:recipe_id>/', views.recipe_page),
]\
    +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

