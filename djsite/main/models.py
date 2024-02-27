from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Board(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Thread(models.Model):
    Tittle = models.CharField(max_length=150)
    Content = models.TextField(blank=False, null=False, max_length=10000)
    Time_Created = models.DateTimeField(auto_now_add=True)
    Board = models.ForeignKey(Board, on_delete=models.CASCADE)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.Tittle


class Post(models.Model):
    Content = models.CharField(blank=False, null=False, max_length=300)
    Time_Created = models.DateField(auto_now_add=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    ThreadID = models.ForeignKey(Thread, on_delete=models.CASCADE)


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    attached_file = models.FileField(upload_to='attachments/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Chat(models.Model):
    task = models.ForeignKey(Task, related_name='chats', on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat for {self.task.title}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    bio = models.TextField(max_length=500, blank=True)  # Добавляем поле bio

    def __str__(self):
        return self.user.username

