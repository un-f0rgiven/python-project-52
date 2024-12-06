from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tasks.models import Task
from statuses.models import Status
from labels.models import Label
from django.contrib.auth.models import User
from tasks.forms import TaskForm
from tasks.filters import TaskFilter

@login_required
def task_list(request):
    tasks = Task.objects.all()
    
    # Создание фильтра с текущими GET параметрами
    task_filter = TaskFilter(request.GET, queryset=tasks)

    # Если выбраны только свои задачи, добавляем это условие
    if request.GET.get('self_tasks'):
        tasks = tasks.filter(author=request.user)  # Фильтруем только свои задачи

    # Применяем фильтры из TaskFilter
    tasks = task_filter.qs  # Теперь tasks уже отфильтрованы

    statuses = Status.objects.all()
    labels = Label.objects.all()
    executors = User.objects.all()

    return render(request, 'tasks/task_list.html', {
        'filter': task_filter,  # Передаем фильтр в шаблон
        'statuses': statuses,
        'labels': labels,
        'executors': executors,
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()
            messages.success(request, 'Задача успешно создана')
            return redirect('task_list')
        else:
            print(form.errors)
    else:
        form = TaskForm()

    statuses = Status.objects.all()
    executors = User.objects.all()
    labels = Label.objects.all()

    return render(request, 'tasks/task_create.html', {
        'form': form,
        'statuses': statuses,
        'executors': executors,
        'labels': labels,
    })

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно обновлена.')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    
    title = Task.objects.all()
    statuses = Status.objects.all()
    executors = User.objects.all()
    labels = Label.objects.all().order_by('name')

    return render(request, 'tasks/task_update.html', {'form': form, 'task': task, 'title': title, 'statuses': statuses, 'executors': executors, 'labels': labels,})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.author != request.user:
        messages.error(request, 'У вас нет прав на удаление этой задачи.')
        return redirect('task_list')
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача успешно удалена.')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_show(request, pk):
    task = get_object_or_404(Task, pk=pk)

    return render(request, 'tasks/task_show.html', {'task': task})
