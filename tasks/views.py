from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from labels.models import Label
from statuses.models import Status
from tasks.filters import TaskFilter
from tasks.forms import TaskForm
from tasks.models import Task


@login_required
def task_list(request):
    tasks = Task.objects.all()

    task_filter = TaskFilter(request.GET, queryset=tasks)

    if request.GET.get('self_tasks'):
        tasks = tasks.filter(author=request.user)

    tasks = task_filter.qs

    statuses = Status.objects.all()
    labels = Label.objects.all()
    executors = User.objects.all()

    return render(request, 'tasks/task_list.html', {
        'filter': task_filter,
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
            messages.success(request, 'Задача успешно изменена.')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    title = Task.objects.all()
    statuses = Status.objects.all()
    executors = User.objects.all()
    labels = Label.objects.all()

    return render(
        request,
        'tasks/task_update.html',
        {
            'form': form,
            'task': task,
            'title': title,
            'statuses': statuses,
            'executors': executors,
            'labels': labels,
        }
    )


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.author != request.user:
        messages.error(request, 'Задачу может удалить только ее автор')
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
