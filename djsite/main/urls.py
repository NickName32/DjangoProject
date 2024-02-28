from django.urls import path
from . import views
from .models import Thread
from django.contrib.auth import views as auth_views
from .views import CustomLoginView


urlpatterns = [
    path('', views.index, name="index"),
    path('<int:task_id>/', views.task_detail, name='task_detail'),
    path('<int:task_id>/create_chat/', views.create_chat, name='create_chat'),
    path('board/<int:id>/', views.index_board, name = "index_board"),
    path('thread/<int:id>/', views.index_thread, name = "index_thread"),
    path('user/<str:username>/', views.index_user, name = "index_user"),
    path('index_posts/', views.index_posts, name = "index_posts"),
    path('members_list/', views.index_users, name = "index_users"),
    path('register/', views.register, name = "register"),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', CustomLoginView.as_view(), name="login"),
    #path('login/', auth_views.LoginView.as_view(template_name="main/login.html", extra_context={
    #   'Threads': Thread.objects.all().order_by("Time_Created")[:10]}),
     #   name = "login"),
    path('logout/', auth_views.LogoutView.as_view(next_page="/", extra_context={
        'Threads': Thread.objects.all().order_by("Time_Created")[:10]}),
         name="logout"),
    path('create_task/', views.create_task, name='create_task'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.profile, name="profile"),
]