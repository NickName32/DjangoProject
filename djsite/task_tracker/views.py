# task_tracker/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all()  # Получаем все задачи из базы данных
    return render(request, 'task_tracker/task_list.html', {'tasks': tasks})


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                title = form.cleaned_data.get('title')
                description = form.cleaned_data.get('description')
                due_date = form.cleaned_data.get('due_date')
                assigned_to = form.cleaned_data.get('assigned_to')

                if title and description and due_date and assigned_to:
                    form.save()
                    return redirect('task_list')
                else:
                    print("Please fill in all required fields")
            except Exception as e:
                print(e)  # Выводим возможную ошибку в консоль
        else:
            print(form.errors)  # Выводим ошибки формы в консоль для отладки
    else:
        form = TaskForm()
    return render(request, 'task_tracker/create_task.html', {'form': form})
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Перенаправление на страницу списка задач
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_tracker/edit_task.html', {'form': form})
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('task_list')
