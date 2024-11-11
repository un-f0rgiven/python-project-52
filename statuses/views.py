from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Status
from .forms import StatusForm

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
            return redirect('status_list')
    else:
        form = StatusForm()
    return render(request, 'statuses/status_form.html', {'form': form})

@login_required
def status_update(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('status_list')
    else:
        form = StatusForm(instance=status)
    return render(request, 'statuses/status_form.html', {'form': form})

@login_required
def status_delete(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        status.delete()
        return redirect('status_list')
    return render(request, 'statuses/status_confirm_delete.html', {'status': status})