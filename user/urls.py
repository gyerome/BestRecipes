from django.urls import path
from . import views


urlpatterns = [
    path('changep', views.PasswordChangeView.as_view()),
    path('changefield', views.UserFieldChangeView.as_view()),
    path('deleteme', views.delete_account),
    path('deletemenu', views.delete_menu),
    path('logout', views.logout_view),
    path('password-reset', views.PasswordResetActualView.as_view()),
    path('password-reset-done', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register', views.register_user, name='register'),
    path('auth', views.LoginUser.as_view()),
]