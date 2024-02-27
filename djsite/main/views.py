from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Board, Thread, Task, Chat
from django.http import HttpResponseRedirect
from .forms import RegistrationForm, ThreadForm, CommentForm, TaskForm, ChatForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


# Create your views here.
def index(request):
    Data = {
        'Boards1': Board.objects.all()[:3],
        'Boards2': Board.objects.all()[3:9],
        'Boards3': Board.objects.all()[9:13],
        'Boards4': Board.objects.all()[13:16],
        'Boards5': Board.objects.all()[16:19],
        'Threads': Thread.objects.all()[:10],
        'Users': User.objects.all()
    }
    return render(request, template_name="main/index.html", context=Data)


def index_board(request, id):
    Boards = get_object_or_404(Board, pk=id)
    form = ThreadForm
    if request.method == 'POST':
        form = ThreadForm(request.POST, UserID=request.user, Board=Boards)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)

    Data = {'Boards': Board.objects.get(pk=id), 'form': form, 'Threads': Thread.objects.all().order_by("-Time_Created")[:10]}
    return render(request, template_name="main/index_board.html", context=Data)


def index_thread(request, id):
    thread = get_object_or_404(Thread, pk=id)
    form = CommentForm
    if request.method == 'POST':
        form = CommentForm(request.POST, UserIS=request.user, ThreadID = thread)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    Data = {'thread': thread, "form": form, "Threads": Thread.objects.all().order_by("-Time_Created")[:]}
    return render(request, template_name="main/index_thread.html", context = Data)


def index_user(request, username):
    Data = {'User':User.objects.get(username=username), 'Threads': Thread.objects.all().order_by("-Time_Created")[:10]}
    return render(request, template_name="main/index_user.html", context = Data)

def index_posts(request):
    tasks = Task.objects.all().order_by("-created_at")
    return render(request, "main/index_posts.html", {'tasks': tasks})

def index_users(request):
    Data = {'Users': User.objects.all().order_by("-date_joined"), 'Threads': Thread.objects.all().order_by("-Time_Created")[:10]}
    return render(request, template_name="main/index_users.html", context=Data)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'main/task_list.html', {'tasks': tasks})

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm()
    return render(request, 'main/create_task.html', {'form': form})

def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    chats = task.chats.all()
    if request.method == 'POST':
        chat_form = ChatForm(request.POST)
        if chat_form.is_valid():
            chat = chat_form.save(commit=False)
            chat.task = task
            chat.sender = request.user
            chat.save()
            return redirect('task_detail', task_id=task.id)
    else:
        chat_form = ChatForm()
    return render(request, 'main/task_detail.html', {'task': task, 'chats': chats, 'chat_form': chat_form})

def create_chat(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        message = request.POST.get('message')
        sender = request.user
        Chat.objects.create(task=task, message=message, sender=sender)
        return redirect('task_detail', task_id=task_id)

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'main/profile.html', {'profile_form': profile_form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Перенаправление на профиль после успешной аутентификации
    return render(request, 'main/login.html')

@login_required
def profile(request):
    return render(request, 'main/profile.html')
