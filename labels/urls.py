from django.urls import path
from labels.views import label_list, label_create, label_update, label_delete

urlpatterns = [
    path('', label_list, name='label_list'),
    path('create/', label_create, name='label_create'),
    path('<int:pk>/update/', label_update, name='label_update'),
    path('<int:pk>/delete/', label_delete, name='label_delete'),
]
