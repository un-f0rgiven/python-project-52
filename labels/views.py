from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Label
from .forms import LabelForm

def label_list(request):
    labels = Label.objects.all()
    return render(request, 'labels/label_list.html', {'labels': labels})

def label_create(request):
    if request.method == 'POST':
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно создана.')
            return redirect('label_list')
    else:
        form = LabelForm()
    return render(request, 'labels/label_form.html', {'form': form})

def label_update(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if request.method == 'POST':
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно обновлена.')
            return redirect('label_list')
    else:
        form = LabelForm(instance=label)
    return render(request, 'labels/label_form.html', {'form': form, 'label': label})

def label_delete(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if request.method == 'POST':
        label.delete()
        messages.success(request, 'Метка успешно удалена.')
        return redirect('label_list')
    return render(request, 'labels/label_confirm_delete.html', {'label': label})