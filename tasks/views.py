from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tasks.models import Task
from statuses.models import Status
from labels.models import Label
from django.contrib.auth.models import User
from tasks.forms import TaskForm

@login_required
def task_list(request):
    tasks = Task.objects.all()

    if request.GET.get('self_tasks'):
        tasks = tasks.filter(author=request.user)

    status_id = request.GET.get('status')
    if status_id:
        tasks = tasks.filter(status_id=status_id)

    executor_id = request.GET.get('executor')
    if executor_id:
        tasks = tasks.filter(executor_id=executor_id)

    label_id = request.GET.get('label')
    if label_id:
        tasks = tasks.filter(labels__id=label_id).distinct()

    statuses = Status.objects.all()
    labels = Label.objects.all()
    executors = User.objects.all()

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
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
    
    statuses = Status.objects.all()
    executors = User.objects.all()
    labels = Label.objects.all()

    return render(request, 'tasks/task_update.html', {'form': form, 'task': task, 'statuses': statuses, 'executors': executors, 'labels': labels,})


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
