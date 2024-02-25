from .models import Board, Thread, Post, Task
from django import forms
import re
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import get_user_model


class RegistrationForm(forms.Form):
    username = forms.CharField(label='User name', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='repeat password', widget=forms.PasswordInput())


    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError('Неправильный пароль')

    def clean_username(self):
        usern = self.cleaned_data['username']
        if not re.search(pattern=r'^\w+$', string=usern):
            raise forms.ValidationError('Имя учетной записи не может содержать специальные символы')
        try:
            User.objects.get(username=usern)
        except ObjectDoesNotExist:
            return usern
        raise forms.ValidationError('Аккаунт уже существует')

    def save_user(self):
        User.objects.create_user(self.cleaned_data['username'], email=self.cleaned_data['email'],
                                 password=self.cleaned_data['password1'])

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.UserID = kwargs.pop('UserID', None)
        self.ThreadID = kwargs.pop('ThreadID', None)
        super().__init__(*args, **kwargs)


    def save(self, commit=True):
        post = super().save(commit=False)
        post.UserID = self.UserID
        post.ThreadID = self.ThreadID
        post.save()

    class Meta:
        model = Post
        fields = ['Content']


class ThreadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.UserID = kwargs.pop('UserID', None)
        self.Board = kwargs.pop('Board', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        thread = super().save(commit=False)
        thread.UserID = self.UserID
        thread.Board = self.Board
        if commit:
            thread.save()
        return thread

    class Meta:
        model = Thread
        fields = ['Tittle', 'Content']


class TaskForm(forms.ModelForm):
    title = forms.CharField(label='Название задачи', max_length=100)
    description = forms.CharField(label='Описание задачи', widget=forms.Textarea)
    due_date = forms.DateField(label='Дата завершения', widget=forms.DateInput(attrs={'type': 'date'}))
    attached_file = forms.FileField(label='Прикрепить файл', required=False)  # required=False, если файл необязателен

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'attached_file']

class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']  # Включаем новое поле bio

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs['class'] = 'your-custom-class'