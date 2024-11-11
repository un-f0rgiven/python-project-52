from django.urls import path
from .views import (
    task_list,
    task_create,
    task_update,
    task_delete,
    task_detail
)

urlpatterns = [
    path('tasks/', task_list, name='task_list'),
    path('tasks/create/', task_create, name='task_create'),
    path('tasks/<int:pk>/update/', task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', task_delete, name='task_delete'),
    path('tasks/<int:pk>/', task_detail, name='task_detail'),
]