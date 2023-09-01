from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('subscribe', views.subscribe),
    path('makeforum', views.NewForumView.as_view()),
    path('newrecipe', views.NewRecipeView.as_view()),
    path('newcomment', views.NewCommentView.as_view()),
]