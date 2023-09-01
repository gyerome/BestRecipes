from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.http import HttpRequest
from .forms import UserFieldChangeForm, PasswordChangeActualForm, PasswordChangeForm, UserLoginForm, UserRegisterForm
from django.contrib.auth import views as auth_views, logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from recipes import settings

class UserFieldChangeView(FormView):
    form_class = UserFieldChangeForm
    success_url = '/me'
    template_name = 'userFieldChange.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data()
        kwargs['field'] = self.request.GET.get('field')
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginUser(LoginView):
    template_name = 'auth.html'
    redirect_authenticated_user = True
    form_class = UserLoginForm
    next_page = '/'

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form), status=401)


class PasswordChangeView(auth_views.PasswordChangeView):
    form_class = PasswordChangeActualForm
    template_name = 'changePassword.html'
    success_url = '/me'


def delete_menu(request: HttpRequest):
    return render(request, 'deleteAccept.html')


def delete_account(request: HttpRequest):
    request.user.is_active = False
    request.user.save()
    logout(request)
    return redirect('/')


def logout_view(request: HttpRequest):
    logout(request)
    return redirect('/')


def register_user(request: HttpRequest):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect("/")
    else:
        form = UserRegisterForm()

    return render(request, "registration.html", {"form": form})


class PasswordResetActualView(PasswordResetView):
    from_email = settings.EMAIL_HOST_USER
    template_name = 'resetPassword.html'