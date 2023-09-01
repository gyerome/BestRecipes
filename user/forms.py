from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UsernameField, AuthenticationForm, UserCreationForm
from user.models import User


class PasswordChangeActualForm(PasswordChangeForm):
    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'auth-field', 'placeholder': 'Старый пароль'}),
        error_messages={'required': 'Введите ваш пароль'}
    )

    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'auth-field', 'placeholder': 'Новый пароль'}),
        error_messages={'required': 'Введите новый пароль'}
    )

    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'auth-field', 'placeholder': 'Повторите новый пароль'}),
        error_messages={'required': 'Повторите новый пароль'}
    )


class UserFieldChangeForm(forms.ModelForm):
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class':'description-field auth-field'}),
    )

    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={}),
    )

    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class':'auth-field', 'placeholder':'Новое имя пользователя'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].empty_value = self.instance.username

    class Meta:
        model = User
        fields = ('avatar', 'description', 'username')


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'auth-field', 'placeholder': 'Эл. почта или имя пользователя', 'id': 'ident'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'auth-field',
            'placeholder': 'Пароль',
            'id': 'password',
        }
))


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'name':'ident', 'id':'email', 'class':'auth-field', 'placeholder':'Эл. почта'}))

    username = UsernameField(widget=forms.TextInput(
        attrs={'id':'username',  'class':'auth-field', 'placeholder':"Имя пользователя"}))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'name':"password",  'id':'password',  'class':'auth-field', 'placeholder':"Пароль"}))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'name':"password",  'id':'password',  'class':'auth-field', 'placeholder':"Пароль"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

