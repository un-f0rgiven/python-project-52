from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from statuses.models import Status
from statuses.forms import StatusForm

@login_required
def status_list(request):
    statuses = Status.objects.all()
    return render(request, 'statuses/status_list.html', {'statuses': statuses})

@login_required
def status_create(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус успешно создан')
            return redirect('status_list')
    else:
        form = StatusForm()
    return render(request, 'statuses/status_create.html', {'form': form})

@login_required
def status_update(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус успешно изменен')
            return redirect('status_list')
    else:
        form = StatusForm(instance=status)
    return render(request, 'statuses/status_update.html', {'form': form})

@login_required
def status_delete(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        status.delete()
        messages.success(request, 'Статус успешно удален')
        return redirect('status_list')
    return render(request, 'statuses/status_confirm_delete.html', {'status': status})