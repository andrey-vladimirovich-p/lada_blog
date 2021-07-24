from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField
from .models import Comment


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    captcha = CaptchaField(label='Введите текст с картинки', error_messages={'invalid': 'Неправильный текст'})


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    captcha = CaptchaField(label='Введите текст с картинки', error_messages={'invalid': 'Неправильный текст'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ContactForm(forms.Form):
    name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    subject = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Тема'}))
    content = forms.CharField(label=False, widget=forms.Textarea(attrs={'placeholder': 'Текст', 'rows': 5}))
    email = forms.EmailField(label=False, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    captcha = CaptchaField(label='Введите текст с картинки', error_messages={'invalid': 'Неправильный текст'},)


class GuestCommentForm(forms.ModelForm):
    captcha = CaptchaField(label='Введите текст с картинки:  ', error_messages={'invalid': 'Неправильный текст'},)

    class Meta:
        model = Comment
        exclude = ['is_active', ]
        widgets = {'article': forms.HiddenInput,
                   'created_ad': forms.HiddenInput,
                   'content': forms.Textarea(attrs={'placeholder': 'Текст комментария', 'rows': 6}),
                   'author': forms.TextInput(attrs={'placeholder': 'Имя автора'}),
                   'email': forms.TextInput(attrs={'placeholder': 'Email'}),

                   }


class UserCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['is_active', ]
        widgets = {'article': forms.HiddenInput,
                   'email': forms.HiddenInput,
                   'author': forms.HiddenInput,
                   'created_ad': forms.HiddenInput,
                   'content': forms.Textarea(attrs={'placeholder': 'Текст комментария', 'rows': 1}),
                   }