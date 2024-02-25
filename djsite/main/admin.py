from django.contrib import admin
from .models import Board, Thread, Post, Task


admin.site.register(Board)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Task)