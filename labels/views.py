from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from labels.models import Label
from labels.forms import LabelForm


@login_required
def label_list(request):
    labels = Label.objects.all()
    return render(request, 'labels/label_list.html', {'labels': labels})

@login_required
def label_create(request):
    if request.method == 'POST':
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно создана.')
            return redirect('label_list')
    else:
        form = LabelForm()
    return render(request, 'labels/label_create.html', {'form': form})

@login_required
def label_update(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if request.method == 'POST':
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно изменена')
            return redirect('label_list')
    else:
        form = LabelForm(instance=label)
    return render(request, 'labels/label_update.html', {'form': form, 'label': label})

@login_required
def label_delete(request, pk):
    label = get_object_or_404(Label, pk=pk)

    if request.method == 'POST':
        if label.tasks.exists():
            messages.error(request, 'Невозможно удалить метку, т.к. она связана с задачей.')
            return redirect('label_list')
        
        label.delete()
        messages.success(request, 'Метка успешно удалена')
        return redirect('label_list')
    return render(request, 'labels/label_confirm_delete.html', {'label': label})