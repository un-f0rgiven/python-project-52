from django.urls import path

from labels.views import label_create, label_delete, label_list, label_update

urlpatterns = [
    path('', label_list, name='label_list'),
    path('create/', label_create, name='label_create'),
    path('<int:pk>/update/', label_update, name='label_update'),
    path('<int:pk>/delete/', label_delete, name='label_delete'),
]
